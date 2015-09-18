import wx
from src.sentio import Parameters

from src.sentio.Time import Time
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


    def computeEventStats(self):
        pre_game_instance = None
        for game_instance in self.sentio.game_instances.getAllInstances():
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


    def buildMatchObjects(self):
        q = {}, {}, {}, {}  ## home_team, away_team, referees, unknowns
        for game_instance in self.sentio.game_instances.getAllInstances():
            teams = ReaderBase.divideIntoTeams(game_instance.players)
            for team_index, team in enumerate(teams.getTeams()):
                for player in team.getTeamPlayers():
                    temp_team = q[team_index]
                    if player.jersey_number in temp_team:
                        temp_player = temp_team[player.jersey_number]
                        temp_player.appendNewCoordInfo(game_instance.time, player.get_position())
                    else:
                        temp_team[player.jersey_number] = Player(game_instance.time, player.raw_data)

        home_team, away_team, referees, unknowns = q
        self.teams = Teams(
            Team(Parameters.HOME_TEAM_NAME, home_team),
            Team(Parameters.AWAY_TEAM_NAME, away_team),
            Team(Parameters.REFEREES_TEAM_NAME, referees),
            Team(Parameters.UNKNOWNS_TEAM_NAME, unknowns)
        )


    def makeClassification(self, time_info, objects_coord_info, game_stop):
        types = [[0,3], [1,4], [2,6,7,8,9], [-1]]
        for player_coord_info in objects_coord_info:
            object_type, jersey_number = int(player_coord_info[0]), int(player_coord_info[2])
            for index, object_class in enumerate([self.homeTeamPlayers, self.awayTeamPlayers, self.referees, self.unknownObjects]):
                if object_type in types[index]:
                    if jersey_number in object_class:
                        object_class[jersey_number].appendNewCoordInfo(time_info, player_coord_info)
                    else:
                        object_class[jersey_number] = Player(time_info, player_coord_info)
                        player = object_class[jersey_number]
                        player.set_gameStopTimeInterval(game_stop)


    def get_timeInterval_ofGameStop(self):
        game_stop_time_intervals = dict()
        time = Time()
        time.set_minMaxOfHalf(self.get_minMaxOfHalf(self.sentio.getCoordinateData()))
        q = self.sentio.getEventData_byTime()
        game_stop_time_intervals = self.checkForGameStopEvent(time, game_stop_time_intervals, q)
        while True:
            try:
                next_time = time.next()
                #print next_time.half, next_time.minute, next_time.second, next_time.mili_second
                game_stop_time_intervals = self.checkForGameStopEvent(next_time, game_stop_time_intervals, q)
            except KeyError:
                break
        return game_stop_time_intervals


    def checkForGameStopEvent(self, time, game_stop_time_intervals, q):
        try:
            instant_events = q[time.half][time.minute][time.second]
            for instant_event in instant_events:
                teamName, js, eventID = instant_event
                if eventID == 2:
                    game_stop_time_intervals = self.append_newEventTimeIntervals(game_stop_time_intervals, time)
        except KeyError:
            back_time = time.back()
            back_half, back_minute, back_second, back_millisec = back_time.half, back_time.minute, back_time.second, back_time.millisecond
            try:
                checkIfInside = game_stop_time_intervals[back_half][back_minute][back_second][back_millisec]
                current_time = time.next()
                game_stop_time_intervals = self.append_newEventTimeIntervals(game_stop_time_intervals, current_time)
            except KeyError:
                pass
        return game_stop_time_intervals


    def visualizeMatch(self):
        app = wx.App()
        app.frame = wxVisualization(self.sentio)
        app.frame.Show()
        app.MainLoop()


    def __str__(self):
        pass
