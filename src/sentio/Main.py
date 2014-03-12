# coding=utf-8
import time
from src.sentio.Match import Match
from src.sentio.Sentio import Sentio

__author__ = 'emrullah'

def main():
    start = time.time()
    print "sasd"


    sentio = Sentio()
    sentio.parseSentioData()

    match = Match(sentio)
    match.visualizeMatch()


    # match.identifyObjects()
    # # match.compute_someEvents()
    # q = match.getHomeTeam().getTeamPlayers()
    # for i in q:
    #     player = q[i]
    #     print player.getSpeedOfPlayer_atAllPoints()
    #     break


    # player.getTeamName(), player.get_minMaxOfHalf_forPlayer(), player.getSpeedOfPlayer_atAllPoints()

    #
    #
    # match.identifyObjects()
    # q = match.getHomeTeam().getTeamPlayers()
    #
    # for i in q:
    #     print q[i].getTeamName(), q[i].getJerseyNumber(), q[i].compute_runningDistance(), \
    #         q[i].compute_runningDistance_withGameStopFilter()
    #     # #print q[i].getJerseyNumber(), q[i].drawHeatMap()
    #     #
    #









    end = time.time()
    print
    print end - start

if __name__ == "__main__":
    main()


