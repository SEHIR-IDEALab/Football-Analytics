# coding=utf-8
import time as tm
from src.sentio.Match import Match
from src.sentio.Sentio import Sentio

__author__ = 'emrullah'

def main():
    start = tm.time()


    sentio = Sentio()
    sentio.parseSentioData()

    match = Match(sentio)
    # match.identifyObjects()
    # match.compute_someEvents()
    # q = match.getHomeTeam().getTeamPlayers()
    # print "js, ball_time, time_played"
    # for i in q:
    #     player = q[i]
    #     print player.getJerseyNumber(), player.get_ballOwnershipTime(), player.getTimeInterval_played()


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


