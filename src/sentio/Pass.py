import math
from src.sentio.Player_base import Player_base

__author__ = 'emrullah'


class Pass:

    def __init__(self, coordinateDataOfObjects=None):
        self.coordinateDataOfObjects = self.convertTextsToPlayers(coordinateDataOfObjects)


    @staticmethod
    def convertTextsToPlayers(coordinateDataOfObjects):
        if coordinateDataOfObjects == None: return None
        q = []
        for p in coordinateDataOfObjects:
            p = p.point
            object_type, object_id, js, (x, y) = p.object_type, p.object_id, p.get_text(), p.get_position()
            player_base = Player_base([object_type, object_id, js, x, y])
            q.append(player_base)
        return q


    def displayDefinedPass(self, definedPass, passDisplayer):
        p1 = definedPass.textcoords
        p2 = definedPass.xycoords
        object_type1, object_id1, js1, (x1, y1) = p1.object_type, p1.object_id, p1.get_text(), p1.get_position()
        object_type2, object_id2, js2, (x2, y2) = p2.object_type, p2.object_id, p2.get_text(), p2.get_position()

        p1 = Player_base([object_type1, object_id1,js1, x1, y1])
        p2 = Player_base([object_type2, object_id2,js2, x2, y2])

        effectiveness = self.effectiveness(p1, p2)

        passDisplayer.insert("1.0", "goal_chance = %.2f\n" %self.goalChance(p2))
        passDisplayer.insert("1.0", "effectiveness = %.2f\n" %effectiveness)
        passDisplayer.insert("1.0", "pass_advantage = %.2f (%s)\n" %self.passAdvantage(p2))
        passDisplayer.insert("1.0", "gain = %.2f\n" %self.gain(p1, p2))
        passDisplayer.insert("1.0", "overall_risk(%s->%s) = %.2f\n" %(p1.getJerseyNumber(), p2.getJerseyNumber(),
                                                                      self.overallRisk(p1, p2)))
        passDisplayer.insert("1.0", "\n%s --> %s\n" %(p1.getJerseyNumber(), p2.getJerseyNumber()))

        return effectiveness


    def isInRange(self, p1, p3, p2):
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3

        additional_r = 1

        distance_1to2 = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
        radius_x, radius_y = ((x1 + x2) / 2.), ((y1 + y2) / 2.)
        distance_radiusTo3 = math.sqrt(math.pow(radius_x - x3, 2) + math.pow(radius_y - y3, 2))
        radius = (distance_1to2 / 2.) + additional_r

        if distance_radiusTo3 <= radius:
            return True
        return False


    def risk(self, p1, p3, p2):
        risk = 0.0

        try: x1, y1 = p1.getPositionX(), p1.getPositionY()
        except AttributeError: x1, y1 = p1

        try: x2, y2 = p2.getPositionX(), p2.getPositionY()
        except AttributeError: x2, y2 = p2

        try: x3, y3 = p3.getPositionX(), p3.getPositionY()
        except AttributeError: x3, y3 = p3

        if not self.isInRange((x1,y1), (x3,y3), (x2,y2)): return risk

        if x2 != x1:
            slope = (y2 - y1) / (x2 - x1)
            a = slope
            b = -1
            c = ( ( slope * (-x1) ) + y1 )
            d2 = math.fabs(a * x3 + b * y3 + c) / math.sqrt(math.pow(a, 2) + math.pow(b, 2))
        else:
            d2 = math.fabs(x3 - x1)
        hypotenuse_1to3 = math.sqrt(math.pow(x3 - x1, 2) + math.pow(y3 - y1, 2))
        d1 = math.sqrt(math.pow(hypotenuse_1to3, 2) - math.pow(d2, 2))

        try: risk = d1 / d2
        except ZeroDivisionError: risk = d1

        return risk


    def overallRisk(self, p1, p2, goalKeeper=True):
        overallRisk = 0.0

        team1 = p1.getTypeName()

        try: js2 = p2.getJerseyNumber()
        except AttributeError: js2 = None

        for p3 in self.coordinateDataOfObjects:
            team3 = p3.getTypeName()

            if team3 not in [team1, "referee", "unknown"]:
                if js2 != None:
                    if js2 != p3.getJerseyNumber():
                        if goalKeeper:
                            overallRisk += self.risk(p1, p3, p2)
                        else:
                            if not p3.isGoalKeeper():
                                overallRisk += self.risk(p1, p3, p2)
                else:
                    if goalKeeper:
                        overallRisk += self.risk(p1, p3, p2)
                    else:
                        if not p3.isGoalKeeper():
                            overallRisk += self.risk(p1, p3, p2)
        return overallRisk


    def gain(self, p1, p2):
        x1, y1 = p1.getPositionX(), p1.getPositionY()
        team1 = p1.getTypeName()

        x2, y2 = p2.getPositionX(), p2.getPositionY()

        gain = 0
        left = False
        for p3 in self.coordinateDataOfObjects:
            x3, y3 = p3.get_position()
            team3 = p3.getTypeName()
            if team3 not in [team1, "referee", "unknown"]:
                if x1 <= x3 <= x2 or x2 <= x3 <= x1:
                    gain += 1
                if p3.isGoalKeeper():
                    if x3 <= x1 and x3 <= x2:
                        left = True
        if left:
            if x1 < x2: return -gain
            else: return gain
        else:
            if x1 < x2: return gain
            else: return -gain


    def passAdvantage(self, p1):
        team1 = p1.getTypeName()
        js1 = p1.getJerseyNumber()

        passAdvantages = {}
        for p2 in self.coordinateDataOfObjects:
            js2 = p2.getJerseyNumber()
            team2 = p2.getTypeName()

            if team2 == team1 and js2 != js1:
                pa = ((10 + self.gain(p1, p2)) / (10 + self.overallRisk(p1, p2)))
                passAdvantages[pa] = js2
        max_pass = max(passAdvantages.keys())
        return max_pass, passAdvantages[max_pass]


    def opponentGoalKeeperLocation_isLeft(self, p1):
        team1 = p1.getTypeName()

        goalKeeper_1, goalKeeper_2 = None, None
        for p2 in self.coordinateDataOfObjects:
            x2, y2 = p2.getPositionX(), p2.getPositionY()
            team2 = p2.getTypeName()

            if p2.isGoalKeeper():
                if team2 == team1: goalKeeper_1 = x2
                else: goalKeeper_2 = x2

        if goalKeeper_2 < goalKeeper_1:
            return True
        return False


    def goalChance(self, p1):
        x1, y1 = p1.getPositionX(), p1.getPositionY()

        leftGoalKeeperXY = 0.0, 32.5
        rightGoalKeeperXY = 105.0, 32.5

        if self.opponentGoalKeeperLocation_isLeft(p1): goalKeeperX, goalKeeperY = leftGoalKeeperXY
        else: goalKeeperX, goalKeeperY = rightGoalKeeperXY

        d1 = math.sqrt(math.pow(goalKeeperX - x1, 2) + math.pow(goalKeeperY - y1, 2))
        d2 = 8.5
        angle = math.atan2(math.fabs(y1 - goalKeeperY), math.fabs(x1 - goalKeeperX)) * 180 / math.pi
        angle = math.fabs(90 - angle)
        q = self.overallRisk(p1, [goalKeeperX, goalKeeperY], goalKeeper=False)
        q = (1 if q == 0 else q)
        goalCoefficient = 1000

        d1 = (1 if d1 == 0 else d1)
        return (d2 / d1) * (min(angle, (180 - angle)) / 90.) * (1. / (1 + q)) * goalCoefficient


    def isSuccessfulPass(self, p1, p2):
        team1 = p1.getTypeName()
        team2 = p2.getTypeName()
        if team1 == team2:
            return True
        return False


    def effectiveness(self, p1, p2):
        w1, w2, w3, w4 = 1, 1, 1, 1
        effectiveness = w1 * self.gain(p1, p2) + w3 * self.passAdvantage(p2)[0] + w4 * self.goalChance(p2)
        if not self.isSuccessfulPass(p1, p2):
            return -effectiveness
        return effectiveness


    def effectiveness_withComponents(self, p1, p2):
        w1, w2, w3, w4 = 1, 1, 1, 1
        gain = w1 * self.gain(p1, p2)
        passAdvantage = w3 * self.passAdvantage(p2)[0]
        goalChance = w4 * self.goalChance(p2)
        overallRisk = self.overallRisk(p1, p2)
        effectiveness = gain + passAdvantage + goalChance
        if not self.isSuccessfulPass(p1, p2):
            effectiveness = -effectiveness

        return (effectiveness, gain, passAdvantage, goalChance, overallRisk)


    def __str__(self):
        pass