from utils import *
import sys

# Function that prints the data to a .dat file
def outputToFile(name, data, timeLine):
    outputVehicles = open('data/' + name + '.dat', 'w')
    for index in range(0, len(timeLine)):
        dataVehicles = str(timeLine[index]) + "      " + str(data[index]) + "\n"
        outputVehicles.write(dataVehicles)

# iterate the compartiments and output each compartiment to a.dat file
def iterateCompartiments(compartimentsList, time):
    for compartiment in compartimentsList:
        outputToFile(compartiment.getName(True), compartiment.getData(True), time)
        outputToFile(compartiment.getName(False), compartiment.getData(False), time)

def main(argv):
    print("Simulation of traffic on the ring of Antwerp")
    print("Which timeframe do you want to simulate:")
    print("Option 1: 10h-15h (non peak) DEFAULT")
    print("Option 2: 6h30-8h30 (morning peak)")
    print("Option 3: 15h30-17h30 (evening peak)")
    option = input()

    # Initialisation of the 6 sources
    AntwerpSouth = Source("AntwerpSouth", 15.40, 42.87)
    AntwerpEast = Source("AntwerpEast", 56.67, 24.32)
    AntwerpNorth = Source("AntwerpNorth", 55.08, 10.70)
    AntwerpWest = Source("AntwerpWest", 15.75, 60.05)
    Beveren = Source("Beveren", 7.89, 19.80)
    AntwerpPort = Source("AntwerpPort", 14.76, 6.89)
    timePeriod = 300

    # Initialisation of the 8 compartiments and 2 bottlenecks
    KennedyTunnel = Compartiment("KennedyTunnel", 180, 0.59)
    LiefkensHoekTunnel = Compartiment("LiefkensHoekTunnel", 280, 1.374)
    Compartiment1 = Compartiment("Beveren-AntwerpWest", 1878, 8.9)
    Compartiment2 = Compartiment("AntwerpWest-Kennedy", 456, 1.5)
    Compartiment3 = Compartiment("Kennedy-AntwerpSouth", 977, 3.2)
    Compartiment4 = Compartiment("AntwerpSouth-AntwerpEast", 1252, 4.1)
    Compartiment5 = Compartiment("AntwerpEast-AntwerpNorth", 2239, 5.5)
    Compartiment6 = Compartiment("AntwerpNorth-AntwerpPort", 2300, 9.6)
    Compartiment7 = Compartiment("AntwerpPort-LiefkensHoek", 814, 4.0)
    Compartiment8 = Compartiment("LiefkensHoek-Beveren", 1404, 6.3)
    compartimentsList = [Compartiment1, Compartiment2, Compartiment3, Compartiment4, Compartiment5, \
                         Compartiment6, Compartiment7, Compartiment8, KennedyTunnel, LiefkensHoekTunnel]

    # Morning hours
    if option == "2":
        # Morning values
        AntwerpSouth = Source("AntwerpSouth", 24.9583, 51.175)
        AntwerpEast = Source("AntwerpEast", 56.4083, 25.508)
        AntwerpNorth = Source("AntwerpNorth", 65.258, 25.258)
        AntwerpWest = Source("AntwerpWest", 24.025, 64.067)
        Beveren = Source("Beveren", 17.8916, 41.3583)
        AntwerpPort = Source("AntwerpPort", 22.375, 12.367)
        timePeriod = 120

    # Evening hours
    if option == "3" or option == "4":
        # Evening values
        AntwerpSouth = Source("AntwerpSouth", 21.5416, 51.79167)
        AntwerpEast = Source("AntwerpEast", 57.1583, 21.058)
        AntwerpNorth = Source("AntwerpNorth", 49.39167, 10.375)
        AntwerpWest = Source("AntwerpWest", 20.983, 45.49166)
        Beveren = Source("Beveren", 10.0667, 20.8833)
        AntwerpPort = Source("AntwerpPort", 20.0083, 8.8167)
        timePeriod = 120
        if option == "4":
            timePeriod = 200


    # 1 timestep is a minute
    time = list(range(timePeriod))
    for t in time:
        print("Timestep", t)

        # Compartiment 1
        Compartiment1.simulateClockwise(AntwerpWest.getVehicles(True) + Compartiment2.getFlow(True, 0.303),
                                        Compartiment2)
        Compartiment1.simulateCounterClockwise(Beveren.getVehicles(False) + Compartiment8.getFlow(False, 0.043),
                                               Compartiment8)

        # Compartiment 2
        Compartiment2.simulateClockwise(KennedyTunnel.getFlow(True, 0), KennedyTunnel)
        Compartiment2.simulateCounterClockwise(AntwerpWest.getVehicles(False), Compartiment1)

        # Kennedy tunnel
        KennedyTunnel.simulateClockwise(Compartiment3.getFlow(True, 0), Compartiment3)
        KennedyTunnel.simulateCounterClockwise(Compartiment2.getFlow(False, 0), Compartiment2)

        # Compartiment 3
        Compartiment3.simulateClockwise(AntwerpSouth.getVehicles(True) + Compartiment4.getFlow(True, 0.234),
                                        Compartiment4)
        Compartiment3.simulateCounterClockwise(KennedyTunnel.getFlow(False, 0), KennedyTunnel)

        # Compartiment 4
        Compartiment4.simulateClockwise(AntwerpEast.getVehicles(True) + Compartiment5.getFlow(True, 0.124),
                                        Compartiment5)
        Compartiment4.simulateCounterClockwise(
            AntwerpSouth.getVehicles(False) + Compartiment3.getFlow(False, 0.234), Compartiment3)

        # Compartiment 5
        Compartiment5.simulateClockwise(AntwerpNorth.getVehicles(True) + Compartiment6.getFlow(True, 0.263),
                                        Compartiment6)
        Compartiment5.simulateCounterClockwise(AntwerpEast.getVehicles(False) + Compartiment4.getFlow(False, 0.124),
                                               Compartiment4)

        # Compartiment 6
        Compartiment6.simulateClockwise(AntwerpPort.getVehicles(True) + Compartiment7.getFlow(True, 0.033),
                                        Compartiment7)
        Compartiment6.simulateCounterClockwise(
            AntwerpNorth.getVehicles(False) + Compartiment5.getFlow(False, 0.263), Compartiment5)

        # Compartiment 7
        Compartiment7.simulateClockwise(LiefkensHoekTunnel.getFlow(True, 0), LiefkensHoekTunnel)
        Compartiment7.simulateCounterClockwise(AntwerpPort.getVehicles(False) + Compartiment6.getFlow(False, 0.033),
                                               Compartiment6)

        # Liefkenshoektunnel
        LiefkensHoekTunnel.simulateClockwise(Compartiment8.getFlow(True, 0), Compartiment8)
        LiefkensHoekTunnel.simulateCounterClockwise(Compartiment7.getFlow(False, 0), Compartiment7)

        # Compartiment 8
        Compartiment8.simulateClockwise(Beveren.getVehicles(True) + Compartiment1.getFlow(True, 0.043),
                                        Compartiment1)
        Compartiment8.simulateCounterClockwise(LiefkensHoekTunnel.getFlow(False, 0), LiefkensHoekTunnel)

    iterateCompartiments(compartimentsList, time)

if __name__ == '__main__':
    main(sys.argv)
