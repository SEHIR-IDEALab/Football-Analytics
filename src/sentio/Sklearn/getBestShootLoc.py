__author__ = 'aliuzun'
import math
from src.sentio.Parameters import *
from src.sentio.gui.RiskRange import RiskRange
from src.sentio.object.PlayerBase import PlayerBase
from src.sentio.pass_evaluate.Pass import *
import matplotlib.pyplot as plt
average_distance_per_frame=1

# def goalChance(p1):
#     goalChances=[]
#     if Pass.isOpponentGoalKeeperLocationLeft(p1): goal_keeper_x = GOALPOST_MIN_X
#
#     else: goal_keeper_x = GOALPOST_MAX_X
#
#     if p1.getY() < GOALPOST_MIN_Y: goal_keeper_y = GOALPOST_MIN_Y
#     elif p1.getY() > GOALPOST_MAX_Y: goal_keeper_y = GOALPOST_MAX_Y
#     else: goal_keeper_y = p1.getY()
#
#
#     goal_keeper = PlayerBase()
#     goal_keeper.set_position((goal_keeper_x, goal_keeper_y))
#     goal_keeper.setJerseyNumber("goal_keeper")
#
#
#
#     player_list, initilaInfo = get_players_in_gcr(p1)
#     try:
#         ln = min(getLN(p1,player_list,(goal_keeper_x,goal_keeper_y)))
#     except  ValueError:
#         ln=1
#     ln = (1 if ln == 0 else ln)
#
#     for i in range(ln):
#         d1 = math.sqrt(math.pow(goal_keeper_x - p1.getX(), 2) + math.pow(goal_keeper_y - p1.getY(), 2))
#         angle = math.atan2(math.fabs(p1.getY() - goal_keeper_y), math.fabs(p1.getX() - goal_keeper_x)) * 180 / math.pi
#         angle = math.fabs(90 - angle)
#         q = Pass.overallRisk(p1, goal_keeper, goal_keeper=False)
#
#         # q = (1 if q == 0 else q)
#         d1 = (0.1 if d1 == 0 else d1)
#
#         goalChances.append((GOALPOST_LENGTH / d1) * (min(angle, (180 - angle)) / 90.) * (1. / (1 + q)) * GOAL_COEFFICIENT)
#         getFutureCoordinates(p1,player_list,(goal_keeper_x,goal_keeper_y))
#
#     p1.set_position(initilaInfo[p1])
#     for p2 in player_list:
#         p2.set_position(initilaInfo[p2])
#
#     return max(goalChances)

def drawFigure(p1,player_list,Gxy,ln=30):

    goal_keeper_x,goal_keeper_y=Gxy
    # try:
    #     ln = min(getLN(p1,player_list,(goal_keeper_x,goal_keeper_y)))
    # except  ValueError:
    #     ln=1
    # ln = (1 if ln == 0 else ln)

    scat_xr,scat_yr=[],[]
    s1x,s1y=[],[]
    hm= plt.figure(figsize=(15,9))

    plt.scatter(Gxy[0],Gxy[1],c="b")

    for i in range(1,ln+1):

        bp,ot=getFutureCoordinates(p1,player_list,Gxy,i)
        s1x.append(bp[0])
        s1y.append(bp[1])
        for x,y in ot:
            scat_xr.append(x)
            scat_yr.append(y)

    plt.scatter(scat_xr,scat_yr,s=30,c='red',label = "Unsuccessful Pass")
    plt.scatter(s1x,s1y,s=30,c='blue',label = "ball owner")
    im2=plt.imread('/Users/aliuzun/PycharmProjects/futbol-data-analysis/src/sentio/Sklearn/srcc/background.png',0)

    hm = plt.imshow(im2, extent=[-2.0, 107.0, 72.0, 0.0], aspect="auto")

    plt.show()



#-----------------

# def get_players_in_gcr(p1): # return the list of player has affect on goalchance
#     players_list=[]
#     initialInfo={}
#
#     own_goal_keeper = Pass.teams.home_team.getGoalKeeper()
#     opponent_goal_keeper = Pass.teams.away_team.getGoalKeeper()
#     x_home, x_away= own_goal_keeper.getX(),opponent_goal_keeper.getX()
#
#     if p1.isHomeTeamPlayer():
#         team=Pass.teams.away_team
#         min_x=min(p1.get_position()[0],x_away)
#         max_x=max(p1.get_position()[0],x_away)
#     else:
#         team=Pass.teams.home_team
#         min_x=min(p1.get_position()[0],x_home)
#         max_x=max(p1.get_position()[0],x_home)
#     # player_list=team.getJerseyNumbersOfPlayers()
#     player_list=team.getTeamPlayers()
#
#     initialInfo[p1]=(p1.getX(),p1.getY())
#
#     for player1 in player_list:
#         js,x,y=player1.getJerseyNumber(),player1.getX(),player1.getY()
#         if (x >= min_x) and (x <= max_x) and ((x,y)!=(team.getGoalKeeper().getX(), team.getGoalKeeper().getY())):
#             players_list.append(player1)
#             initialInfo[player1]=(player1.getX(),player1.getY())
#
#     return (players_list,initialInfo)


