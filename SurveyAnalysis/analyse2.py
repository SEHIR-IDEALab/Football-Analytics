from src.sentio.gui.SnapShotCSV import SnapShot
# from src.sentio.pass_evaluate.Pass import Pass
from src.sentio.algorithms.Pass2 import Pass
from src.sentio.Sklearn.SurveyScoreCalculation import *
import csv
import glob



class SurveyAnalyse():

    def __init__(self,solution,pair=None):
        self.pair=pair
        self.sorted_risk,self.sorted_effectiveness,self.sorted_gc,self.sorted_pass_adv=[],[],[],[]
        self.weight_coefficient = solution
        self.survey_answer=[['P3', 'P2', 'P1'],['P2', 'P3', 'P1'],['P2', 'P1', 'P3'], ['P3', 'P2', 'P1'], ['P2', 'P1', 'P3'], (['P1', 'P2', 'P3'],['P3', 'P2', 'P1']), ['P2', 'P1', 'P3'], ['P2', 'P1', 'P3'], ['P2', 'P3', 'P1'], ['P2', 'P3', 'P1'], ['P2', 'P3', 'P1'], (['P3', 'P1', 'P2'],['P1', 'P3', 'P2'])]
        self.dd={"a":"P1","b":"P2","c":"P3"}

    def Write_to_csv(self):
        aaa=list()
        aaa.extend(["Q #","overal_risk","gain","pass_advantages","goal_chance","effectiveness_score"])
        out = csv.writer(open("/Users/aliuzun/PycharmProjects/futbol-data-analysis/SurveyAnalysis/pa.csv","w"), delimiter='\t', quoting=csv.QUOTE_NONE)
        out.writerow(aaa)
        PosDict={}
        del aaa[:]
        for file_path in glob.glob('/Users/aliuzun/PycharmProjects/futbol-data-analysis/SampleScenarios/Positions2/*.csv'):
            Q=file_path[len(file_path)-8:len(file_path)-4]
            status=self.getStatus(Q)
            snapShot = SnapShot(file_path)
            teams = snapShot.loadTeams()
            defined_passes = snapShot.getLoadedPassesFor(teams)
            pas = Pass()
            pas.teams = teams

            for pass_event in defined_passes:
                p1, p2 = pass_event.pass_source, pass_event.pass_target

                overallRisk, gain, pass_advantages,pa_player, goalChance, effectiveness = pas.effectiveness_withComponents(p1,p2,self.weight_coefficient,status)
                if Q not in PosDict:
                    PosDict[Q]=[Q,overallRisk, gain, pass_advantages, goalChance, effectiveness]
                else:
                    PosDict[Q]=[Q,PosDict[Q][1]+overallRisk, PosDict[Q][2]+gain, PosDict[Q][3]+pass_advantages, PosDict[Q][4]+goalChance, PosDict[Q][5]+effectiveness]

        for Qs in sorted(PosDict.keys()):
            aaa.extend(PosDict[Qs])
            out.writerow(aaa)
            del aaa[:]

    def getStatus(sefl,file):
        noRisk=["Q02a","Q02b","Q02c","Q04a","Q04b","Q04c","Q07a","Q07b","Q07c","Q05a","Q05b","Q05c","Q11a","Q11b","Q11c","Q09a","Q09b","Q09c"] # "Q09a","Q09b","Q09c"
        if file in noRisk:
            return True
        else: return False
        # return False

    def sortPossitions(self):
        risk_info,effectiveness_info,gchange_info,pass_adv=[],[],[],[]
        # sorted_risk,sorted_effectiveness,sorted_gc,sorted_pass_adv=[],[],[],[]

        # with open("PossitionsInfo.csv") as file:
        with open("/Users/aliuzun/PycharmProjects/futbol-data-analysis/SurveyAnalysis/pa.csv") as file:
            file.readline()
            data=csv.reader(file, delimiter="\t")
            for line in data:
                risk_info.append((line[0],float(line[1])))
                gchange_info.append((line[0],float(line[4])))
                effectiveness_info.append((line[0],float(line[5])))
                pass_adv.append((line[0],float(line[3])))

        for i in range(0,34,3):
            self.sorted_risk.append(sorted(risk_info[i:i+3],key=lambda element: (element[1])))
            self.sorted_effectiveness.append(sorted(effectiveness_info[i:i+3], reverse=True, key=lambda element: (element[1])))
            self.sorted_gc.append(sorted(gchange_info[i:i+3],reverse=True, key=lambda element: (element[1])))
            self.sorted_pass_adv.append(sorted(pass_adv[i:i+3], reverse= True, key=lambda element: (element[1])))

        self.sorted_risk = self.sorted_risk[2:11] + self.sorted_risk[0:2] + [self.sorted_risk[11]]
        self.sorted_effectiveness = self.sorted_effectiveness[2:11] + self.sorted_effectiveness[0:2] + [self.sorted_effectiveness[11]]
        self.sorted_gc = self.sorted_gc[2:11] + self.sorted_gc[0:2] + [self.sorted_gc[11]]
        self.sorted_pass_adv = self.sorted_pass_adv[2:11] + self.sorted_pass_adv[0:2] + [self.sorted_pass_adv[11]]
        # return sorted_risk,sorted_effectiveness,sorted_gc,sorted_pass_adv

    def get_result_list(self):
        riskPs,effectivenessPs,gcPs,pass_adv=[],[],[],[]
        try:
            for i in range(12):
                (x1r,y1r),(x2r,y2r),(x3r,y3r)=self.sorted_risk[i]
                riskPs.append((self.dd[x1r[-1]],self.dd[x2r[-1]],self.dd[x3r[-1]]))
                # print sorted_risk[i],"==>",(x1r,x2r,x3r),"==>",(dd[x1r[-1]],dd[x2r[-1]],dd[x3r[-1]])

                (x1e,y1e),(x2e,y2e),(x3e,y3e)=self.sorted_effectiveness[i]
                effectivenessPs.append((self.dd[x1e[-1]],self.dd[x2e[-1]],self.dd[x3e[-1]]))
                # print sorted_effectiveness[i],"==>",(x1e,x2e,x3e),"==>",(dd[x1e[-1]],dd[x2e[-1]],dd[x3e[-1]])

                (x1g,y1g),(x2g,y2g),(x3g,y3g)=self.sorted_gc[i]
                gcPs.append((self.dd[x1g[-1]],self.dd[x2g[-1]],self.dd[x3g[-1]]))

                (x1pa,y1pa),(x2pa,y2pa),(x3pa,y3pa)=self.sorted_pass_adv[i]
                pass_adv.append((self.dd[x1pa[-1]],self.dd[x2pa[-1]],self.dd[x3pa[-1]]))

            SurveyAnswer=[]

            for i in range(1,13):
                if i in [1,3,8]:
                    ourRes = list(riskPs[i-1])
                    SurveyAnswer.append(ourRes)

                elif i in [2,4,5,6,11,12]:
                    ourRes = list(effectivenessPs[i-1])
                    SurveyAnswer.append(ourRes)

                elif i==7:
                    ourRes = list(gcPs[i-1])
                    SurveyAnswer.append(ourRes)

                elif i in [9,10]:
                    ourRes = list(effectivenessPs[i-1])
                    ourRes[0],ourRes[2] = ourRes[2],ourRes[0]
                    SurveyAnswer.append(ourRes)
            return SurveyAnswer
        except ValueError:
            pass


    def convertPs(self):
        riskPs,effectivenessPs,gcPs,pass_adv=[],[],[],[]
        for i in range(12):

            (x1r,y1r),(x2r,y2r),(x3r,y3r)=self.sorted_risk[i]
            riskPs.append((self.dd[x1r[-1]],self.dd[x2r[-1]],self.dd[x3r[-1]]))

            (x1e,y1e),(x2e,y2e),(x3e,y3e)=self.sorted_effectiveness[i]
            # if i==1:
            #     print self.sorted_effectiveness[i]
            effectivenessPs.append((self.dd[x1e[-1]],self.dd[x2e[-1]],self.dd[x3e[-1]]))

            (x1g,y1g),(x2g,y2g),(x3g,y3g)=self.sorted_gc[i]
            gcPs.append((self.dd[x1g[-1]],self.dd[x2g[-1]],self.dd[x3g[-1]]))

            (x1pa,y1pa),(x2pa,y2pa),(x3pa,y3pa)=self.sorted_pass_adv[i]
            pass_adv.append((self.dd[x1pa[-1]],self.dd[x2pa[-1]],self.dd[x3pa[-1]]))

        surveyRes,ourRes=[],[]

        # p1,p2=self.pair[0]+1,self.pair[1]+1
        p1=self.pair+1

        print "      Tool's Answer","      Survey Answer"
        for i in range(1,13):

            surveyRes = self.survey_answer[(i-1)]

            if i in [1,3,8]:
                ourRes = list(riskPs[i-1])

            elif i in [2,4,5,6,11,12]:
                ourRes = list(effectivenessPs[i-1])

            elif i==7:
                ourRes = list(gcPs[i-1])

            # elif i==9:
            #     ourRes = list(effectivenessPs[i-1])

            elif i in [9,10]:
                ourRes = list(effectivenessPs[i-1])
                ourRes[0],ourRes[2] = ourRes[2],ourRes[0]

            if p1==i:
                print "Q"+str(i),"::::",ourRes,surveyRes,"++++++",
                if surveyRes!=ourRes:
                    print "*"
                else:
                    print ""
            else:
                print "Q"+str(i),"::::",ourRes,surveyRes,
                if surveyRes!=ourRes:
                    print "*"
                else:
                    print ""



