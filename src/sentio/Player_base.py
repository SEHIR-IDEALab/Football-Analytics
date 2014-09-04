__author__ = 'emrullah'


class Player_base:

    object_types = {0: "Home Team Player", 1: "Away Team Player", 2: "Referee", 3: "Home Team Goalkeeper",
                    4: "Away Team Goalkeeper", -1: "Unknown object", 6: "The other referees",
                    7: "The other referees", 8: "The other referees", 9: "The other referees"}


    def __init__(self, object_info=None):
        if object_info is not None:
            self.object_type = int(object_info[0])
            self.object_id = int(object_info[1])
            self.jersey_number = int(object_info[2])
            self.position_x = float(object_info[3])
            self.position_y = float(object_info[4])


    @staticmethod
    def convertTextsToPlayers(coordinateDataOfObjects):
        if coordinateDataOfObjects is None: return None
        teams = ( {}, {}, {}, {} )
        for index, team in enumerate(coordinateDataOfObjects):
            temp_team = teams[index]
            for js in team:
                p = team[js]
                p = p.point
                object_type, object_id, js, (x, y) = p.object_type, p.object_id, p.get_text(), p.get_position()
                player = Player_base([object_type, object_id, js, x, y])
                temp_team[player.getJerseyNumber()] = player
        return teams


    def getObjectType(self):
        return self.object_type


    def getObjectTypeName(self):
        return self.object_types[self.object_type]


    def getTypeName(self):
        if self.object_type in [0,3]: return "home"
        elif self.object_type in [1,4]: return "away"
        elif self.object_type in [2,6,7,8,9]: return "referee"
        else: return "unknown"


    def getObjectColor(self):
        if self.object_type in [0,3]: return "blue"
        elif self.object_type in [1,4]: return "red"
        elif self.object_type in [2,6,7,8,9]: return "yellow"
        else: return "black"


    def getObjectTypeColor(self):
        if self.object_type == 0: return "blue"
        elif self.object_type == 1: return "red"
        elif self.object_type in [3,4]: return "black"
        elif self.object_type in [2,6,7,8,9]: return "yellow"
        else: return "black"


    def getObjectID(self):
        return self.object_id


    def getJerseyNumber(self):
        return self.jersey_number


    def getPositionX(self):
        return self.position_x


    def getPositionY(self):
        return self.position_y


    def set_position(self, (x,y)):
        self.position_x = x
        self.position_y = y


    def get_position(self):
        return (self.position_x, self.position_y)


    def isGoalKeeper(self):
        if self.object_type in [3,4]:
            return True
        return False


    def __str__(self):
        pass
