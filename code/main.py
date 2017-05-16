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
    AntwerpSouth    = Source("AntwerpSouth", 15.40, 42.87)
    AntwerpEast     = Source("AntwerpEast", 56.67, 24.32)
    AntwerpNorth    = Source("AntwerpNorth", 55.08, 10.70)
    AntwerpWest     = Source("AntwerpWest", 15.75, 60.05)
    Beveren         = Source("Beveren", 7.89, 19.80)
    AntwerpPort     = Source("AntwerpPort", 14.76, 6.89)

    # Initialisation of the 8 compartiments and 2 bottlenecks
    KennedyTunnel       = Compartiment("KennedyTunnel", 180, 0.59)
    LiefkensHoekTunnel  = Compartiment("LiefkensHoekTunnel", 280, 1.374)
    Compartiment1       = Compartiment("Beveren-AntwerpWest", 1878, 8.9)
    Compartiment2       = Compartiment("AntwerpWest-Kennedy", 456, 1.5)
    Compartiment3       = Compartiment("Kennedy-AntwerpSouth", 977, 3.2)
    Compartiment4       = Compartiment("AntwerpSouth-AntwerpEast", 1252, 4.1)
    Compartiment5       = Compartiment("AntwerpEast-AntwerpNorth", 2239, 5.5)
    Compartiment6       = Compartiment("AntwerpNorth-AntwerpPort", 2300, 9.6)
    Compartiment7       = Compartiment("AntwerpPort-LiefkensHoek", 814, 4.0)
    Compartiment8       = Compartiment("LiefkensHoek-Beveren", 1404, 6.3)
    compartimentsList   = [Compartiment1,Compartiment2,Compartiment3,Compartiment4,Compartiment5,\
                            Compartiment6,Compartiment7,Compartiment8, KennedyTunnel, LiefkensHoekTunnel]

    # 1 timestep is a minute
    time = list(range(300))
    for t in time:

        print("Timestep", t)

        # Compartiment 1
        Compartiment1.simulateClockwise(AntwerpWest.getVehicles(True)+Compartiment2.getFlow(True, 0.697))
        Compartiment1.simulateCounterClockwise(Beveren.getVehicles(False)+Compartiment8.getFlow(False, 0.957))

        # Compartiment 2
        Compartiment2.simulateClockwise(KennedyTunnel.getFlow(True, 1))
        Compartiment2.simulateCounterClockwise(AntwerpWest.getVehicles(False))

        # Kennedy tunnel
        KennedyTunnel.simulateClockwise(Compartiment3.getFlow(True, 1))
        KennedyTunnel.simulateCounterClockwise(Compartiment2.getFlow(False, 1))

        # Compartiment 3
        Compartiment3.simulateClockwise(AntwerpSouth.getVehicles(True)+ Compartiment4.getFlow(True, 0.766))
        Compartiment3.simulateCounterClockwise(KennedyTunnel.getFlow(False, 1))

        # Compartiment 4
        Compartiment4.simulateClockwise(AntwerpEast.getVehicles(True) + Compartiment5.getFlow(True, 0.876))
        Compartiment4.simulateCounterClockwise(AntwerpSouth.getVehicles(False) + Compartiment3.getFlow(False, 0.766))

        # Compartiment 5
        Compartiment5.simulateClockwise(AntwerpNorth.getVehicles(True) + Compartiment6.getFlow(True, 0.737))
        Compartiment5.simulateCounterClockwise(AntwerpEast.getVehicles(False) + Compartiment4.getFlow(False, 0.876))

        # Compartiment 6
        Compartiment6.simulateClockwise(AntwerpPort.getVehicles(True) + Compartiment7.getFlow(True, 0.967))
        Compartiment6.simulateCounterClockwise(AntwerpNorth.getVehicles(False) + Compartiment5.getFlow(False, 0.737))

        # Compartiment 7
        Compartiment7.simulateClockwise(LiefkensHoekTunnel.getFlow(True, 1))
        Compartiment7.simulateCounterClockwise(AntwerpPort.getVehicles(False) + Compartiment6.getFlow(False, 0.967))

        # Liefkenshoektunnel
        LiefkensHoekTunnel.simulateClockwise(Compartiment8.getFlow(True, 1))
        LiefkensHoekTunnel.simulateCounterClockwise(Compartiment7.getFlow(False, 1))

        # Compartiment 8
        Compartiment8.simulateClockwise(Beveren.getVehicles(True)+ Compartiment1.getFlow(True, 0.957))
        Compartiment8.simulateCounterClockwise(LiefkensHoekTunnel.getFlow(False, 1))

    for compartiment in compartimentsList:
        outputToFile(compartiment.getName(True), compartiment.getData(True), time)
        outputToFile(compartiment.getName(False), compartiment.getData(False), time)

if __name__ == '__main__':
    main(sys.argv)