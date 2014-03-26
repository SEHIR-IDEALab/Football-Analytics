import csv

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
            half, minute, second, mili_second, coord_data = int(line[3]), int(line[4]), int(line[5]), int(line[2][-3]), \
                                                        [playerInfo.split(",") for playerInfo in line[6].split("+")[:-1]]
            a.setdefault(half, {})
            a[half].setdefault(minute, {})
            a[half][minute].setdefault(second, {})
            a[half][minute][second][mili_second] = coord_data
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


    def __str__(self):
        pass
