import math, operator, requests
from bs4 import BeautifulSoup

class Meteostation:
    def __init__(self, code, name, latitude, longitude, type, parameter):
        self.code = code
        self.name = name
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.type = type
        self.parameter = parameter
        self.distance = None
        self.temperature = None
        self.pressure = None
        self.humidity = None

class Location:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = float(latitude)
        self.longitude = float(longitude)

class Meteo:
    def __init__(self):
        self.myLocation = None #Location("init", 50, 14)
        self.myLocationId = 0
        self.listMeteo = []
        self.locations = []
        self.result = []

    def ReadMeteoStationsLocations(self):
        count = -1
        with open('meteostanice.csv', encoding='utf-8') as file:
            for line in file:
                count += 1
                elements = line.split(';')
                if len(elements) > 5:
                    self.listMeteo.append(Meteostation(elements[0], elements[1], elements[2], elements[3], elements[4], elements[5]))


        count = 0
        with open('location.csv', encoding='utf-8') as file1:
            for line in file1:
                #count += 1
                elements = line.split(';')
                if len(elements) > 2:
                    self.locations.append(Location(elements[0], elements[1], elements[2]))

    def SetMyLocation(self, id):
        self.myLocationId = id

    def FindNearestMeteostations(self):
        """
        FROM PHP
        $dLatitude = abs($station->latitude - $myLatitude) * 6378 * 2 * pi() / 360;
	    $Longitude = abs($station->longitude - $myLongitude) * 6378 * 2 * pi() / 360;
	    $station->distance = sqrt(($dLatitude * $dLatitude) + ($Longitude * $Longitude));
        """
        self.myLocation = self.locations[int(self.myLocationId)];
        for meteo in self.listMeteo:
            dLat = abs(meteo.latitude - self.myLocation.latitude) * 6378 * 2 * math.pi / 360
            dLong = abs(meteo.longitude - self.myLocation.longitude) * 6378 * 2 * math.pi / 360
            meteo.distance = math.sqrt((dLat ** 2) + (dLong ** 2))
        self.listMeteo.sort(key = operator.attrgetter('distance'))
        """
        print("Location: {}".format(self.myLocation.name))
        print("\nMeteostations\n")
        for meteo in self.listMeteo:
            print("{}: distance: {}".format(meteo.name,meteo.distance))
        """

    def GetValues(self):
        for i in range(0,15):
            url = "https://www.in-pocasi.cz/" + self.listMeteo[i].parameter + "/" + self.listMeteo[i].code + "/"
            result = requests.get(url)
            soup = BeautifulSoup(result.text, "html.parser")
            #els = soup.find_all(attrs={"href":"setting-up-django-sitemaps", "id":"link"})   #Multiple attributes
            tag = soup.find('td', attrs={'data-title': 'Teplota'})
            if tag != None:
                 self.listMeteo[i].temperature = tag.text
                 self.result.append(i)

            tag = soup.find('td', attrs={'data-title': 'Tlak'})
            if tag != None:
                 self.listMeteo[i].pressure = tag.text

            tag = soup.find('td', attrs={'data-title': 'Vlhkost'})
            if tag != None:
                 self.listMeteo[i].humidity = tag.text
                 #temperature = tag['class'] # attributes
                 #print("{}: {}".format(tag, temperature))
