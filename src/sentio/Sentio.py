import csv
from src.sentio.Match import Match
from src.sentio.Time import Time

__author__ = 'emrullah'


class Sentio(object):

    def __init__(self):
        self.coordinateData = list()
        self.eventData = list()


    def getCoordinateData(self):
        return self.coordinateData


    def getCoordinateData_byTime(self):
        a = dict()
        for line in self.coordinateData:
            half, minute, second, millisecond, coord_data = int(line[3]), int(line[4]), int(line[5]), int(line[2][-3]),\
                                                        [playerInfo.split(",") for playerInfo in line[6].split("+")[:-1]]
            a.setdefault(half, {})
            a[half].setdefault(minute, {})
            a[half][minute].setdefault(second, {})
            a[half][minute][second][millisecond] = coord_data
        return a


    def getEventData(self):
        return self.eventData


    def getEventData_byTime(self):
        a = dict()
        for line in self.eventData:
            half, minute, second, teamName, js, eventID = int(line[0]), int(line[1]), int(line[2]), \
                                                          line[3], int(line[4]), int(line[5])
            a.setdefault(half, {})
            a[half].setdefault(minute, {})
            a[half][minute].setdefault(second, [])
            a[half][minute][second].append((teamName, js, eventID))
        return a


    def parseSentioData(self, coordinate_data="data/GS_FB_Sentio.txt", event_data="data/GS_FB_Event.txt"):
        with open(coordinate_data) as md, open(event_data) as ed:
            coordinate_dt, event_dt = csv.reader(md, delimiter="\t"), csv.reader(ed, delimiter="\t")
            for line in coordinate_dt: self.coordinateData += [line]
            for line in event_dt: self.eventData += [line]

        self.minMaxOfHalf = Match.get_minMaxOfHalf(self.getCoordinateData())


    def get_ID_Explanation(self):
        a = dict()
        for line in self.getEventData():
            id, explanation = int(line[5]), line[6]
            a[id] = explanation
        return a


    def checkTimeValid_forEvent(self, time, eventData_byTime):
        try:
            eventData_current = eventData_byTime[time.half][time.minute][time.second]
            return eventData_current
        except KeyError:
            current_time = time
            back_time = current_time.back()
            return self.checkTimeValid_forEvent(back_time, eventData_byTime)


    def get_currentEventData(self, time):
        current_time = time
        current_time.set_minMaxOfHalf(self.minMaxOfHalf)
        eventData_byTime = self.getEventData_byTime()
        return self.checkTimeValid_forEvent(current_time, eventData_byTime)


    def get_previousEventData(self, time, chosenSkip):
        if chosenSkip == None: chosenSkip = 0
        current_time = time
        current_time.set_minMaxOfHalf(self.minMaxOfHalf)
        back_time = current_time
        for skipTimes in range(chosenSkip+1):
            back_time = current_time.back()
        eventData_previous = self.get_currentEventData(back_time)
        return eventData_previous


    def __str__(self):
        pass
