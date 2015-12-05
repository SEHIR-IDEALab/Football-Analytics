import math
from src.sentio.Parameters import OBJECT_TYPES
from src.sentio.Time import Time
from src.sentio.file_io.reader.ReaderBase import ReaderBase

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


    @staticmethod
    def calculateSpeedFor(time, coord_info, visual=False, player_id=-1):
        pre_position = None
        speed = 0.0
        for temp_milliseconds in range(time.milliseconds-8, time.milliseconds+2, 2):
            if visual:
                game_instance = coord_info.getGameInstance(Time(time.half, temp_milliseconds))
                if game_instance:
                    idToPlayers = ReaderBase.mapIDToPlayers(game_instance.players)
                    try:
                        player = idToPlayers[player_id]
                        position = player.get_position()
                    except:
                        position = None
                else:
                    position = None
            else:
                position = coord_info[time.half][temp_milliseconds]

            if pre_position and position:
                speed += math.sqrt(pow(position[0]-pre_position[0],2) + pow(position[1]-pre_position[1],2))
            if position: ### needed to handle missing positions
                pre_position = position

        return float("{0:.2f}".format(speed))


    @staticmethod
    def calculateDirectionFor(time, coord_info, visual=False, player_id=-1):
        positions = []
        for temp_milliseconds in range(time.milliseconds, time.milliseconds+4, 2):
            if visual:
                game_instance = coord_info.getGameInstance(Time(time.half, temp_milliseconds))
                if game_instance:
                    idToPlayers = ReaderBase.mapIDToPlayers(game_instance.players)
                    try:
                        player = idToPlayers[player_id]
                        temp_position = player.get_position()
                    except:
                        temp_position = None
                else:
                    temp_position = None
            else:
                temp_position = coord_info[time.half][temp_milliseconds]
            if temp_position:
                positions.append(temp_position)

        if len(positions) != 2:
            return 0.0

        x1, y1 = positions[0]
        x2, y2 = positions[1]
        if y2 > y1: sign = 1
        else: sign = -1
        try:
            Q = math.degrees(math.atan((y2-y1)/(x2-x1)))
        except ZeroDivisionError:
            if sign > 0: Q = 90.0
            else: Q = 270.0
        if Q < 0: Q = Q + 360.0
        if Q==0.0: Q = 0.0
        return float("{0:.2f}".format(Q))


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


    def __str__(self):
        return "%s, %s, %s, %s" % (self.getTypeName(), self.jersey_number, self.position_x, self.position_y)
