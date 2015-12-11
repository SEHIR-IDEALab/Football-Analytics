__author__ = 'aliuzun'
import csv
#from profilehooks import profile, timecall
import math
from src.sentio.object import Match
from src.sentio.Time import Time
from sklearn import svm
import numpy
import random

from src.sentio.Sentio import Sentio

class WhoHasBall():

    def __init__(self,sentio):
        self.sentio = sentio
        self.match = Match(sentio)
        self.time_int,self.score,self.had_ball=None,None,None
        self.corrFB,self.corrGS,self.corrXFB,self.corrXGS=0,0,0,0

    def get_time_info(self,minute):
        if minute <= 15:
            time_int=1
        elif minute > 15 and minute <=30:
            time_int=2
        elif minute > 30 and minute <=45:
            time_int=3
        elif minute > 45 and minute <=60:
            time_int=4
        elif minute > 60 and minute <=75:
            time_int=5
        elif minute > 75 and minute <=90:
            time_int=6
        return time_int

    def score_info(self,half, minute, second, mili_second):
        scoreInfo=self.match.getMatchScore_forGivenTime(half, minute, second, mili_second)
        if scoreInfo[self.match.getHomeTeam().getTeamName()] >  scoreInfo[self.match.getAwayTeam().getTeamName()]:
            score=1
        elif scoreInfo[self.match.getHomeTeam().getTeamName()] <  scoreInfo[self.match.getAwayTeam().getTeamName()]:
            score=-1
        else:
            score=0
        return score

    #@profile(immediate=True) ##3.08 sec
    def get_currentEventData(self, half, minute, second, milisec):
        try:
            self.eventData_byTime=self.sentio.getEventData_byTime()
            eventData_current = self.eventData_byTime[half][minute][second]
            return eventData_current
        except KeyError:
            time = Time(half, minute, second, milisec)
            back_time = time.back()
            #print back_time.half, back_time.minute, back_time.second, back_time.mili_second
            return self.get_currentEventData(back_time.half, back_time.minute, back_time.second, back_time.mili_second)
    #@profile(immediate=True)  ##2.94 sec
    def get_previousEventData(self,half, minute ,second, milisec, chosenSkip):
        if chosenSkip == None: chosenSkip = 0
        time = Time(half, minute, second, milisec)
        back_half, back_minute, back_second, back_milisec = time.half, time.minute, time.second, time.mili_second
        for skipTimes in range(chosenSkip+1):
            back_time = time.back()
            back_half, back_minute, back_second, back_milisec = back_time.half, back_time.minute, back_time.second, back_time.mili_second
        eventData_previous = self.get_currentEventData(back_half, back_minute, back_second, back_milisec)
        return eventData_previous

    #@profile(immediate=True) #2.94 sec
    def get_preBallOwner(self,half,minute,second,mili_second,chosenSkip=5):
        preOwner=self.get_previousEventData(half, minute, second, mili_second,5)
        if preOwner[0][0]==self.match.getHomeTeam().getTeamName():
            had_ball=1
        elif preOwner[0][0]==self.match.getAwayTeam().getTeamName():
            had_ball=-1
        else:
            had_ball=0
        return had_ball


    def get_currentBallOwner(self,a):
        own=None
        if a==self.match.getHomeTeam().getTeamName():
           own=1
        elif a==self.match.getAwayTeam().getTeamName():
            own=0
        return own

    #@profile(immediate=True) # 5.73 sec
    def getCorrelatedPlayer_byTime(self,half,minute,second,mili_second):
        fbDict,gsDict,fbDict1,gsDict1={},{},{},{}
        corFB,corGS,corXFB,corXGS=0,0,0,0

        q=self.sentio.getCoordinateData_byTime()
        time = Time(half, minute, second, mili_second)
        time.set_minMaxOfHalf(self.match.get_minMaxOfHalf())
        print half,minute,second,mili_second
        for tt in [0,1]:
            coord_info0=q[half][minute][second+tt][0]
            coord_info2=q[half][minute][second+tt][2]
            coord_info4=q[half][minute][second+tt][4]
            coord_info6=q[half][minute][second+tt][6]
            coord_info8=q[half][minute][second+tt][8]
            min_length=min(len(coord_info0),len(coord_info2),len(coord_info4),len(coord_info6),len(coord_info8))
            for i in xrange(min_length):
                x1,y1=0,0
                team1,pl1,x0,y0=int(coord_info0[i][0]),int(coord_info0[i][2]),float(coord_info0[i][3]),float(coord_info0[i][4])
                team1,pl1,x2,y2=int(coord_info2[i][0]),int(coord_info2[i][2]),float(coord_info2[i][3]),float(coord_info2[i][4])
                team1,pl1,x4,y4=int(coord_info4[i][0]),int(coord_info4[i][2]),float(coord_info4[i][3]),float(coord_info4[i][4])
                team1,pl1,x6,y6=int(coord_info6[i][0]),int(coord_info6[i][2]),float(coord_info6[i][3]),float(coord_info6[i][4])
                team1,pl1,x8,y8=int(coord_info8[i][0]),int(coord_info8[i][2]),float(coord_info8[i][3]),float(coord_info8[i][4])

                point_x=[x0,x2,x4,x6,x8]
                point_y=[y0,y2,y4,y6,y8]

                for i in range(5):
                    next_time=time.next()
                    time_half, time_min, time_sec, time_milisec = next_time.half, next_time.minute, next_time.second, next_time.mili_second
                #next_coord_info = q[next_time.half][next_time.minute][next_time.second][next_time.mili_second]
                for index,tm in enumerate([0,2,4,6,8]):
                    next_coord_info = q[next_time.half][next_time.minute][next_time.second][tm]
                    for i in range(len(next_coord_info)):
                        team2,pl2,x,y=int(next_coord_info[i][0]),int(next_coord_info[i][2]),float(next_coord_info[i][3]),float(next_coord_info[i][4])
                        if pl2==pl1:
                            if x != None:
                                point_x[index]=x
                            else:
                                point_x.pop(index)
                            if y != None:
                                point_y[index]=y
                            else:
                                point_y.pop(index)

                            x1=(sum(point_x))/len(point_x)
                            y1=(sum(point_y))/len(point_y)

                            if team1 in [1,4]:
                                if tt==0:
                                    if pl1 not in gsDict: gsDict[pl1]=[x1,y1]
                                    else: gsDict[pl1].extend([x1,y1])
                                else:
                                    if pl1 not in gsDict1: gsDict1[pl1]=[x1,y1]
                                    else: gsDict1[pl1].extend([x1,y1])
                            elif team1 in [0,3]:
                                if tt==0:
                                    if pl1 not in fbDict: fbDict[pl1]=[x1,y1]
                                    else: fbDict[pl1].extend([x1,y1])
                                else:
                                    if pl1 not in fbDict1: fbDict1[pl1]=[x1,y1]
                                    else: fbDict1[pl1].extend([x1,y1])


        for tms in [gsDict.values() + fbDict.values()]:
            for pl in tms:
                if len(pl) !=10:
                    for i in range(10-len(pl)):
                        pl.append(-1)


        v1GS=gsDict.values()
        v2GS=gsDict1.values()
        v1FB=fbDict.values()
        v2FB=fbDict1.values()

        averageSpeed=[]
        for indexfb,ply in enumerate(v1FB):
            for indexgs,o_ply in enumerate(v1GS):

                for i in range(min(len(ply),len(o_ply))):
                    averageSpeed.extend([((ply[i] + o_ply[i])/2)])

                a=min(len(averageSpeed),len(v2FB[indexfb]),len(v2GS[indexgs]))

                if numpy.corrcoef(averageSpeed[:a],(v2FB[indexfb])[:a])[0,1] >= numpy.corrcoef(averageSpeed[:a],(v2GS[indexgs])[:a])[0,1]:
                    corFB+=1
                    corXFB+=math.fabs((o_ply[0]-o_ply[4]))
                    #corXGS+=math.fabs((ply[0]-ply[4]))
                if numpy.corrcoef(averageSpeed[:a],(v2GS[indexgs])[:a])[0,1] >= numpy.corrcoef(averageSpeed[:a],(v2FB[indexfb][:a]))[0,1]:
                    corGS+=1
                    #corXFB+=math.fabs((o_ply[0]-o_ply[4]))
                    corXGS+=math.fabs((ply[0]-ply[4]))
                averageSpeed=[]
        return [corFB,corGS,corXFB,corXGS]



    #@profile(immediate=True)
    def getBallOwner_byTime(self,half,minute,second,mili_second=0):
        gkGSx,gkFBx,netGSx,netFBx,netGSy,netFBy=0,0,0,0,0,0
        av_speedGS,av_speedFB,sp6_GS,sp6_FB,distanceGS,distanceFB=0,0,0,0,0,0
        Fdata=[]

        q=self.sentio.getCoordinateData_byTime()
        current_event_info = self.get_currentEventData(half, minute, second, mili_second)

        a,b,z=current_event_info[0] # a will be used for deciding the ball owner at given time

        time = Time(half, minute, second, mili_second)
        time.set_minMaxOfHalf(self.match.get_minMaxOfHalf())
        time_half, time_min, time_sec, time_milisec = time.half, time.minute, time.second, time.mili_second
        current_coord_info = q[time_half][time_min][time_sec][time_milisec]
        for i in range(5):
            next_time=time.next()
            time_half, time_min, time_sec, time_milisec = next_time.half, next_time.minute, next_time.second, next_time.mili_second

        next_coord_info = q[next_time.half][next_time.minute][next_time.second][next_time.mili_second]

        if self.get_currentBallOwner(a) != None:
            for i in xrange(len(current_coord_info)):
                q = current_coord_info[i]
                q_next = next_coord_info[i]
                team1,pl1,x1,y1=int(q[0]),int(q[2]),float(q[3]),float(q[4])
                team2,pl2,x2,y2=int(q_next[0]),int(q_next[2]),float(q_next[3]),float(q_next[4])

                if team1 ==4:
                    gkGSx=x1
                elif team1==1:
                    netGSy+=math.fabs(y2-y1)
                    X1=math.sqrt(((x2-x1)*(x2-x1)) + ((y2-y1)*(y2-y1)))
                    if (X1*3.6) >= 6:
                        sp6_GS+=1
                    av_speedGS+=(X1*3.6)
                    distanceGS+=X1
                    if math.fabs((x2-gkGSx)) >=math.fabs((x1-gkGSx)):
                        netGSx+=(math.fabs(x2-x1))
                    else:
                        netGSx+=-(math.fabs(x2-x1))

                if team1 ==3:
                    gkFBx=x1
                elif team1==0:
                    netFBy+=math.fabs(y2-y1)
                    X1=math.sqrt(((x2-x1)*(x2-x1)) + ((y2-y1)*(y2-y1)))
                    if (X1*3.6) >= 6:
                        sp6_FB+=1
                    av_speedFB+=(X1*3.6)
                    distanceFB+=X1
                    if math.fabs((x2-gkFBx)) >=math.fabs((x1-gkFBx)):
                        netFBx+=(math.fabs(x2-x1))
                    else:
                        netFBx+=-(math.fabs(x2-x1))
        else:
            pass

        Fdata.extend([netFBx,netGSx,netFBy,netGSy,distanceFB,distanceGS,self.get_time_info(minute),(av_speedFB/11),(av_speedGS/11),sp6_FB,sp6_GS,self.get_preBallOwner(half, minute, second, mili_second),self.score_info(half, minute, second, mili_second)])
        Fdata.extend(self.getCorrelatedPlayer_byTime(half,minute,second,mili_second))
        return [self.get_currentBallOwner(a),Fdata]

    def Run_Test(self):
        aaa = list()
        aaa.extend(["half","minute","second","Inf","changesInXFB", "changesInXGS", "changesInYFB", "changesInYGS", "coveredDistanceFB", "coveredDistanceGS", "timeInfo", "averageSpeedFB", "averageSpeedGS","NumofPlayer>6FB","NumofPlayer>6GS",
                    "preBallOwner","scoreInfo","NumofCorPlayerFB","NumofCorPlayerGS","DistanceInXFB","DistanceInXGS"])
        out = csv.writer(open("tests_result/result_test.csv","a"), delimiter='\t', quoting=csv.QUOTE_NONE)
        out.writerow(aaa)
        del aaa[:]
        trainData=[]
        tr1,tr0,own0,own1=[],[],[],[]
        own=[]
        realvalues,testdata = [],[]
        i=1
        while i <=44 :
            for l in range(0,59,3):
                try:
                    owner_, feature_ = self.getBallOwner_byTime(1,i,l)
                    aaa.extend([1,i,l,owner_, feature_])
                    out.writerow(aaa)
                    del aaa[:]
                    if owner_==1:
                        tr1.append(feature_)
                        own1.append(owner_)

                    elif owner_==0:
                        tr0.append(feature_)
                        own0.append(owner_)

                except (IndexError,KeyError):
                    pass
            i=i+1

        #outfile1 = open(filename1, "a")
        #outfile1.write(tr0)
        print len(own1),len(own0)
        print "********************"
        aa=0
        for i in range(100):
            try:
                index=random.randint(0,len(own1)-aa)
                trainData.append(tr1[index])
                own.append(own1[index])
                tr1.pop(index)
                own1.pop(index)
                aa+=1
            except (ValueError,IndexError):
                pass
        bb=0
        for i in range(100):
            try:
                index=random.randint(0,len(own0)-bb)

                trainData.append(tr0[index])
                own.append(own0[index])
                tr0.pop(index)
                own0.pop(index)
                bb+=1
            except (ValueError,IndexError):
                pass

        testdata.extend(tr1[:15] + tr0[:15])
        realvalues.extend(own1[:15] + own0[:15])


        clf=svm.SVC()
        clf.fit(trainData,own)
        predicted=[]
        for data in testdata:
            predicted.extend(clf.predict(data))
        kl=0
        for i in range(len(predicted)):
            if predicted[i] != realvalues[i]:
                kl+=1
        print kl,len(predicted),len(own)

        print predicted,realvalues

