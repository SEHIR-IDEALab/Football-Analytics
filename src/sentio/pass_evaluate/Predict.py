from src.sentio.object.PlayerBase import PlayerBase
from src.sentio.pass_evaluate.Pass import Pass

__author__ = 'doktoray'


class Predict:

    def __init__(self, effectiveness_score, pass_event, teams):
        self.effectiveness_score = effectiveness_score
        self.pass_event = pass_event
        self.teams = teams
        self.pas = Pass(teams)


    def getTargetWithBestPositionsFor(self, temp_pass_event):
        pass_target = temp_pass_event.getPassTarget()
        best_positions = pass_target.get_position()

        partial_range = 1
        step = 0.25
        best_effectiveness_score = -999999.9
        for temp_position_x in range(pass_target.getX() - partial_range, pass_target.getX() + partial_range, step):
            pass_target.setX(temp_position_x)
            for temp_position_y in range(pass_target.getY() - partial_range, pass_target.getY() + partial_range, step):
                pass_target.setY(temp_position_y)

                temp_effectiveness_score = self.pas.effectiveness(temp_pass_event.getPassSource(), pass_target)
                if temp_effectiveness_score > best_effectiveness_score:
                    best_effectiveness_score = temp_effectiveness_score

                    best_positions = temp_position_x, temp_position_y

        target_with_best_positions = PlayerBase((pass_target.object_type, pass_target.object_id,
                                                pass_target.jersey_number, pass_target.getX(), pass_target.getY()))
        target_with_best_positions.set_position(best_positions)
        return target_with_best_positions


    def getBestPassTarget(self):
        pass_target = self.pass_event.getPassTarget()

        if pass_target.isHomeTeamPlayer(): own_team = self.teams.home_team
        else: own_team = self.teams.away_team

        best_effectiveness_score = -999999.9
        best_pass_target = pass_target
        for target_player in own_team.getTeamPlayers():
            if self.pass_event.getPassSource().getJerseyNumber() != target_player.getJerseyNumber():
                temp_effectiveness_score = self.pas.effectiveness(self.pass_event.getPassSource(), target_player)
                if temp_effectiveness_score > best_effectiveness_score:
                    best_effectiveness_score = temp_effectiveness_score
                    best_pass_target = target_player
        return best_pass_target


    def getBestPassTargetWithBestPositions(self):
        pass_target = self.pass_event.getPassTarget()

        if pass_target.isHomeTeamPlayer(): own_team = self.teams.home_team
        else: own_team = self.teams.away_team

        best_target_with_best_positions = pass_target
        best_effectiveness_score = -999999.9
        for target_player in own_team.getTeamPlayers():
            if self.pass_event.getPassSource().getJerseyNumber() != target_player.getJerseyNumber():
                temp_pass_event = self.pass_event.setPassTarget(target_player)
                temp_target_with_best_positions = self.getTargetWithBestPositionsFor(temp_pass_event)
                temp_effectiveness_score = self.pas.effectiveness(self.pass_event.getPassSource(),
                                                                  temp_target_with_best_positions)
                if temp_effectiveness_score > best_effectiveness_score:
                    best_effectiveness_score = temp_effectiveness_score
                    best_target_with_best_positions = temp_target_with_best_positions
        return best_target_with_best_positions


    def __str__(self):
        pass
