class Vehicle:
    def __init__(self):
        ''' Vehicle class that keeps track of the travelled distance of the vehicle'''
        self.distance = 0

    def __repr__(self):
        return "Vehicle with a travelled distance of " + str(self.distance)

    def travel(self):
        # A vehicle travelling @ 100 km/h will travel 1.67 km in 1 min-timestep
        self.distance += 1.67

    def reachedDistance(self, distance):
        # Check if the vehicle has reached the distance / reached the next compartiment
        if self.distance >= distance: return True
        return False


class Compartiment:
    ''' 
        Compartiment class with represents a certain compartiment of the ring of Antwerp

        Attributes:
        name                        -- The name of the compartiment
        maxCapacity                 -- The max capacity/number of vehicles of the compartiment
        distance                    -- The length of the compartiment in kilometres
        capacityClockwise           -- The current vehicles in the clockwise direction
        capacityCounterClockwise    -- The current vehicles in the counter clockwise direction
        dataClockwise               -- The data of the clockwise direction
        dataCounterClockwise        -- The data of the counter clockwise direction
    '''

    def __init__(self, name, capacity, distance):
        self.name = name
        self.maxCapacity = capacity
        self.distance = distance
        self.capacityClockwise = list()
        self.capacityCounterClockwise = list()
        self.dataClockwise = list()
        self.dataCounterClockwise = list()
        # TODO use list later
        # self.reachedNextCompartimentClockwise = list()
        # self.reachedNextCompartimentCounterClockwise = list()
        self.reachedNextCompartimentClockwise = 0
        self.reachedNextCompartimentCounterClockwise = 0

    def __repr__(self):
        returnVal = "Compartiment " + str(self.name) + " contains currently " + str(len(self.capacityClockwise)) + " vehicles"
        returnVal += "(clockwise) and " + str(len(self.capacityCounterClockwise))
        returnVal += "(counterclockwise) and has a maximum capacity of " + str(self.maxCapacity)
        return returnVal

    def getName(self, clockwise):
        if clockwise: return str(self.name) + 'Clockwise'
        return str(self.name) + 'CounterClockwise'

    def getData(self, clockwise):
        if clockwise: return self.dataClockwise
        return self.dataCounterClockwise

    def getFlow(self, clockwise, ratio=0.6):
        if clockwise: return ratio*self.reachedNextCompartimentClockwise
        return ratio*self.reachedNextCompartimentCounterClockwise

    def simulateClockwise(self, vehicles):
        if len(self.capacityClockwise) >= self.maxCapacity: print("Traffic congestion in the clockwise direction @ compartiment {0}".format(str(self.name)))
        self.dataClockwise.append(len(self.capacityClockwise))
        for veh in self.capacityClockwise: veh.travel()
        self.reachedNextCompartimentClockwise = len([veh for veh in self.capacityClockwise if veh.reachedDistance(self.distance)])
        self.capacityClockwise = [veh for veh in self.capacityClockwise if not veh.reachedDistance(self.distance)]
        for i in range(0,int(vehicles)):
            newVehicle = Vehicle()
            self.capacityClockwise.append(newVehicle)

    def simulateCounterClockwise(self, vehicles):
        if len(self.capacityCounterClockwise) >= self.maxCapacity: print("Traffic congestion in the counterclockwise direction @ compartiment {0}".format(str(self.name)))
        self.dataCounterClockwise.append(len(self.capacityCounterClockwise))
        for veh in self.capacityCounterClockwise: veh.travel()
        self.reachedNextCompartimentCounterClockwise = len([veh for veh in self.capacityCounterClockwise if veh.reachedDistance(self.distance)])
        self.capacityCounterClockwise = [veh for veh in self.capacityCounterClockwise if not veh.reachedDistance(self.distance)]
        for i in range(0,int(vehicles)):
            newVehicle = Vehicle()
            self.capacityCounterClockwise.append(newVehicle)

class Source:
    def __init__(self, name, rate1, rate2):
        ''' Class that represent an incoming road/source of vehicles'''
        self.name = name
        self.rateClockwise = rate1
        self.rateCounterClockwise = rate2

    def __repr__(self):
        returnValue = "Source "+ str(self.name) + " has a rate of " + str(self.rateClockwise) + " (clockwise) and"
        returnValue += "a rate of " + str(self.rateCounterClockwise) + " (counterclockwise)."
        return returnValue

    def getVehicles(self, clockwise):
        if clockwise: return self.rateClockwise
        return self.rateCounterClockwise
        