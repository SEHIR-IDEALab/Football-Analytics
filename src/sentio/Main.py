# coding=utf-8
import time as tm
from src.sentio.Match import Match
from src.sentio.Sentio import Sentio
from src.sentio.Time import Time

__author__ = 'emrullah'

def main():
    start = tm.time()


    sentio = Sentio()
    sentio.parseSentioData()

    match = Match(sentio)
    match.visualizeMatch()

    def get_currentEventData(half, minute, second, milisec):
        try:
            eventData_current = sentio.getEventData_byTime()[half][minute][second]
            return eventData_current
        except KeyError:
            time = Time(half, minute, second, milisec)
            time.set_minMaxOfHalf(match.get_minMaxOfHalf())
            back_time = time.back()
            #print back_time.half, back_time.minute, back_time.second, back_time.mili_second
            return get_currentEventData(back_time.half, back_time.minute, back_time.second, back_time.mili_second)


    def getBallOwner_byTime(half, minute, second, mili_second):
        q = sentio.getCoordinateData_byTime()
        current_coord_info = q[half][minute][second][mili_second]
        current_event_info = get_currentEventData(half, minute, second, mili_second)
        print half, minute, second, mili_second
        print current_event_info
        print current_coord_info
        time = Time(half, minute, second, mili_second)
        time.set_minMaxOfHalf(match.get_minMaxOfHalf())
        next_time = time.next()
        next_coord_info = q[next_time.half][next_time.minute][next_time.second][next_time.mili_second]
        print next_time.half, next_time.minute, next_time.second, next_time.mili_second
        print next_coord_info

#    getBallOwner_byTime(1,0,0,0)



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









    end = tm.time()
    print
    print end - start

if __name__ == "__main__":
    main()


