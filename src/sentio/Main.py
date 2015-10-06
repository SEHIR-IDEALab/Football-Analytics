# coding=utf-8
import time as tm
import os
from src.sentio.Parameters import DATA_BASE_DIR
from src.sentio.Time import Time
from src.sentio.file_io.Parser import Parser
from src.sentio.file_io.Writer import Writer
from src.sentio.file_io.reader.JSONreader import JSONreader
from src.sentio.file_io.reader.XMLreader import XMLreader
from src.sentio.object.Match import Match


__author__ = 'emrullah'

def main():
    start = tm.time()

    # coord_data = os.path.join(DATA_BASE_DIR, 'input/GS_FB_Sentio.txt')
    # event_data = os.path.join(DATA_BASE_DIR, 'input/GS_FB_Event.txt')


    reader = XMLreader(os.path.join(DATA_BASE_DIR, 'output/sentio_data_new.xml'))
    game_instances, slider_mapping = reader.parse()

    # count = 0
    # for game_instance in game_instances.getAllInstances():
    #     if game_instance.event:
    #         count += 1
    #         print game_instance.event
    # print count

    # writer = Writer(game_instances, slider_mapping)
    # writer.createFileAsXML()
    # writer.createFileAsJSON()



    # for game_instance in game_instances.getFirstHalfInstances():
    #     if game_instance.event and game_instance.event.isPassEvent():
    #         pass_event = game_instance.event.pass_event
    #         pass_source = pass_event.pass_source
    #         pass_target = pass_event.pass_target
    #         print game_instance.time.half, pass_source.get_position(), pass_target.get_position(), pass_event.isSuccessful()




    match = Match(reader)
    #
    # match.getGameEvents()
    # print match.computeGameStopTimeIntervals()

    # match.buildMatchObjects()
    # match.computeEventStats()
    #
    # team_players = match.getHomeTeam().getTeamPlayers()
    #
    # # for half in home_goal_keeper.coord_info:
    # #     for milliseconds in home_goal_keeper.coord_info[half]:
    # #         print half, milliseconds, home_goal_keeper.coord_info[half][milliseconds]
    #
    # print home_goal_keeper.computeRunningDistance()

    # for team_player in team_players:
    #     print "direction: ", team_player.calculateDirectionAtAllPoints()
        # print team_player.calculateSpeed(Time(1, 500))
        # print team_player.printStats()
        # print "without filter: ", team_player.computeRunningDistance()
        # print "with game_stop filter: ", team_player.computeRunningDistanceWithGameStopFilter()
        # print "with game_stop and speed filter: ", team_player.computeRunningDistanceWithGameStopAndSpeedFilter()
        # print "---------------------"
        # break


    match.visualizeMatch()






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