#-----------------

# def getLN(p1,p2s,Gxy): # give the number of times next position will be got
#     dists=list()
#     x1, y1 = p1
#     x3, y3 = Gxy
#
#     Q1 = math.degrees(math.atan((y3-y1)/(x3-x1))) # Q1 is the angle of p1 - goalkeeper line
#     try: slope = (y3 - y1) / (x3 - x1) # zero devision error gives
#     except ZeroDivisionError: slope = 1000 # might be change
#     a,b,c = slope,-1,( ( slope * (-x1) ) + y1 )
#
#     for p2 in p2s:
#
#         x2, y2 = p2
#         angle1 = math.degrees(math.atan((y2-y1)/(x2-x1))) # the angle of p1-p2 line
#         alpha_p1 = 2*math.fabs(Q1-angle1) # the angle with p1's direction and p1-p2 line
#         d2 = math.fabs(a * x2 + b * y2 + c) / math.sqrt(math.pow(a, 2) + math.pow(b, 2))
#
#         if alpha_p1 > 180:
#             # alpha_p1 = alpha_p1 - 180
#             t=(d2/average_speed_player)
#         else:
#             alpha_p1 = math.radians(alpha_p1)
#             t=(d2/average_speed_player)*math.sin(alpha_p1)
#
#         dists.append(int(t))
#     return dists

def getPointLocation(p1,p2,Gxy):
    x3,y3=Gxy
    x1,y1=p1
    x2,y2=p2

    m=(y3-y1)/(x3-x1) #slope
    a=y1-m*x1 # constant
    tmp_val=m*x2+a

    if y2 > tmp_val:   return -1
    elif y2 < tmp_val: return 1
    else:              return 0



def getFutureCoordinates(p1,p2s,Gxy,t):
    x1, y1 = p1
    x3, y3 = Gxy

    Q1 = math.degrees(math.atan((y3-y1)/(x3-x1))) # Q1 is the angle of p1 - goalkeeper line

    if x1 > x3:
        x1_p,y1_p  = x1 - t*(average_distance_per_frame)*round(math.cos(math.radians(Q1)),2) ,\
                   y1 - t*(average_distance_per_frame)*round(math.sin(math.radians(Q1)),2)
    else:
        x1_p,y1_p  = x1 + t*(average_distance_per_frame)*round(math.cos(math.radians(Q1)),2) ,\
                       y1 + t*(average_distance_per_frame)*round(math.sin(math.radians(Q1)),2)

    ## set the new coordinates
    # p1.set_position((x1_p,y1_p))

    cords=[]
    for p2 in p2s:
        wherePoint=getPointLocation(p1,p2,Gxy)
        x2, y2 = p2
        try:
            angle1 = math.degrees(math.atan((y2-y1)/(x2-x1))) # the angle of p1-p2 line
        except:
            ZeroDivisionError
            angle1=90.0
        alpha_p1 = math.fabs(Q1-angle1) # the angle with p1's direction and p1-p2 line

        if wherePoint == 1: # above the line
            if x1 > x3:
                Q2 = Q1 + 2*alpha_p1
                x2_p,y2_p  = x2 + t*(average_distance_per_frame)*round(math.cos(math.radians(Q2)),2) ,\
                           y2 + t*(average_distance_per_frame)*round(math.sin(math.radians(Q2)),2)
            else:
                Q2 = -Q1 + 2*alpha_p1
                x2_p,y2_p  = x2 - t*(average_distance_per_frame)*round(math.cos(math.radians(-Q2)),2) ,\
                           y2 - t*(average_distance_per_frame)*round(math.sin(math.radians(-Q2)),2)

        elif wherePoint == -1: # below the line
            if x1 > x3:
                Q2 = Q1 + (180.0 - 2*alpha_p1 )
                x2_p,y2_p  = x2 - t*(average_distance_per_frame)*round(math.cos(math.radians(Q2)),2) ,\
                           y2 - t*(average_distance_per_frame)*round(math.sin(math.radians(Q2)),2)
            else:
                Q2 = Q1 + 2*alpha_p1
                x2_p,y2_p  = x2 - t*(average_distance_per_frame)*round(math.cos(math.radians(Q2)),2) ,\
                           y2 - t*(average_distance_per_frame)*round(math.sin(math.radians(Q2)),2)
        else:
            if x1 > x3:
                #Q2==Q1
                x2_p,y2_p  = x2 - t*(average_distance_per_frame)*round(math.cos(math.radians(Q1)),2) ,\
                           y2 - t*(average_distance_per_frame)*round(math.sin(math.radians(Q1)),2)
            else:
                #Q2==Q1
                x2_p,y2_p  = x2 + t*(average_distance_per_frame)*round(math.cos(math.radians(Q1)),2) ,\
                           y2 + t*(average_distance_per_frame)*round(math.sin(math.radians(Q1)),2)

        cords.append((x2_p,y2_p))

    return ([x1_p,y1_p],cords)
       ## set the new coordinates
        # p2.set_position((x2_p,y2_p))

        

print drawFigure((60.0,55.0),[(70.0,35.0),(90.0,65.0),(65.0,60.0)],(100.0,35.0))