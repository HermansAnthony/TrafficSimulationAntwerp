class Source:
    def __init__(self, name, rate1, rate2):
        ''' 
            Class that represent an incoming road/source of vehicles
        
            Attributes:
            name                                        -- The name of the source
            rateClockwise                               -- The rate in the clockwise direction
            rateCounterClockwise                        -- The rate in the counter clockwise direction
        '''
        self.name = name
        self.rateClockwise = rate1
        self.rateCounterClockwise = rate2

    def __repr__(self):
        returnValue = "Source " + str(self.name) + " has a rate of " + str(self.rateClockwise) + " (clockwise) and"
        returnValue += "a rate of " + str(self.rateCounterClockwise) + " (counterclockwise)."
        return returnValue

    def getVehicles(self, clockwise):
        if clockwise: return self.rateClockwise
        return self.rateCounterClockwise


class Compartiment:
    ''' 
        Compartiment class with represents a certain compartiment of the ring of Antwerp

        Attributes:
        name                                        -- The name of the compartiment
        maxCapacity                                 -- The max capacity/number of vehicles of the compartiment
        distance                                    -- The length of the compartiment in kilometres
        capacityClockwise                           -- The current vehicles in the clockwise direction
        capacityCounterClockwise                    -- The current vehicles in the counter clockwise direction
        dataClockwise                               -- The data of the clockwise direction
        dataCounterClockwise                        -- The data of the counter clockwise direction
        reachedNextCompartimentClockwise            -- The vehicles ready for the next compartiment (clockwise)
        reachedNextCompartimentCounterClockwise     -- The vehicles ready for the next compartiment (counter clockwise)
    '''

    def __init__(self, name, capacity, distance):
        self.name = name
        self.maxCapacity = capacity
        self.distance = distance
        self.capacityClockwise = list()
        self.capacityCounterClockwise = list()
        self.dataClockwise = list()
        self.dataCounterClockwise = list()
        self.reachedNextCompartimentClockwise = 0
        self.reachedNextCompartimentCounterClockwise = 0
        self.waitingClockWise = 0
        self.waitingCounterClockWise = 0

    def __repr__(self):
        returnVal = "Compartiment " + str(self.name) + " contains currently " + str(
            len(self.capacityClockwise)) + " vehicles"
        returnVal += "(clockwise) and " + str(len(self.capacityCounterClockwise))
        returnVal += "(counterclockwise) and has a maximum capacity of " + str(self.maxCapacity)
        return returnVal

    def getName(self, clockwise):
        if clockwise: return str(self.name) + 'Clockwise'
        return str(self.name) + 'CounterClockwise'

    def getData(self, clockwise):
        if clockwise: return self.dataClockwise
        return self.dataCounterClockwise

    def getFlow(self, clockwise, ratio):
        if clockwise: return (1 - ratio) * self.reachedNextCompartimentClockwise
        return (1 - ratio) * self.reachedNextCompartimentCounterClockwise

    def oosterWeelVerbinding(self):
        length = 0.33*len(self.capacityClockwise) + 0.33 * len(self.capacityCounterClockwise)
        return [0] * int(length)



    def waitingVehicles(self, clockwise, vehicles):
        if clockwise:
            for i in range(0,int(vehicles)):
                self.capacityClockwise.append(0)
        if not clockwise:
            for i in range(0,int(vehicles)):
                self.capacityCounterClockwise.append(0)

    def simulateClockwise(self, vehicles, prevCompartiment):
        rate = 1 - (len(self.capacityClockwise) / self.maxCapacity)**8
        travelDistance = rate * 1.67
        acceptedVehicles = rate * vehicles
        self.dataClockwise.append(len(self.capacityClockwise))
        if len(self.capacityClockwise) >= self.maxCapacity: print(
            "Traffic congestion in the clockwise direction @ compartiment {0}".format(str(self.name)))
        self.capacityClockwise = [veh + travelDistance for veh in self.capacityClockwise]
        self.reachedNextCompartimentClockwise = len([veh for veh in self.capacityClockwise if veh >= self.distance])
        self.capacityClockwise = [veh for veh in self.capacityClockwise if veh < self.distance]

        waitingVehicles = 0
        for i in range(0, int(acceptedVehicles)):
            if len(self.capacityClockwise) >= self.maxCapacity:
                waitingVehicles += 1
                continue
            self.capacityClockwise.append(0)

        prevCompartiment.waitingVehicles(True, waitingVehicles)

    def simulateCounterClockwise(self, vehicles, prevCompartiment):
        rate = 1 - (len(self.capacityCounterClockwise) / self.maxCapacity) ** 8
        acceptedVehicles = rate * vehicles
        travelDistance = rate * 1.67
        self.dataCounterClockwise.append(len(self.capacityCounterClockwise))
        if len(self.capacityCounterClockwise) >= self.maxCapacity: print(
            "Traffic congestion in the counterclockwise direction @ compartiment {0}".format(str(self.name)))

        self.capacityCounterClockwise = [veh + travelDistance for veh in self.capacityCounterClockwise]
        self.reachedNextCompartimentCounterClockwise = len([veh for veh in self.capacityCounterClockwise if veh >= self.distance])
        self.capacityCounterClockwise = [veh for veh in self.capacityCounterClockwise if veh < self.distance]

        waitingVehicles = 0
        for i in range(0, int(acceptedVehicles)):
            if len(self.capacityCounterClockwise) >= self.maxCapacity:
                waitingVehicles += 1
                continue
            self.capacityCounterClockwise.append(0)

        prevCompartiment.waitingVehicles(False, waitingVehicles)
