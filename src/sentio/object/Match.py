import wx
from src.sentio import Parameters
from src.sentio.file_io.reader import tree
from src.sentio.file_io.reader.ReaderBase import ReaderBase
from src.sentio.gui.wxVisualization import wxVisualization
from src.sentio.object.Player import Player
from src.sentio.object.Team import Team
from src.sentio.object.Teams import Teams


__author__ = 'emrullah'

class Match(object):

    def __init__(self, sentio):

        self.sentio = sentio
        self.teams = None


    def getHomeTeam(self):
        return self.teams.home_team


    def getAwayTeam(self):
        return self.teams.away_team


    def getReferees(self):
        return self.teams.referees


    def getUnknownObjects(self):
        return self.teams.unknowns


    def buildMatchObjects(self):
        game_stop_time_intervals = self.getGameStopTimeIntervals()
        q = {}, {}, {}, {}  ## home_team, away_team, referees, unknowns
        for game_instance in self.sentio.game_instances.getAllInstances():
            try:
                teams = ReaderBase.divideIntoTeams(game_instance.players)
                for team_index, team in enumerate(teams.getTeams()):
                    temp_team = q[team_index]
                    for player in team.getTeamPlayers():
                        if player.jersey_number in temp_team:
                            temp_player = temp_team[player.jersey_number]
                            temp_player.appendNewCoordInfo(game_instance.time, player.get_position())
                        else:
                            temp_team[player.jersey_number] = Player(game_instance.time, player.raw_data)
                            temp_team[player.jersey_number].set_gameStopTimeInterval(game_stop_time_intervals)
            except:
                print "game instance is missing", game_instance
        home_team, away_team, referees, unknowns = q
        self.teams = Teams(
            Team(Parameters.HOME_TEAM_NAME, home_team),
            Team(Parameters.AWAY_TEAM_NAME, away_team),
            Team(Parameters.REFEREES_TEAM_NAME, referees),
            Team(Parameters.UNKNOWNS_TEAM_NAME, unknowns)
        )


    def computeEventStats(self):
        pre_game_instance = None
        for game_instance in self.sentio.game_instances.getAllInstances():
            try:
                if game_instance.event and pre_game_instance:
                    event = game_instance.event
                    pre_event = pre_game_instance.event
                    if event.player and (event.player.getTypeName() != pre_event.player.getTypeName() or
                            event.player.jersey_number != pre_event.player.jersey_number or pre_event.event_id == 1):
                        own_time = game_instance.time.milliseconds - pre_game_instance.time.milliseconds
                        if pre_event.player.isHomeTeamPlayer():
                            self.teams.home_team.team_players[pre_event.player.jersey_number].add_ballOwnershipTime(own_time)
                        elif pre_event.player.isAwayTeamPlayer():
                            self.teams.away_team.team_players[pre_event.player.jersey_number].add_ballOwnershipTime(own_time)

                if game_instance.event and game_instance.event.player:
                    pre_game_instance = game_instance

                if game_instance.event and game_instance.event.isPassEvent():
                    pass_source = game_instance.event.pass_event.pass_source
                    pass_target = game_instance.event.pass_event.pass_target

                    if pass_source.getTypeName() != pass_target.getTypeName():
                        if pass_target.isHomeTeamPlayer():
                            self.teams.home_team.team_players[pass_target.jersey_number].add_ballSteal()
                            self.teams.away_team.team_players[pass_source.jersey_number].add_ballLose()
                        elif pass_target.isAwayTeamPlayer():
                            self.teams.away_team.team_players[pass_target.jersey_number].add_ballSteal()
                            self.teams.home_team.team_players[pass_source.jersey_number].add_ballLose()
                    else:
                        if pass_target.isHomeTeamPlayer():
                            self.teams.home_team.team_players[pass_source.jersey_number].add_ballPass()
                        elif pass_target.isAwayTeamPlayer():
                            self.teams.away_team.team_players[pass_source.jersey_number].add_ballPass()
            except:
                print "game instance is missing", game_instance


    def getGameEvents(self):
        game_events = []
        for game_instance in self.sentio.game_instances.getAllInstances():
            if game_instance.event:
                game_events.append(game_instance.event)
        return game_events


    def getGameStopTimeIntervals(self):
        intervals = tree()
        pre_game_event = None
        for game_instance in self.sentio.game_instances.getAllInstances():
            try:
                if game_instance.event:
                    pre_game_event = game_instance.event
                    if game_instance.event.event_name == "GameStop":
                        intervals[game_instance.time.half][game_instance.time.milliseconds] = True
                else:
                    if pre_game_event and pre_game_event.event_name == "GameStop":
                        intervals[game_instance.time.half][game_instance.time.milliseconds] = True
            except:
                print "game instance is missing", game_instance
        return intervals


    def visualizeMatch(self):
        app = wx.App()
        app.frame = wxVisualization(self)
        app.frame.Show()
        app.MainLoop()


    def __str__(self):
        pass
