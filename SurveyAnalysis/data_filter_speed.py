__author__ = 'mehmetinan'

import math
import json
import csv


coor_file = []
speedlist = []
coordata = open("of-mu.txt","r").readlines()
file = open("player_speed.txt","w")
filter_minutes = [0,1,2,3,4,5,30,31,32,33,34,35,60,61,62,63,64,65,80,81,82,83,84,85]

for line in coordata:
    #coor_file.append(json.loads(line.replace("'", "\"")))
    gamedata = json.loads(line.replace("'", "\""))
    timestamp = gamedata["ts"]
    minute = ((timestamp-1878448)/100)/600
    player_speed = [minute]
    playerdata = gamedata["data"]
    if minute in filter_minutes:
        for player in playerdata:
            player_speed.append(player["id"])
            player_speed.append(player["spd"])

        speedlist.append(player_speed)

for line in speedlist:
        ln = ("%d\t%d\t%f\t%d\t%f\t%d\t%f\t%d\t%f\t%d\t%f\t%d\t%f\t%d\t%f\t%d\t%f\t"
              "%d\t%f\t%d\t%f\t%d\t%f\t%d\t%f\t%d\t%f\t%d\t%f\t%d\t%f\t%d\t%f\t%d\t"
              "%f\t%d\t%f\t%d\t%f\t%d\t%f\t%d\t%f\t%d\t%f\n") % (line[0],line[1],line[2],line[3],line[4],
                                                                                     line[5],line[6],line[7],line[8],line[9],
                                                                                     line[10],line[11],line[12],line[13],line[14],
                                                                                     line[15],line[16],line[17],line[18],line[19]
                                                                                         ,line[20],line[21],line[22],line[23],line[24]
                                                                                         ,line[25],line[26],line[27],line[28],line[29]
                                                                                         ,line[30],line[31],line[32],line[33],line[34]
                                                                                         ,line[35],line[36],line[37],line[38],line[39]
                                                                                         ,line[40],line[41],line[42],line[43],line[44])
        file.write(ln)