from src.sentio.gui.SnapShot import SnapShot
# from src.sentio.pass_evaluate.Pass import Pass
from src.sentio.pass_evaluate.Pass2 import Pass
import csv
import glob



class SurveyAnalyse():

    def __init__(self,solution):
        self.sorted_risk,self.sorted_effectiveness,self.sorted_gc,self.sorted_pass_adv=[],[],[],[]
        self.weight_coefficient = solution
        self.survey_answer=[['P3', 'P2', 'P1'],['P2', 'P3', 'P1'],['P2', 'P1', 'P3'], ['P3', 'P2', 'P1'], ['P2', 'P1', 'P3'], ['P1', 'P2', 'P3'], ['P2', 'P1', 'P3'], ['P2', 'P1', 'P3'], ['P2', 'P3', 'P1'], ['P2', 'P3', 'P1'], ['P2', 'P3', 'P1'], ['P3', 'P1', 'P2']]


    def Write_to_csv(self):
        aaa=list()
        aaa.extend(["Q #","overal_risk","gain","pass_advantages","goal_chance","effectiveness_score"])
        out = csv.writer(open("/Users/aliuzun/PycharmProjects/SentioProject/SurveyAnalysis/Po2.csv","w"), delimiter='\t', quoting=csv.QUOTE_NONE)
        out.writerow(aaa)
        PosDict={}
        del aaa[:]
        for file_path in glob.glob('/Users/aliuzun/PycharmProjects/SentioProject/SampleScenarios/Positions2/*.csv'):
            Q=file_path[len(file_path)-8:len(file_path)-4]

            status=self.getStatus(Q)

            snapShot = SnapShot(file_path)
            teams = snapShot.loadTeams()
            defined_passes = snapShot.getLoadedPassesFor(teams)
            pas = Pass()
            pas.teams = teams
            for pass_event in defined_passes:
                p1, p2 = pass_event.pass_source, pass_event.pass_target
                try:
                    overallRisk, gain, pass_advantages,pa_player, goalChance, effectiveness = pas.effectiveness_withComponents(p1,p2,self.weight_coefficient,status)
                    if Q not in PosDict:
                        PosDict[Q]=[Q,overallRisk, gain, pass_advantages, goalChance, effectiveness]
                    else:
                        PosDict[Q]=[Q,PosDict[Q][1]+overallRisk, PosDict[Q][2]+gain, PosDict[Q][3]+pass_advantages, PosDict[Q][4]+goalChance, PosDict[Q][5]+effectiveness]
                except:
                    TypeError
                    pass
        for Qs in sorted(PosDict.keys()):

            aaa.extend(PosDict[Qs])
            out.writerow(aaa)
            del aaa[:]

    def getStatus(sefl,file):
        noRisk=["Q02a","Q02b","Q02c","Q04a","Q04b","Q04c","Q07a","Q07b","Q07c","Q05a","Q05b","Q05c","Q11a","Q11b","Q11c","Q09a","Q09b","Q09c"] # "Q09a","Q09b","Q09c"
        if file in noRisk:
            return True
        else: return False

    def sortPossitions(self):
        risk_info,effectiveness_info,gchange_info,pass_adv=[],[],[],[]
        # sorted_risk,sorted_effectiveness,sorted_gc,sorted_pass_adv=[],[],[],[]

        # with open("PossitionsInfo.csv") as file:
        with open("/Users/aliuzun/PycharmProjects/SentioProject/SurveyAnalysis/Po2.csv") as file:
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
        dd={"a":"P1","b":"P2","c":"P3"}
        for i in range(12):
            (x1r,y1r),(x2r,y2r),(x3r,y3r)=self.sorted_risk[i]
            riskPs.append((dd[x1r[-1]],dd[x2r[-1]],dd[x3r[-1]]))
            # print sorted_risk[i],"==>",(x1r,x2r,x3r),"==>",(dd[x1r[-1]],dd[x2r[-1]],dd[x3r[-1]])

            (x1e,y1e),(x2e,y2e),(x3e,y3e)=self.sorted_effectiveness[i]
            effectivenessPs.append((dd[x1e[-1]],dd[x2e[-1]],dd[x3e[-1]]))
            # print sorted_effectiveness[i],"==>",(x1e,x2e,x3e),"==>",(dd[x1e[-1]],dd[x2e[-1]],dd[x3e[-1]])

            (x1g,y1g),(x2g,y2g),(x3g,y3g)=self.sorted_gc[i]
            gcPs.append((dd[x1g[-1]],dd[x2g[-1]],dd[x3g[-1]]))

            (x1pa,y1pa),(x2pa,y2pa),(x3pa,y3pa)=self.sorted_pass_adv[i]
            pass_adv.append((dd[x1pa[-1]],dd[x2pa[-1]],dd[x3pa[-1]]))

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
        # print SurveyAnswer
        return SurveyAnswer

    def convertPs(self):
        riskPs,effectivenessPs,gcPs,pass_adv=[],[],[],[]
        dd={"a":"P1","b":"P2","c":"P3"}
        for i in range(12):
            (x1r,y1r),(x2r,y2r),(x3r,y3r)=self.sorted_risk[i]
            riskPs.append((dd[x1r[-1]],dd[x2r[-1]],dd[x3r[-1]]))
            # print sorted_risk[i],"==>",(x1r,x2r,x3r),"==>",(dd[x1r[-1]],dd[x2r[-1]],dd[x3r[-1]])

            (x1e,y1e),(x2e,y2e),(x3e,y3e)=self.sorted_effectiveness[i]
            effectivenessPs.append((dd[x1e[-1]],dd[x2e[-1]],dd[x3e[-1]]))
            # print sorted_effectiveness[i],"==>",(x1e,x2e,x3e),"==>",(dd[x1e[-1]],dd[x2e[-1]],dd[x3e[-1]])

            (x1g,y1g),(x2g,y2g),(x3g,y3g)=self.sorted_gc[i]
            gcPs.append((dd[x1g[-1]],dd[x2g[-1]],dd[x3g[-1]]))

            (x1pa,y1pa),(x2pa,y2pa),(x3pa,y3pa)=self.sorted_pass_adv[i]
            pass_adv.append((dd[x1pa[-1]],dd[x2pa[-1]],dd[x3pa[-1]]))

        surveyRes,ourRes=[],[]

        for i in range(1,13):
            surveyRes = self.survey_answer[(i-1)]

            if i in [1,3,8]:
                ourRes = list(riskPs[i-1])

            elif i in [2,4,5,6,11,12]:
                ourRes = list(effectivenessPs[i-1])

            elif i==7:
                ourRes = list(gcPs[i-1])

            elif i in [9,10]:
                ourRes = list(effectivenessPs[i-1])
                ourRes[0],ourRes[2] = ourRes[2],ourRes[0]


            print "Q"+str(i),"::::",ourRes,surveyRes,
            if surveyRes!=ourRes:
                print "*"
            else:
                print ""



