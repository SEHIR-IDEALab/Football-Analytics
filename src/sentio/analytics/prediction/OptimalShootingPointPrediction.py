import math
import operator
from src.sentio.Parameters import average_speed_player, average_distance_per_frame, GOALPOST_LENGTH
from src.sentio.analytics.Analyze import Analyze

__author__ = 'emrullah'


class OptimalShootingPointPrediction:

    def __init__(self, teams):
        self.teams = teams
        self.Qs={}


    def get_players_in_gcr(self, p1): # return the list of player has affect on goal chance
        players_list=[]
        initialInfo={}
        ball_ownerTeam = ("home" if p1.isHomeTeamPlayer()==True else "away")
        team = (self.teams.away_team if ball_ownerTeam=="home" else self.teams.home_team)
        home_Gkeeper = self.teams.home_team.getGoalKeeper()
        away_Gkeeper = self.teams.away_team.getGoalKeeper()
        goalKeepersPosition = {"away":home_Gkeeper.get_position(),"home":away_Gkeeper.get_position()}
        g = goalKeepersPosition[ball_ownerTeam] # coordinate of goalkeeper

        player_list=team.getTeamPlayers()

        initialInfo[p1]=p1.get_position()
        R1,R2 = min(p1.getX(),g[0]),max(p1.getX(),g[0])
        for player1 in player_list:
            js,x,y=player1.getJerseyNumber(),player1.getX(),player1.getY()
            if (R1 <= x) and (x <= R2) and (x,y) !=g :
                players_list.append(player1)
                initialInfo[player1]=(x,y)
        return (players_list,initialInfo,g)


    # def getLN(self, p1, p2s, Gxy): # give the number of times next position will be got
    #     dists=list()
    #     x1, y1 = p1.get_position()
    #     x3, y3 = Gxy
    #
    #     try: tmp_slope=(y3-y1)/(x3-x1)
    #     except ZeroDivisionError: tmp_slope=100
    #
    #     Q1 = math.degrees(math.atan(tmp_slope)) # Q1 is the angle of p1 - goalkeeper line
    #     try: slope = (y3 - y1) / (x3 - x1) # zero devision error gives
    #     except ZeroDivisionError: slope = 100 # might be change
    #     a,b,c = slope,-1,( ( slope * (-x1) ) + y1 )
    #
    #     for p2 in p2s:
    #
    #         x2, y2 = p2.get_position()
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
    #     print dists ##########################
    #     return dists


    def getPointLocation(self, p1, p2, Gxy):
        x3,y3=Gxy
        x1,y1=p1.get_position()
        x2,y2=p2.get_position()
        dx = (0.01 if (x3-x1) == 0 else (x3-x1))
        slope=(y3-y1)/dx
        a=y1-slope*x1 # constant
        tmp_val=slope*x2+a
        if y2 > tmp_val:   return -1
        elif y2 < tmp_val: return 1
        else:              return 0


    def getFutureCoordinates(self, p1, p2s, t,Gxy, Q1):
        x1, y1 = p1.get_position()
        x3, y3 = Gxy
        # t=4*t
        if x1 > x3:
            x1_p,y1_p  = x1 - t*(average_distance_per_frame)*round(math.cos(math.radians(Q1)),2) ,\
                       y1 - t*(average_distance_per_frame)*round(math.sin(math.radians(Q1)),2)
        else:
            x1_p,y1_p  = x1 + t*(average_distance_per_frame)*round(math.cos(math.radians(Q1)),2) ,\
                           y1 + t*(average_distance_per_frame)*round(math.sin(math.radians(Q1)),2)
        ## set the new coordinates
        cords=[]
        Q2=None
        for i in range(len(p2s)):
            p2=p2s[i]
            wherePoint=self.getPointLocation(p1,p2,Gxy)
            x2, y2 = p2.get_position()

            if i not in self.Qs:
                dx = (0.01 if (x2-x1) == 0 else (x2-x1))
                angle1 = math.degrees(math.atan((y2-y1)/dx))
                if angle1 <0: angle1+=360 # convert positive angle
                alpha_p1 = math.fabs((Q1-angle1)) # the angle with p1's direction and p1-p2 line

                if wherePoint ==1: # above the line

                    if y1 > y3:
                        if x1>x3: Q2 = Q1 + 2*alpha_p1

                        else: Q2 = Q1 - (180+2*alpha_p1)  # x3>=x1 ,alpha_p1 is negative

                    else:
                        if x1>x3: Q2 = Q1 - (180+2*alpha_p1)-180 #Q2 = 2*alpha_p1-math.fabs(Q1)

                        else: Q2 = 180-(Q1 - 2*alpha_p1)

                elif wherePoint ==-1: # below the line
                    if y1 > y3:
                        if x1>x3: Q2 = Q1 - 2*alpha_p1

                        else: Q2 = (Q1 - (180-2*alpha_p1)) -180 # x3>=x1 ,alpha_p1 is negative

                    else:
                        if x1>x3: Q2 = Q1-2*alpha_p1

                        else: Q2 = (Q1 + 2*alpha_p1-180)
                while Q2<0:
                    Q2+=360
                self.Qs[i]=Q2

            Q=self.Qs[i]
            x2_p,y2_p  = x2 + t*(average_distance_per_frame)*round(math.cos(math.radians(Q)),2) ,\
                        y2 + t*(average_distance_per_frame)*round(math.sin(math.radians(Q)),2)
            cords.append((x2_p,y2_p))
            # print p2.getJerseyNumber(),(x2,y2),"Q",Q

           # set the new coordinates
            p2.set_position((x2_p,y2_p))
        p1.set_position((x1_p,y1_p))
        return ([x1_p,y1_p],cords)


    def predict(self, p1, goalChance, iterate=15, stepSize=1):

        player_list, initialInfo,g = self.get_players_in_gcr(p1)

        scat_xr,scat_yr=[],[]
        s1x,s1y=[],[]

        x1,y1=p1.get_position()
        x3,y3=g
        dx = (0.01 if (x3-x1) == 0 else (x3-x1))
        Q1 = math.degrees(math.atan((y3-y1)/dx)) # Q1 is the angle of p1 - goalkeeper line
        if Q1 <0: Q1+=360 # convert positive angle

        # print Q1,"Q1"
        goalChances={}
        for i in range(iterate+1):
            goalChances[goalChance(p1)] = p1.get_position()
            bp, ot = self.getFutureCoordinates(p1, player_list,i*stepSize, g,Q1)
            s1x.append(bp[0])
            s1y.append(bp[1])

            for x,y in ot:
                scat_xr.append(x)
                scat_yr.append(y)
        p1.set_position(initialInfo[p1])
        for p2 in player_list:
            p2.set_position(initialInfo[p2])

        best_goal_position = max(goalChances.iteritems(), key=operator.itemgetter(0))[1]
        return best_goal_position, scat_xr,scat_yr, s1x,s1y


    def __str__(self):
        pass