from meteostation import Meteo

if __name__ == '__main__':
    Mstation = Meteo()
    Mstation.ReadMeteoStationsLocations()
    Mstation.SetMyLocation(0)
    Mstation.FindNearestMeteostations()
    Mstation.GetValues()

    print("Lokace: {} \n\nMeteostanice:\n".format(Mstation.myLocation.name))

    for i in range(0, 5):
        print("{0}, {1:3.1f} km, teplota: {2}, tlak: {3}, vlhkost: {4}".format(Mstation.listMeteo[Mstation.result[i]].name, Mstation.listMeteo[Mstation.result[i]].distance, Mstation.listMeteo[Mstation.result[i]].temperature, Mstation.listMeteo[Mstation.result[i]].pressure, Mstation.listMeteo[Mstation.result[i]].humidity))
