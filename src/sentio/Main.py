# coding=utf-8
import time as tm
from src.sentio.object.Match import Match
from src.sentio.parser.Parser import Parser


__author__ = 'emrullah'

def main():
    start = tm.time()


    parser = Parser()
    parser.parseSentioData()

    # game_events = parser.getGameEvents()
    # for event_time in sorted(game_events.keys()):
    #     temp_game_event = game_events.get(event_time)
    #     print temp_game_event.isPassEvent()


    #q = parser.getCoordinateData()
    #parser.getCombinedEventData()
    # parser.getCoordinateData()

    #for definedPass in sentio.getEventData():
    # #    print definedPass
    #


    match = Match(parser)
    match.visualizeMatch()








    #print match.getMatchScore_forGivenTime(2, 75, 56, 0)

#    getBallOwner_byTime(1,0,0,0)

    #
    #
    # match.identifyObjects()
    # #match.compute_someEvents()
    # q = match.getHomeTeam().getTeamPlayers()
    # for i in q:
    #     player = q[i]
    #     print player.compute_runningDistance_withGameStopAndSpeedFilter()
    # #

    # match.identifyObjects()
    # q = match.getHomeTeam().getTeamPlayers()
    #
    # for i in q:
    #     print q[i].getTeamName(), q[i].getJerseyNumber(), q[i].compute_runningDistance(), \
    #         q[i].compute_runningDistance_withGameStopFilter()
        # #print q[i].getJerseyNumber(), q[i].drawHeatMap()
        #
    #









    end = tm.time()
    print
    print end - start

if __name__ == "__main__":
    main()


