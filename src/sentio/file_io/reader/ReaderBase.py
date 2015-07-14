from collections import OrderedDict
from src.sentio import Parameters
from src.sentio.object.PlayerBase import PlayerBase
from src.sentio.object.Team import Team
from src.sentio.object.Teams import Teams

__author__ = 'emrullah'






def convertDraggableToTeams(draggable_visual_teams):
    q = ({},{},{},{})
    for index, team in enumerate(draggable_visual_teams):
        for draggable_visual_player in team.values():
            player = draggable_visual_player.visual_player.player
            player.set_position(draggable_visual_player.visual_player.get_position())
            q[index][player.getJerseyNumber()] = player
    return Teams(Team("home", q[0]), Team("away", q[1]),
                 Team("referee", q[2]), Team("unknown", q[3]))




class ReaderBase:
    def __init__(self, file_path):
        self.file_path = file_path

        self.game_instances = OrderedDict()
        self.slider_mapping = OrderedDict()


    def parse(self):
        pass


    def computeHalfTimeIntervals(self):
        pass


    @staticmethod
    def divideIntoTeams(players):
        home_team_players, away_team_players, referees, unknowns = {}, {}, {}, {}

        for object_info in players:
            player = PlayerBase(object_info)
            if player.isHomeTeamPlayer(): home_team_players[player.getJerseyNumber()] = player
            elif player.isAwayTeamPlayer(): away_team_players[player.getJerseyNumber()] = player
            elif player.isReferee(): referees[player.getJerseyNumber()] = player
            else: unknowns[player.getJerseyNumber()] = player

        return Teams(Team("home", home_team_players), Team("away", away_team_players),
                     Team("referee", referees), Team("unknown", unknowns))


    def idToPlayer(self, player_id, teams):
        for player in teams.getPlayers():
            if player.object_id == player_id:
                return player
        return None


    @staticmethod
    def getPlayerIn(p_player, teams):
        own_team = None
        if p_player.isHomeTeamPlayer(): own_team = teams.home_team
        elif p_player.isAwayTeamPlayer(): own_team = teams.away_team
        return own_team.getTeamPlayersWithJS().get(p_player.getJerseyNumber())


    def convertEventPlayerToCoordinatePlayer(self, event_player, teams):
        if event_player.getTeamName() == Parameters.HOME_TEAM_NAME: own_team = teams.home_team
        else: own_team = teams.away_team

        for player in own_team.getTeamPlayers():
            if player.getJerseyNumber() == event_player.getJerseyNumber():
                player.team_name = event_player.team_name
                return player


    def get_ID_Explanation(self):
        a = dict()
        for line in self.event_data:
            id, explanation = int(line[5]), line[6]
            a[id] = explanation
        return a


    def __str__(self):
        pass