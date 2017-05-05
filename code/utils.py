class Vehicle:
    def __init__(self):
        self.distance = 0

    def travel(self):
        # A vehicle travelling @ 100 km/h will travel 1.67 km in 1 min/timestep
        self.distance += 1.67

    def reachedDistance(self, distance):
        if self.distance >= distance: return True
        return False


class Compartiment:
    ''' 
        Compartiment class with represents a certain compartiment of the ring of Antwerp

        Attributes:
        name           -- The name of the compartiment
        maxCapacity    -- The max capacity/number of vehicles of the compartiment
    '''

    def __init__(self, name, capacity, distance, incoming=None, outgoing=None):
        self.name = name
        self.maxCapacity = capacity
        self.distance = distance
        self.capacityClockwise = list()
        self.capacityCounterClockwise = list()
        self.dataClockwise = list()
        self.dataCounterClockwise = list()
        self.flowClockwise = incoming
        self.flowCounterClockwise = outgoing

    def getName(self, clockwise):
        if clockwise: return str(self.name) + 'Clockwise'
        return str(self.name) + 'CounterClockwise'

    def getData(self, clockwise):
        if clockwise: return self.dataClockwise
        return self.dataCounterClockwise

    def simulateClockwise(self, vehicles):
        for veh in self.capacityClockwise: veh.travel()
        self.capacityClockwise = [veh for veh in self.capacityClockwise if not veh.reachedDistance(self.distance)]
        for i in range(0,int(vehicles)):
            newVehicle = Vehicle()
            self.capacityClockwise.append(newVehicle)
        self.dataClockwise.append(len(self.capacityClockwise))

    def simulateCounterClockwise(self, vehicles):
        for veh in self.capacityCounterClockwise: veh.travel()
        self.capacityCounterClockwise = [veh for veh in self.capacityCounterClockwise if not veh.reachedDistance(self.distance)]
        for i in range(0,int(vehicles)):
            newVehicle = Vehicle()
            self.capacityCounterClockwise.append(newVehicle)
        self.dataCounterClockwise.append(len(self.capacityCounterClockwise))

    def __repr__(self):
        returnVal = "Compartiment " + str(self.name) + " contains currently " + str(len(self.capacityClockwise)) + " vehicles"
        returnVal += "(clockwise) and " + str(len(self.capacityCounterClockwise))
        returnVal += "(counterclockwise) and has a maximum capacity of " + str(self.maxCapacity)
        return returnVal

    def flowThrough(self, clockwise):
        if clockwise: return self.flowClockwise
        return self.flowCounterClockwise


class Source:
    def __init__(self, rate1, rate2):
        self.rateClockwise = rate1
        self.rateCounterClockwise = rate2

    def getVehicles(self, clockwise):
        if clockwise: return self.rateClockwise
        return self.rateCounterClockwise
        