if __name__ == "__main__":
    # sol=[899.0, 503.0, 474.0]
    # sol=[1, 5]
    # sol=[11, 2, 2298]
    # sol=[6, -2, 3910]
    sol=[489, 975, 572]
    q=SurveyAnalyse(sol)
    q.Write_to_csv()
    q.sortPossitions()
    q.convertPs()



#score 22
# Q1 :::: ['P3', 'P2', 'P1'] ['P3', 'P2', 'P1']
# Q2 :::: ['P1', 'P3', 'P2'] ['P2', 'P3', 'P1'] *
# Q3 :::: ['P2', 'P1', 'P3'] ['P2', 'P1', 'P3']
# Q4 :::: ['P3', 'P1', 'P2'] ['P3', 'P2', 'P1'] *
# Q5 :::: ['P2', 'P1', 'P3'] ['P2', 'P1', 'P3']
# Q6 :::: ['P1', 'P2', 'P3'] ['P1', 'P2', 'P3']
# Q7 :::: ['P2', 'P1', 'P3'] ['P2', 'P1', 'P3']
# Q8 :::: ['P2', 'P1', 'P3'] ['P2', 'P1', 'P3']
# Q9 :::: ['P2', 'P3', 'P1'] ['P2', 'P3', 'P1']
# Q10 :::: ['P2', 'P3', 'P1'] ['P2', 'P3', 'P1']
# Q11 :::: ['P3', 'P1', 'P2'] ['P2', 'P3', 'P1'] *
# Q12 :::: ['P3', 'P1', 'P2'] ['P3', 'P1', 'P2']


#score 24
# Q1 :::: ['P3', 'P2', 'P1'] ['P3', 'P2', 'P1']
# Q2 :::: ['P1', 'P3', 'P2'] ['P2', 'P3', 'P1'] *
# Q3 :::: ['P2', 'P1', 'P3'] ['P2', 'P1', 'P3']
# Q4 :::: ['P3', 'P1', 'P2'] ['P3', 'P2', 'P1'] *
# Q5 :::: ['P2', 'P1', 'P3'] ['P2', 'P1', 'P3']
# Q6 :::: ['P1', 'P2', 'P3'] ['P1', 'P2', 'P3']
# Q7 :::: ['P2', 'P1', 'P3'] ['P2', 'P1', 'P3']
# Q8 :::: ['P2', 'P1', 'P3'] ['P2', 'P1', 'P3']
# Q9 :::: ['P2', 'P3', 'P1'] ['P2', 'P3', 'P1']
# Q10 :::: ['P2', 'P3', 'P1'] ['P2', 'P3', 'P1']
# Q11 :::: ['P1', 'P3', 'P2'] ['P2', 'P3', 'P1'] *
# Q12 :::: ['P3', 'P1', 'P2'] ['P3', 'P1', 'P2']

#last
# Q1 :::: ['P3', 'P2', 'P1'] ['P3', 'P2', 'P1']
# Q2 :::: ['P1', 'P2', 'P3'] ['P2', 'P3', 'P1'] *
# Q3 :::: ['P2', 'P1', 'P3'] ['P2', 'P1', 'P3']
# Q4 :::: ['P3', 'P1', 'P2'] ['P3', 'P2', 'P1'] *
# Q5 :::: ['P2', 'P1', 'P3'] ['P2', 'P1', 'P3']
# Q6 :::: ['P1', 'P2', 'P3'] ['P1', 'P2', 'P3']
# Q7 :::: ['P2', 'P1', 'P3'] ['P2', 'P1', 'P3']
# Q8 :::: ['P1', 'P2', 'P3'] ['P2', 'P1', 'P3'] *
# Q9 :::: ['P2', 'P3', 'P1'] ['P2', 'P3', 'P1']
# Q10 :::: ['P2', 'P3', 'P1'] ['P2', 'P3', 'P1']
# Q11 :::: ['P2', 'P3', 'P1'] ['P2', 'P3', 'P1']
# Q12 :::: ['P3', 'P1', 'P2'] ['P3', 'P1', 'P2']