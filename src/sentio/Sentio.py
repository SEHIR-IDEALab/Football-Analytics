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
            try:
                a[half][minute][second][mili_second] = coord_data
            except KeyError:
                try:
                    a[half][minute][second] = {mili_second: coord_data}
                except KeyError:
                    try:
                        a[half][minute] = {second: {mili_second: coord_data}}
                    except KeyError:
                        try:
                            a[half] = {minute: {second: {mili_second: coord_data}}}
                        except KeyError:
                            print "!!!!!!!!!"
        return a

    def getEventData(self):
        return self.eventData

    def getEventData_byTime(self):
        a = dict()
        for line in self.eventData:
            half, minute, second, teamName, js, eventID = int(line[0]), int(line[1]), int(line[2]), \
                                                          line[3], int(line[4]), int(line[5])
            try:
                if second not in a[half][minute]:
                    a[half][minute][second] = [(teamName, js, eventID)]
                else:
                    event_already = a[half][minute][second]
                    event_new = (teamName, js, eventID)
                    event_already.append(event_new)
            except KeyError:
                try:
                    a[half][minute] = {second: [(teamName, js, eventID)]}
                except KeyError:
                    try:
                        a[half] = {minute: {second: [(teamName, js, eventID)]}}
                    except KeyError:
                        print "!!!!!!!!!"
        return a

    def parseSentioData(self, coordinate_data="data/GS_FB_Sentio.txt", event_data="data/GS_FB_Event.txt"):
        with open(coordinate_data) as md, open(event_data) as ed:
            coordinate_dt, event_dt = csv.reader(md, delimiter="\t"), csv.reader(ed, delimiter="\t")
            for line in coordinate_dt: self.coordinateData += [line]
            for line in event_dt: self.eventData += [line]

    def __str__(self):
        pass
