__author__ = 'aliuzun'

from src.sentio.Time import Time
from sklearn import cluster
from scipy.sparse import *
from sklearn.cluster import KMeans

from src.sentio.Match import Match
from src.sentio.Sentio import Sentio

class Classification():

    def __init__(self,sentio):
        self.sentio = sentio


    def DataToKmeans(self):
        skDict={}
        sentio = Sentio()
        sentio.parseSentioData(coordinate_data="../data/GS_FB_Sentio.txt", event_data="../data/GS_FB_Event.txt")
        match = Match(sentio)
        match.identifyObjects()
        match.compute_someEvents()
        homePlayer = match.getHomeTeam().getTeamPlayers()
        awayPlayer = match.getAwayTeam().getTeamPlayers()

        for i in awayPlayer:
            a= str(awayPlayer[i].getJerseyNumber())+ "-" + "GS"
            skDict[a]=[awayPlayer[i].compute_runningDistance_withGameStopFilter(),awayPlayer[i].get_totalBallSteal(),awayPlayer[i].get_totalBallLose(),awayPlayer[i].get_totalBallPass()]
        #print skDict [running distanceiball steal,ball lose,get average location]
        #,q1[i].get_averageLocation()[0],q1[i].get_averageLocation()[1]]
        for i in homePlayer:
             a= str(homePlayer[i].getJerseyNumber())+ "-" + "FB"
             skDict[a]=[homePlayer[i].compute_runningDistance_withGameStopFilter(),homePlayer[i].get_totalBallSteal(),homePlayer[i].get_totalBallLose(),homePlayer[i].get_totalBallPass()]
        return skDict

    #@staticmethod
    def invert_dict(self,in_dict):
        inv = dict()
        #val=[]
        for key in in_dict:
            val = in_dict[key]
            if val not in inv:
                inv[val] = [key]
            else:
                inv[val].append(key)
        return inv


    def KmeansClusture(self,in_dict,k=6):
        l={}
        X=in_dict.values()
        S = coo_matrix(X)
        labeler = KMeans(k)
        labeler.fit(S.tocsr())
        for (row, label) in enumerate(labeler.labels_):
            l[str(in_dict.keys()[row])]=label

        return self.invert_dict(l)




