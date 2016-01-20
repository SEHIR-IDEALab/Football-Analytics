import math
from src.sentio.Parameters import average_speed_player, average_distance_per_frame, GOALPOST_LENGTH
from src.sentio.analytics.Analyze import Analyze

__author__ = 'emrullah'


class OptimalShootingPointPrediction:

    def __init__(self, teams):
        self.teams = teams


    def get_players_in_gcr(self, p1): # return the list of player has affect on goal chance
        players_list=[]
        initialInfo={}

        own_goal_keeper = self.teams.home_team.getGoalKeeper()
        opponent_goal_keeper = self.teams.away_team.getGoalKeeper()
        x_home, x_away= own_goal_keeper.getX(),opponent_goal_keeper.getX()

        if p1.isHomeTeamPlayer():
            team=self.teams.away_team
            min_x=min(p1.get_position()[0],x_away)
            max_x=max(p1.get_position()[0],x_away)
        else:
            team=self.teams.home_team
            min_x=min(p1.get_position()[0],x_home)
            max_x=max(p1.get_position()[0],x_home)
        # player_list=team.getJerseyNumbersOfPlayers()
        player_list=team.getTeamPlayers()

        initialInfo[p1]=(p1.getX(),p1.getY())

        for player1 in player_list:
            js,x,y=player1.getJerseyNumber(),player1.getX(),player1.getY()
            if (x >= min_x) and (x <= max_x) and ((x,y)!=(team.getGoalKeeper().getX(), team.getGoalKeeper().getY())):
                players_list.append(player1)
                initialInfo[player1]=(player1.getX(),player1.getY())

        return (players_list,initialInfo)


    def getLN(self, p1, p2s, Gxy): # give the number of times next position will be got
        dists=list()
        x1, y1 = p1.get_position()
        x3, y3 = Gxy

        try: tmp_slope=(y3-y1)/(x3-x1)
        except ZeroDivisionError: tmp_slope=100

        Q1 = math.degrees(math.atan(tmp_slope)) # Q1 is the angle of p1 - goalkeeper line
        try: slope = (y3 - y1) / (x3 - x1) # zero devision error gives
        except ZeroDivisionError: slope = 100 # might be change
        a,b,c = slope,-1,( ( slope * (-x1) ) + y1 )

        for p2 in p2s:

            x2, y2 = p2.get_position()
            angle1 = math.degrees(math.atan((y2-y1)/(x2-x1))) # the angle of p1-p2 line
            alpha_p1 = 2*math.fabs(Q1-angle1) # the angle with p1's direction and p1-p2 line
            d2 = math.fabs(a * x2 + b * y2 + c) / math.sqrt(math.pow(a, 2) + math.pow(b, 2))

            if alpha_p1 > 180:
                # alpha_p1 = alpha_p1 - 180
                t=(d2/average_speed_player)
            else:
                alpha_p1 = math.radians(alpha_p1)
                t=(d2/average_speed_player)*math.sin(alpha_p1)

            dists.append(int(t))
        print dists ##########################
        return dists


    def getPointLocation(self, p1, p2, Gxy):
        x3,y3=Gxy
        x1,y1=p1.get_position()
        x2,y2=p2.get_position()

        try: m=(y3-y1)/(x3-x1)
        except ZeroDivisionError: m=100

        # m=(y3-y1)/(x3-x1) #slope
        a=y1-m*x1 # constant
        tmp_val=m*x2+a

        if y2 > tmp_val:   return -1
        elif y2 < tmp_val: return 1
        else:              return 0


    def getFutureCoordinates(self, p1, p2s, Gxy, t):
        x1, y1 = p1.get_position()
        x3, y3 = Gxy
        try: tmp_slope=(y3-y1)/(x3-x1)
        except ZeroDivisionError: tmp_slope=100

        Q1 = math.degrees(math.atan(tmp_slope)) # Q1 is the angle of p1 - goalkeeper line

        if x1 > x3:
            x1_p,y1_p  = x1 - t*(average_distance_per_frame)*round(math.cos(math.radians(Q1)),2) ,\
                       y1 - t*(average_distance_per_frame)*round(math.sin(math.radians(Q1)),2)
        else:
            x1_p,y1_p  = x1 + t*(average_distance_per_frame)*round(math.cos(math.radians(Q1)),2) ,\
                           y1 + t*(average_distance_per_frame)*round(math.sin(math.radians(Q1)),2)

        ## set the new coordinates
        p1.set_position((x1_p,y1_p))

        cords=[]
        for p2 in p2s:
            wherePoint=self.getPointLocation(p1, p2, Gxy)
            x2, y2 = p2.get_position()
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

           ## set the new coordinates
            p2.set_position((x2_p,y2_p))

            return ([x1_p,y1_p],cords)


    def predict(self, p1, goalChance, iterate=None):
        goal_keeper = Analyze.detectGoalKeeperWithPositions(p1, self.teams)

        player_list, initialInfo = self.get_players_in_gcr(p1)

        if not iterate:
            try:
                iterate = min(self.getLN(p1, player_list, goal_keeper.get_position()))
            except ValueError:
                iterate=1
            iterate = (1 if iterate == 0 else iterate)

        scat_xr,scat_yr=[],[]
        s1x,s1y=[],[]

        goalChances=[]
        for i in range(iterate+1):
            goalChances.append(goalChance(p1))

            bp, ot = self.getFutureCoordinates(p1, player_list, goal_keeper.get_position(), i)
            s1x.append(bp[0])
            s1y.append(bp[1])

            for x,y in ot:
                scat_xr.append(x)
                scat_yr.append(y)

        p1.set_position(initialInfo[p1])
        for p2 in player_list:
            p2.set_position(initialInfo[p2])

        return max(goalChances), scat_xr,scat_yr, s1x,s1y


    def __str__(self):
        pass