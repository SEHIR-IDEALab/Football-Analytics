# coding=utf-8
import time as tm
import os
from src.sentio.Parameters import DATA_BASE_DIR
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


    reader = JSONreader(os.path.join(DATA_BASE_DIR, 'output/sentio_data.json'))
    game_instances, slider_mapping = reader.parse()

    # writer = Writer(game_instances, slider_mapping)
    # writer.createFileAsXML()
    # writer.createFileAsJSON()


    # for i in parser.game_instances:
    #     print i, parser.game_instances[i]

    # game_events = file_io.getGameEvents()
    # for event_time in sorted(game_events.keys()):
    #     temp_game_event = game_events.get(event_time)
    #     print temp_game_event.isPassEvent()


    #q = file_io.getCoordinateData()
    #file_io.getCombinedEventData()
    # file_io.getCoordinateData()

    #for definedPass in sentio.getEventData():
    # #    print definedPass
    #



    match = Match(reader)
    match.visualizeMatch()
    #







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


