from collections import OrderedDict
from src.sentio import Parameters
from src.sentio.file_io.reader import tree
from src.sentio.object.Team import Team
from src.sentio.object.Teams import Teams


__author__ = 'emrullah'



class ReaderBase:
    def __init__(self, file_path):
        self.file_path = file_path

        self.game_instances = tree()
        self.slider_mapping = OrderedDict()


    def parse(self):
        pass


    def computeHalfTimeIntervals(self):
        pass


    @staticmethod
    def mapIDToPlayers(players):
        q = {}
        for player in players:
            q[player.object_id] = player
        return q


    @staticmethod
    def divideIntoTeams(players, visual=False):
        home_team_players, away_team_players, referees, unknowns = {}, {}, {}, {}

        for player in players:
            if visual:
                temp_player = player.player
                temp_player.set_position(player.get_position())
                player = temp_player

            if player.isHomeTeamPlayer(): home_team_players[player.getJerseyNumber()] = player
            elif player.isAwayTeamPlayer(): away_team_players[player.getJerseyNumber()] = player
            elif player.isReferee(): referees[player.getJerseyNumber()] = player
            else: unknowns[player.getJerseyNumber()] = player

        return Teams(Team("home", home_team_players), Team("away", away_team_players),
                     Team("referee", referees), Team("unknown", unknowns))


    @staticmethod
    def divideIntoVisualTeams(players):
        home_team_players, away_team_players, referees, unknowns = \
            OrderedDict(), OrderedDict(), OrderedDict(), OrderedDict()

        for visual_player in players:
            player = visual_player.player
            if player.isHomeTeamPlayer(): home_team_players[player.object_id] = visual_player
            elif player.isAwayTeamPlayer(): away_team_players[player.object_id] = visual_player
            elif player.isReferee(): referees[player.object_id] = visual_player
            else: unknowns[player.object_id] = visual_player

        return Teams(Team("home", home_team_players), Team("away", away_team_players),
                     Team("referee", referees), Team("unknown", unknowns))


    def idToPlayer(self, player_id, teams):
        if player_id is None:
            return None

        for player in teams.getPlayers():
            if player.object_id == player_id:
                return player
        return None


    @staticmethod
    def idPlayersToTeamPlayers(idPlayers):
        home_team_players, away_team_players, referees, unknowns = \
            OrderedDict(), OrderedDict(), OrderedDict(), OrderedDict()

        for id in idPlayers:
            player = idPlayers[id]
            if player.isHomeTeamPlayer(): home_team_players[player.jersey_number] = player
            elif player.isAwayTeamPlayer(): away_team_players[player.jersey_number] = player
            elif player.isReferee(): referees[player.jersey_number] = player
            else: unknowns[player.jersey_number] = player

        return Teams(Team("home", home_team_players), Team("away", away_team_players),
                     Team("referee", referees), Team("unknown", unknowns))



    @staticmethod
    def getPlayerIn(p_player, teams):
        own_team = None
        if p_player.isHomeTeamPlayer(): own_team = teams.home_team
        elif p_player.isAwayTeamPlayer(): own_team = teams.away_team
        return own_team.getTeamPlayersWithJS().get(p_player.getJerseyNumber())


    @staticmethod
    def convertEventPlayerToCoordinatePlayer(event_player, teams):
        if event_player.getTeamName() == Parameters.HOME_TEAM_NAME: own_team = teams.home_team
        else: own_team = teams.away_team

        for player in own_team.getTeamPlayers():
            if player.getJerseyNumber() == event_player.getJerseyNumber():
                player.team_name = event_player.team_name
                return player


    def __str__(self):
        pass