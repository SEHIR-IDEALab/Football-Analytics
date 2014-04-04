import math

__author__ = 'doktoray'


class Pass:
    def __init__(self, coordinateDataOfObjects):
        self.coordinateDataOfObjects = coordinateDataOfObjects
        self.teams = {(0.0, 0.0, 1.0, 0.5): "home", (1.0, 0.0, 0.0, 0.5): "away",
                      (1.0, 1.0, 0.0, 0.5): "referee", (0.0, 0.0, 0.0, 0.5): "unknown"}

    def risk(self, p1, p3, p2):
        x1, y1 = p1.get_position()
        team1 = self.teams[p1.get_bbox_patch().get_facecolor()]
        js1 = p1.get_text()

        x2, y2 = None, None
        try:
            x2, y2 = p2.get_position()
            team2 = self.teams[p2.get_bbox_patch().get_facecolor()]
            js2 = p2.get_text()
        except AttributeError:
            x2, y2 = p2

        x3, y3 = p3.get_position()
        js3 = p3.get_text()
        team3 = self.teams[p3.get_bbox_patch().get_facecolor()]

        risk = 0.0
        #if (x1<=x3<=x2 or x2<=x3<=x1) and (y1<=y3<=y2 or y2<=y3<=y1):
        if x1 <= x3 <= x2 or x2 <= x3 <= x1:
            if team3 not in [team1, "referee", "unknown"]:
                slope = (y2 - y1) / (x2 - x1)
                a = slope
                b = -1
                c = ( ( slope * (-x1) ) + y1 )
                d2 = math.fabs(a * x3 + b * y3 + c) / math.sqrt(math.pow(a, 2) + math.pow(b, 2))
                hipotenus_1to3 = math.sqrt(math.pow(x3 - x1, 2) + math.pow(y3 - y1, 2))
                d1 = math.sqrt(math.pow(hipotenus_1to3, 2) - math.pow(d2, 2))
                try:
                    risk = d1 / d2
                except ZeroDivisionError:
                    risk = d1
        return risk

    def overallRisk(self, p1, p2):
        overallRisk = 0.0
        for dragged in self.coordinateDataOfObjects:
            p3 = dragged.point
            overallRisk += self.risk(p1, p3, p2)
        #print overallRisk, self.gain(p1,p2)
        return overallRisk

    def gain(self, p1, p2):
        x1, y1 = p1.get_position()
        team1 = self.teams[p1.get_bbox_patch().get_facecolor()]
        js1 = p1.get_text()

        x2, y2 = p2.get_position()
        team2 = self.teams[p2.get_bbox_patch().get_facecolor()]
        js2 = p2.get_text()

        gain = 0
        opponentTeam = []
        sameTeam = []
        for dragged in self.coordinateDataOfObjects:
            p3 = dragged.point

            x3, y3 = p3.get_position()
            js3 = p3.get_text()
            team3 = self.teams[p3.get_bbox_patch().get_facecolor()]

            if team3 not in [team1, "referee", "unknown"]:
                if x1 <= x3 <= x2 or x2 <= x3 <= x1:
                    gain += 1
                opponentTeam.append(x3)
            elif team3 == team1:
                sameTeam.append(x3)

        min_ultimate = min([min(opponentTeam), min(sameTeam)])
        max_ultimate = max([max(opponentTeam), max(sameTeam)])
        if (min_ultimate in sameTeam) and max_ultimate in opponentTeam:
            if x1 < x2:
                return gain
            else:
                return -gain
        else:
            if x1 < x2:
                return -gain
            else:
                return gain

    def passAdvantage(self, p1):
        x1, y1 = p1.get_position()
        team1 = self.teams[p1.get_bbox_patch().get_facecolor()]
        js1 = p1.get_text()

        passAdvantages = {}
        for dragged in self.coordinateDataOfObjects:
            p2 = dragged.point

            x2, y2 = p2.get_position()
            js2 = p2.get_text()
            team2 = self.teams[p2.get_bbox_patch().get_facecolor()]

            if team2 == team1 and js2 != js1:
                pa = ((10 + self.gain(p1, p2)) / (10 + self.overallRisk(p1, p2)))
                passAdvantages[pa] = js2
        max_pass = max(passAdvantages.keys())
        return max_pass, passAdvantages[max_pass]

    def goalChance(self, p1):
        x1, y1 = p1.get_position()
        team1 = self.teams[p1.get_bbox_patch().get_facecolor()]
        js1 = p1.get_text()

        goalKeeperX, goalKeeperY = 0.0, 32.75
        d1 = math.sqrt(math.pow(goalKeeperX - x1, 2) + math.pow(goalKeeperY - y1, 2))
        d2 = 8.5
        angle = math.atan2(math.fabs(y1 - goalKeeperY), math.fabs(x1 - goalKeeperX)) * 180 / math.pi
        angle = math.fabs(90 - angle)
        q = self.overallRisk(p1, [goalKeeperX, goalKeeperY])
        q = (1 if q == 0 else q)

        return (d2 / d1) * (min(angle, (180 - angle)) / 90) / q * 1000

    def effectiveness(self, p1, p2):
        w1, w2, w3, w4 = 1, 1, 1, 1
        return w1 * self.gain(p1, p2) + w3 * self.passAdvantage(p2)[0] + w4 * self.goalChance(p2)

    def __str__(self):
        pass