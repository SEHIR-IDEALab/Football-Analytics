# coding=utf-8
import os
from src.sentio.pass_evaluate import get_coefficient


__author__ = 'emrullah'



#PATH
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_BASE_DIR = os.path.join(BASE_DIR, '../data')




# team names
HOME_TEAM_NAME = "Home Team"
AWAY_TEAM_NAME = "Away Team"
REFEREES_TEAM_NAME = "Referees"
UNKNOWNS_TEAM_NAME = "Unknowns"

# min-max for each half
INITIAL_HALF_MIN_MAX = {1: ((0,0,0), (44,59,8)), 2: ((45,0,0), (89,59,8))}
HALF_MIN_MAX = {1: ((0, 0, 0), (48, 0, 8)), 2: ((45, 0, 8), (94, 19, 6))}

# football field
FOOTBALL_FIELD_MIN_X = 0.0
FOOTBALL_FIELD_MID_X = 52.5
FOOTBALL_FIELD_MAX_X = 105.0
FOOTBALL_FIELD_MIN_Y = 0.0
FOOTBALL_FIELD_MAX_Y = 70.0

# goalpost
GOALPOST_MIN_X = 0.0
GOALPOST_MAX_X = 105.0
GOALPOST_MIN_Y = 30.0
GOALPOST_MAX_Y = 40.0
GOALPOST_LENGTH = 10.0

# arrow (direction and speed)
INITIAL_ARROW_SIZE = 2

# pass
GOAL_COEFFICIENT = 1

# debug mode
IS_DEBUG_MODE_ON = False
IS_SHOW_DIRECTIONS_ON = False
IS_VORONOI_DIAGRAM_ON = False

# radius of pass_source
PASS_SOURCE_RADIUS = 1.0

# radius coefficient of pass target
PASS_TARGET_RADIUS_COEFFICIENT = 6.0
# radius of back risk area
SOURCE_ANGLE = 60.0

#probability of player run at specific speed

# COEFFICIENTS = get_coefficient()
# print COEFFICIENTS
COEFFICIENTS = {3.5: 0.6600497742899443, 4.5: 0.2888679982197517, 3.0: 1.0, 4.3: 0.33994568426024324, 5.0: 0.1969399711163792, 9.5: 0.005990172302605884, 7.0: 0.049747041245447196, 8.0: 0.025799976384460976, 7.3: 0.04107741355350282, 10.0: 0.0008946656130503102, 8.1: 0.024137805753108622, 3.4: 0.7184619017775234, 4.1: 0.39962033479568015, 3.3: 0.7830367766605811, 7.6: 0.033661226009791365, 8.5: 0.0179523511085679, 3.8: 0.5097368683978674, 3.1: 0.9233948245637937, 4.2: 0.3687929734688502, 7.2: 0.043852239388902516, 6.0: 0.09554756260388567, 4.7: 0.24690046050301098, 6.5: 0.0680581668891977, 3.2: 0.8513401818396505, 5.2: 0.17036794826380375, 6.6: 0.06422972469731238, 5.3: 0.1586419248480885, 6.2: 0.08275429848224747, 3.6: 0.6047303741246356, 4.9: 0.21219924248617128, 6.7: 0.06011517116724343, 9.0: 0.011607945720591841, 9.7: 0.004028265983632615, 9.4: 0.007202739402526863, 8.3: 0.02092700073571487, 7.7: 0.03141774980244693, 8.2: 0.022480176571568707, 9.3: 0.00827452155826226, 6.8: 0.05644113826898099, 5.7: 0.11860450330163401, 4.4: 0.3132510422627319, 6.3: 0.07723643696013516, 7.8: 0.02946946783291098, 5.9: 0.10265039011053889, 8.6: 0.016485462819150386, 4.6: 0.2668192593803646, 5.1: 0.18283422799894639, 6.4: 0.0723452955121393, 5.6: 0.127156053298455, 6.9: 0.052817061318655364, 8.4: 0.019455570996484917, 6.1: 0.08878080238335286, 7.4: 0.03823446597091656, 9.6: 0.005022843492556564, 7.9: 0.027521185863375024, 9.9: 0.0018983260215991353, 5.4: 0.14694769158106033, 9.8: 0.0030200641252713517, 8.8: 0.014064870069120865, 8.9: 0.012734225274076496, 8.7: 0.015354641815853293, 9.1: 0.010636075460730084, 5.5: 0.13670672225401237, 9.2: 0.00935992806343497, 4.8: 0.22881640734988237, 4.0: 0.43314077586128596, 3.9: 0.469504164509478, 7.1: 0.0467814745179251, 5.8: 0.1104662252377449, 3.7: 0.5548380064851903, 7.5: 0.03590016076732336}

#average speed of ball
# average_speed_ball = 22.35
average_speed_ball = 33.5
# average distance covered by a player in 1 sec
average_distance_per_frame= 2.86/5.0 # meters 5 frames in 1 sec
average_speed_player = 2.86
#maximum speed of players
max_speed_player=10.0

#coefficient for goalchace,gain,pass advantages
weight_coefficient=[489,1, 975, 572]
#max values of gain,pass advantage,goal chance,
max_gain,max_goalChance,max_passAdvantage,max_risk=10.0,100.0,2.0,12620.0

# wxGUI
GUI_FILE_DIALOG_DIRECTORY=''
GUI_TITLE = "Sport Analytics Tool - IDEA Lab"
BITMAP_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gui/source/bitmaps')


# Match object types
OBJECT_TYPES = {
    -1: "Unknown object",
    0: "Home Team Player",
    1: "Away Team Player",
    2: "Referee",
    3: "Home Team Goalkeeper",
    4: "Away Team Goalkeeper",
    6: "The other referees",
    7: "The other referees",
    8: "The other referees",
    9: "The other referees"
}


# running distance speed filter
SPEED_THRESHOLD = 2.6  # 13m/s
# additional value, added to the result of speed for visualisation purposes
SPEED_ADDER = 4


# radius of visual player in CircleStyle
VISUAL_PLAYER_RADIUS = 12
# text of jersey number for visual players
VISUAL_PLAYER_JS_SIZE = 10

# default acceleration value for visual_players
DEFAULT_ACCELERATION = average_speed_player