if __name__ == "__main__":
    # sol=[899.0, 503.0, 474.0]
    # sol=[1, 5]
    # sol=[11, 2, 2298]

    sol1=[557, 984, 142]
    sol2=[337, 674, 668]

    sol=[489, 975, 572] # gives best score 33
    # sol=[829.0, 946.0, 287.0] # annealing solution
    # sol=[847, 919, 105] # for Q4
    # sol=[464, 859, 123] # Q9 is 1 point
    # sol =[557, 999, 335]
    # sol_t=502,999,566


    # sol=[20,3,45,507,832,837]
    # q=SurveyAnalyse(sol,(-1,-1))
    # q.Write_to_csv()
    # q.sortPossitions()
    # q.convertPs()

    w=ScoreCal()
    # print "Cost:",w.CostScore2(sol,(-2,-2))
    # newCoeff=[[124, 244, 524],[519, 976, 889],[488, 967, 971],[464, 859, 123],[395, 785, 828],[240, 472, 777]]
    # pairs=[(11,1),(6,5),(9,10),(8,2),(4,3),(7,0)]
    # for i in range(len(newCoeff)):
    #     q=SurveyAnalyse(newCoeff[i],pairs[i])
    #     q.Write_to_csv()
    #     q.sortPossitions()
    #     q.convertPs()
    #     print "----------------------"

    l1=[[542, 950, 362],[477, 953, 370],[494, 983, 604],[907, 973, 641],[549, 999, 37],[553, 980, 172],[437, 863, 989],[469, 937, 241],[513, 993, 285],[277, 551, 462],[466, 849, 782],[564, 991, 419]]
    #leave one out
    l2=[[135, 259, 816],[477, 953, 370],[494, 983, 604],[847, 919, 105], [232, 454, 929],[553, 980, 172], [476, 943, 945], [48, 93, 576], [557, 999, 335],[277, 551, 462], [480, 954, 635], [97, 192, 488]]

    # pair2=[[514,902,473],[420,765,719],[455,901,932],[502,999,566],[119,237,242],[462,481,964]]
    # Q=[(3,10),(1,12),(5,8),(7,4),(2,11),(6,9)]



    # for i in range(12):
    #     print w.CostScore2(l2[i],i,status=1)
    #     q=SurveyAnalyse(l2[i],i)
    #     q.Write_to_csv()
    #     q.sortPossitions()
    #     q.convertPs()
    #     print "-------------------------------"
    # Qs=[(8,11),(3,4),(10,1),(2,7),(9,0),(6,5)]
    # Ps=[[20, 4, 42, 278, 275, 511],[20, 4, 33, 265, 466, 382],[20, 8, 6, 426, 271, 769],[11, 6, 50, 577, 470, 448],[18, 6, 50, 1000, 956, 218],[20, 6, 44, 357, 305, 345]]
    #
    # a=0
    # for i in range(6):
    #     print Qs[i]
    #     a+= (-w.CostScore2(Ps[i],Qs[i])+w.CostScore2(Ps[i],(-1,-1)))*100/6.0
    #     q=SurveyAnalyse(Ps[i],Qs[i])
    #     q.Write_to_csv()
    #     q.sortPossitions()
    #     q.convertPs()
    #     print "-------------------------------"
    # print a/6.0


    # Qs=[(8,1),(4,3),(10, 5),(6, 7),(11, 0),(9, 2)]
    # Ws=[[20, 6, 3, 628, 818, 393],[20, 6, 3, 675, 886, 860],[20, 6, 3, 644, 961, 414],[20, 6, 3, 504, 879, 960],[20, 7, 3, 638, 940, 334],[20, 30, 3, 733, 574, 882]]
    # a=0
    # for i in range(6):
    #     print Qs[i]
    #     scr=(-w.CostScore2(Ws[i],Qs[i])+w.CostScore2(Ws[i],(-1,-1)))
    #     print scr
    #     a+= scr*100/6.0
    #     q=SurveyAnalyse(Ws[i],Qs[i])
    #     q.Write_to_csv()
    #     q.sortPossitions()
    #     q.convertPs()
    #     print "-------------------------------"
    #     # break
    # print a/6.0

    Qs=[0,1,2,3,4,5,6,7,8,9,10,11]
    #29-31-30-30-30-30-29-30-31-31-30-30
    # l2=[[20, 7, 6, 467, 674, 966],[20, 2, 8, 852, 632, 745],[20, 2, 7, 662, 989, 637],[20, 2, 7, 586, 849, 709],[20, 3, 7, 559, 818, 353],[20, 7, 7, 489, 906, 865],[20, 7, 7, 247, 450, 557],[20, 2, 7, 252, 458, 80],[20, 2, 7, 523, 926, 340],[20, 2, 7, 388, 677, 156],[20, 2, 7, 660, 947, 158],[20, 7, 7, 205, 334, 979]]
    l2=[[20, 6, 3, 779, 629, 18],[20, 2, 3, 765, 666, 292],[20, 6, 3, 945, 948, 716],[20, 7, 3, 915, 449, 737],[20, 6, 3, 471, 592, 238],[20, 6, 3, 513, 690, 335],[20, 6, 3, 569, 909, 197],[20, 6, 3, 666, 673, 688],[20, 6, 3, 798, 611, 517],[20, 2, 2, 164, 208, 82],[20, 6, 3, 633, 695, 435],[20, 7, 3, 374, 703, 482]]
    # a=0
    # for i in Qs:
    #     scr=(-w.CostScore2(l2[i],Qs[i])+w.CostScore2(l2[i],(-1,-1)))
    #     print scr*100/3.0
    #     a+= scr*100/3.0
    #     q=SurveyAnalyse(l2[i],Qs[i])
    #     q.Write_to_csv()
    #     q.sortPossitions()
    #     q.convertPs()
    #     if i==1:
    #         break
    # print a/12.0

    # ll=[[10, 2, 7, 98, 170, 169],[10, 2, 8, 336, 234, 394],[10, 2, 7, 300, 489, 307],[10, 2, 8, 201, 326, 80],[10, 2, 7, 235, 408, 479],[10, 2, 7, 219, 419, 174],[10, 2, 7, 250, 462, 403],[10, 2, 2, 419, 469, 482],[10, 2, 15, 155, 234, 413],[10, 2, 7, 187, 298, 85],[9, 2, 7, 259, 454, 207],[10, 5, 7, 222, 360, 1]]# new ranges
    # a=0
    # for i in Qs:
    #     scr=(-w.CostScore2(ll[i],Qs[i])+w.CostScore2(ll[i],(-1,-1)))
    #     print scr*100/3.0
    #     a+= scr*100/3.0
    #     q=SurveyAnalyse(ll[i],Qs[i])
    #     q.Write_to_csv()
    #     q.sortPossitions()
    #     q.convertPs()
    #     # if i==1:
    #     #     break
    # print a/12.0


    # new parameters:: desicion time
    #30-31-30-30-30-31-30-30-30-31-30-30
    lw=[[10, 2, 7, 297, 542, 341, 667],[10, 2, 8, 772, 523, 777, 432],[10, 2, 7, 465, 758, 837, 731],[10, 2, 7, 440, 630, 502, 681],[10, 2, 7, 475, 774, 911, 437],
        [10, 2, 7, 599, 895, 968, 703],[9, 2, 7, 571, 884, 833, 812],[10, 2, 7, 450, 646, 967, 643],[10, 5, 7, 583, 962, 630, 100],[10, 2, 7, 382, 686, 927, 772],[10, 2, 2, 874, 1000, 840, 625],[10, 5, 7, 298, 512, 889, 770]]
    a=0
    # for i in Qs:
    #     scr=(-w.CostScore2(lw[i],Qs[i])+w.CostScore2(lw[i],(-1,-1)))
    #     print scr*100/3.0
    #     a+= scr*100/3.0
    #     q=SurveyAnalyse(lw[i],Qs[i])
    #     q.Write_to_csv()
    #     q.sortPossitions()
    #     q.convertPs()
    #
    # print a/12.0
    i=4
    scr=(-w.CostScore2(lw[i],Qs[i])+w.CostScore2(lw[i],(-1,-1)))
    print scr*100/3.0
    a+= scr*100/3.0
    q=SurveyAnalyse(lw[i],Qs[i])
    q.Write_to_csv()
    q.sortPossitions()
    q.convertPs()