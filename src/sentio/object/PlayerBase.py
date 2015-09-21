from src.sentio.Parameters import OBJECT_TYPES

__author__ = 'emrullah'


class PlayerBase:

    def __init__(self, object_info=None):
        if object_info is not None:
            self.object_type = int(object_info[0])
            self.object_id = int(object_info[1])
            self.jersey_number = int(object_info[2])
            self.position_x = float(object_info[3])
            self.position_y = float(object_info[4])

            self.raw_data = object_info


    def getRawData(self):
        return self.raw_data


    def getObjectType(self):
        return self.object_type


    def setDraggableVisualPlayer(self, draggable_visual_player):
        self.draggable_visual_player = draggable_visual_player


    def getDraggableVisualPlayer(self):
        return self.draggable_visual_player


    def getObjectTypeName(self):
        return OBJECT_TYPES[self.object_type]


    def getTypeName(self):
        if self.object_type in [0,3]: return "home"
        elif self.object_type in [1,4]: return "away"
        elif self.object_type in [2,6,7,8,9]: return "referee"
        else: return "unknown"


    def isHomeTeamPlayer(self):
        return self.getTypeName() == "home"


    def isAwayTeamPlayer(self):
        return self.getTypeName() == "away"


    def isReferee(self):
        return self.getTypeName() == "referee"


    def setTeamName(self, team_name):
        self.team_name = team_name


    def getTeamName(self):
        return self.team_name


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


    def setJerseyNumber(self, jersey_number):
        self.jersey_number = jersey_number


    def getJerseyNumber(self):
        return self.jersey_number


    def setX(self, x):
        self.position_x = x


    def getX(self):
        return self.position_x


    def setY(self, y):
        self.position_y = y


    def getY(self):
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
        return "%s, %s, %s" % (self.jersey_number, self.position_x, self.position_y)
