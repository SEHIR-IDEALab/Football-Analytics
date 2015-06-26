# coding=utf-8
__author__ = 'emrullah'

# team names
HOME_TEAM_NAME = "Fenerbahçe"
AWAY_TEAM_NAME = "Galatasaray"

# min-max for each half
INITIAL_HALF_MIN_MAX = {1: ((0,0,0), (44,59,8)), 2: ((45,0,0), (89,59,8))}
HALF_MIN_MAX = {1: ((0, 0, 0), (48, 0, 8)), 2: ((45, 0, 8), (94, 19, 6))}

# football field
FOOTBALL_FIELD_MIN_X = 0.0
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
GOAL_COEFFICIENT = 1000

# debug mode
IS_DEBUG_MODE_ON = False

# radius of pass_source
PASS_SOURCE_RADIUS = 1.5

# radius coefficient of pass target
PASS_TARGET_RADIUS_COEFFICIENT = 4.0
# radius of back risk area
SOURCE_ANGLE=60.0

#probability of player run at specific speed
Coefficient={8:0.01,0:0.01}
