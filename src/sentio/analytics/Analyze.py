from src.sentio.Parameters import \
    FOOTBALL_FIELD_MIN_X, FOOTBALL_FIELD_MIN_Y, FOOTBALL_FIELD_MAX_X, FOOTBALL_FIELD_MAX_Y, \
    GOALPOST_MIN_Y, GOALPOST_MAX_Y, GOALPOST_MAX_X, GOALPOST_MIN_X
from src.sentio.object.PlayerBase import PlayerBase

__author__ = 'emrullah'


class Analyze:

    def __init__(self):
        pass


    @staticmethod
    def detectGoalKeeperWithPositions(p1, teams):
        if Analyze.isOpponentGoalKeeperLocationLeft(p1, teams): goal_keeper_x = GOALPOST_MIN_X
        else: goal_keeper_x = GOALPOST_MAX_X

        if p1.getY() < GOALPOST_MIN_Y: goal_keeper_y = GOALPOST_MIN_Y
        elif p1.getY() > GOALPOST_MAX_Y: goal_keeper_y = GOALPOST_MAX_Y
        else: goal_keeper_y = p1.getY()

        goal_keeper = PlayerBase()
        goal_keeper.set_position((goal_keeper_x, goal_keeper_y))
        goal_keeper.setJerseyNumber("goal_keeper")
        return goal_keeper


    @staticmethod
    def isOpponentGoalKeeperLocationLeft(p1, teams):
        if p1.isHomeTeamPlayer():
            own_goal_keeper = teams.home_team.getGoalKeeper()
            opponent_goal_keeper = teams.away_team.getGoalKeeper()
        else:
            own_goal_keeper = teams.away_team.getGoalKeeper()
            opponent_goal_keeper = teams.home_team.getGoalKeeper()

        return own_goal_keeper.getX() > opponent_goal_keeper.getX()


    @staticmethod
    def isInField(p1):
        return FOOTBALL_FIELD_MIN_X <= p1.getX() <= FOOTBALL_FIELD_MAX_X and \
               FOOTBALL_FIELD_MIN_Y <= p1.getY() <= FOOTBALL_FIELD_MAX_Y


    @staticmethod
    def isSuccessfulPass(p1, p2):
        return p1.getTypeName() == p2.getTypeName()


    @staticmethod
    def isBetween(p1, p3, p2):
        return p1.getX() <= p3.getX() <= p2.getX() or \
               p2.getX() <= p3.getX() <= p1.getX()


    def __str__(self):
        pass