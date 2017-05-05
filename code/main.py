from utils import *
import sys

# Function that prints the data to a .dat file
def outputToFile(name, data, timeLine):
    outputVehicles = open('data/' + name +'.dat', 'w')
    for index in range(0,len(timeLine)):
        dataVehicles = str(timeLine[index]) + "      " + str(data[index]) + "\n"
        outputVehicles.write(dataVehicles)

def main(argv):
    print("Simulation of traffic on the ring of Antwerp")

    # Initialisation of the 6 sources
    AntwerpSouth    = Source(15.40, 42.87)
    AntwerpEast     = Source(56.67, 24.32)
    AntwerpNorth    = Source(55.08, 10.70)
    AntwerpWest     = Source(15.75, 60.05)
    Beveren         = Source(7.89, 19.80)
    AntwerpPort     = Source(14.76, 6.89)

    # Initialisation of the 8 compartiments and 2 bottlenecks
    KennedyTunnel       = Compartiment("KennedyTunnel", 180, 0.59, 7.89, 6.89)
    LiefkensHoekTunnel  = Compartiment("LiefkensHoekTunnel", 280, 1.374, 15.40, 60.05)
    Compartiment1       = Compartiment("Beveren-AntwerpWest", 1878, 8.9)
    Compartiment2       = Compartiment("AntwerpWest-Kennedy", 456, 1.5)
    Compartiment3       = Compartiment("Kennedy-AntwerpSouth", 977, 3.2)
    Compartiment4       = Compartiment("AntwerpSouth-AntwerpEast", 1252, 4.1)
    Compartiment5       = Compartiment("AntwerpEast-AntwerpNorth", 2239, 5.5)
    Compartiment6       = Compartiment("AntwerpNorth-AntwerpPort", 2300, 9.6)
    Compartiment7       = Compartiment("AntwerpPort-LiefkensHoek", 814, 4.0)
    Compartiment8       = Compartiment("LiefkensHoek-Beveren", 1404, 6.3)


    # TODO add support for the bottlenecks + flowthrough of vehicles
    # 1 timestep is a minute
    compartimentsList = [Compartiment1,Compartiment2,Compartiment3,Compartiment4,Compartiment5,\
                         Compartiment6,Compartiment7,Compartiment8]
    time = list(range(300))
    for t in time:

        print("Timestep", t)

        # Compartiment 1
        Compartiment1.simulateClockwise(Beveren.getVehicles(False))
        Compartiment1.simulateCounterClockwise(AntwerpWest.getVehicles(True))

        # Compartiment 2
        Compartiment2.simulateClockwise(KennedyTunnel.flowThrough(True))
        Compartiment2.simulateCounterClockwise(AntwerpWest.getVehicles(False))

        # Compartiment 3
        Compartiment3.simulateClockwise(AntwerpSouth.getVehicles(True))
        Compartiment3.simulateCounterClockwise(KennedyTunnel.flowThrough(False))

        # Compartiment 4
        Compartiment4.simulateClockwise(AntwerpSouth.getVehicles(False))
        Compartiment4.simulateCounterClockwise(AntwerpEast.getVehicles(True))

        # Compartiment 5
        Compartiment5.simulateClockwise(AntwerpNorth.getVehicles(True))
        Compartiment5.simulateCounterClockwise(AntwerpEast.getVehicles(False))

        # Compartiment 6
        Compartiment6.simulateClockwise(AntwerpPort.getVehicles(True))
        Compartiment6.simulateCounterClockwise(AntwerpNorth.getVehicles(False))

        # Compartiment 7
        Compartiment7.simulateClockwise(LiefkensHoekTunnel.flowThrough(True))
        Compartiment7.simulateCounterClockwise(AntwerpPort.getVehicles(False))

        # Compartiment 8
        Compartiment8.simulateClockwise(Beveren.getVehicles(True))
        Compartiment8.simulateCounterClockwise(LiefkensHoekTunnel.flowThrough(False))

    for compartiment in compartimentsList:
        outputToFile(compartiment.getName(True),compartiment.getData(True), time)
        outputToFile(compartiment.getName(False), compartiment.getData(False), time)

if __name__ == '__main__':
    main(sys.argv)