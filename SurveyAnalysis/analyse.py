from src.sentio.gui.SnapShotCSV import SnapShot
from src.sentio.pass_evaluate.Pass import Pass
# from src.sentio.pass_evaluate.Pass2 import Pass
import csv
import glob

our_c=[['P2', 'P3', 'P1'],['P3', 'P1', 'P2'],['P2', 'P1', 'P3'], ['P3', 'P1', 'P2'], ['P2', 'P1', 'P3'], ['P3', 'P2', 'P1'], ['P3', 'P1', 'P2'], ['P2', 'P3', 'P1'], ['P2', 'P1', 'P3'], ['P2', 'P3', 'P1'], ['P1', 'P3', 'P2'], ['P3', 'P1', 'P2']]
common_c=[['P3', 'P2', 'P1'],['P2', 'P3', 'P1'],['P2', 'P1', 'P3'], ['P3', 'P2', 'P1'], ['P2', 'P1', 'P3'], ['P1', 'P2', 'P3'], ['P2', 'P1', 'P3'], ['P2', 'P1', 'P3'], ['P2', 'P3', 'P1'], ['P2', 'P3', 'P1'], ['P2', 'P3', 'P1'], ['P3', 'P1', 'P2']]



def main():
    aaa=list()
    aaa.extend(["Q #","overal_risk","gain","pass_advantages","goal_chance","effectiveness_score"])
    out = csv.writer(open("test2.csv","w"), delimiter='\t', quoting=csv.QUOTE_NONE)
    out.writerow(aaa)
    PosDict={}
    del aaa[:]
    for file_path in glob.glob('../SampleScenarios/Positions/*.csv'):
        Q=file_path[len(file_path)-8:len(file_path)-4]

        # status=getStatus(Q)

        snapShot = SnapShot(file_path)
        teams = snapShot.loadTeams()
        defined_passes = snapShot.getLoadedPassesFor(teams)
        pas = Pass()
        pas.teams = teams
        for pass_event in defined_passes:
            p1, p2 = pass_event.pass_source, pass_event.pass_target
            overallRisk, gain, pass_advantages,pa_player, goalChance, effectiveness = pas.effectiveness_withComponents(p1,p2)
            if Q not in PosDict:
                PosDict[Q]=[Q,overallRisk, gain, pass_advantages, goalChance, effectiveness]
            else:
                PosDict[Q]=[Q,PosDict[Q][1]+overallRisk, PosDict[Q][2]+gain, PosDict[Q][3]+pass_advantages, PosDict[Q][4]+goalChance, PosDict[Q][5]+effectiveness]

    for Qs in sorted(PosDict.keys()):

        aaa.extend(PosDict[Qs])
        out.writerow(aaa)
        del aaa[:]

def getStatus(file):
    noRisk=["Q01a","Q01b","Q01c","Q02a","Q02b","Q02c","Q05a","Q05b","Q05c","Q03a","Q03b","Q03c","Q10a","Q10b","Q10c"]
    if file in noRisk:
        return True
    else: return False

def sortPoss():
    risk_info,effectiveness_info,gchange_info,pass_adv=[],[],[],[]
    sorted_risk,sorted_effectiveness,sorted_gc,sorted_pass_adv=[],[],[],[]

    # with open("PossitionsInfo.csv") as file:
    with open("test2.csv") as file:
        file.readline()
        data=csv.reader(file, delimiter="\t")
        for line in data:
            risk_info.append((line[0],float(line[1])))
            gchange_info.append((line[0],float(line[4])))
            effectiveness_info.append((line[0],float(line[5])))
            pass_adv.append((line[0],float(line[3])))

    for i in range(0,30,3):
        sorted_risk.append(sorted(risk_info[i:i+3],key=lambda element: (element[1])))
        sorted_effectiveness.append(sorted(effectiveness_info[i:i+3], reverse=True, key=lambda element: (element[1])))
        sorted_gc.append(sorted(gchange_info[i:i+3],reverse=True, key=lambda element: (element[1])))
        sorted_pass_adv.append(sorted(pass_adv[i:i+3], reverse= True, key=lambda element: (element[1])))
    # print sorted_effectiveness
    # print sorted_risk
    # print sorted_gc
    # print sorted_pass_adv
    return sorted_risk,sorted_effectiveness,sorted_gc,sorted_pass_adv


def convertPs(sorted_risk,sorted_effectiveness,sorted_gc,sorted_pass_adv):
    riskPs,effectivenessPs,gcPs,pass_adv=[],[],[],[]
    dd={"a":"P1","b":"P2","c":"P3"}
    for i in range(10):
        (x1r,y1r),(x2r,y2r),(x3r,y3r)=sorted_risk[i]
        riskPs.append((dd[x1r[-1]],dd[x2r[-1]],dd[x3r[-1]]))
        # print sorted_risk[i],"==>",(x1r,x2r,x3r),"==>",(dd[x1r[-1]],dd[x2r[-1]],dd[x3r[-1]])

        (x1e,y1e),(x2e,y2e),(x3e,y3e)=sorted_effectiveness[i]
        effectivenessPs.append((dd[x1e[-1]],dd[x2e[-1]],dd[x3e[-1]]))

        # print sorted_effectiveness[i],"==>",(x1e,x2e,x3e),"==>",(dd[x1e[-1]],dd[x2e[-1]],dd[x3e[-1]])
        (x1g,y1g),(x2g,y2g),(x3g,y3g)=sorted_gc[i]
        gcPs.append((dd[x1g[-1]],dd[x2g[-1]],dd[x3g[-1]]))

        (x1pa,y1pa),(x2pa,y2pa),(x3pa,y3pa)=sorted_pass_adv[i]
        pass_adv.append((dd[x1pa[-1]],dd[x2pa[-1]],dd[x3pa[-1]]))

    surveyRes,ourRes=[],[]

    # bb=[riskPs,effectivenessPs,gcPs,pass_adv]
    for i in range(1,12):
        surveyRes = common_c[(i-1)]
        if i in [1,3]:
            ourRes = list(riskPs[i/2])
        elif i in [2,4]:
            ourRes = list(effectivenessPs[(i/2)-1])
        elif i in [6,8]:
            ourRes = list(riskPs[i-3])
        elif i in [11,5]:
            ourRes = list(effectivenessPs[i-3])
        elif i==7:
            ourRes = list(gcPs[i-3])

        elif i == 9:
            ourRes = list(effectivenessPs[i-3])
            ourRes[0],ourRes[2] = ourRes[2],ourRes[0]

        elif i==10:
            ourRes=list(effectivenessPs[i-3])
            ourRes[0],ourRes[2] = ourRes[2],ourRes[0]

        print "Q"+str(i),"::::",ourRes,surveyRes,
        if surveyRes!=ourRes:
            print "*"
        else:
            print ""




if __name__ == "__main__":
    main()
    r,e,c,p=sortPoss()
    convertPs(r,e,c,p)

# the looks
# Q1 :::: ['P3', 'P2', 'P1'] ['P3', 'P2', 'P1']
# Q2 :::: ['P2', 'P3', 'P1'] ['P2', 'P3', 'P1']  new
# Q3 :::: ['P2', 'P1', 'P3'] ['P2', 'P1', 'P3']
# Q4 :::: ['P2', 'P1', 'P3'] ['P3', 'P2', 'P1'] * done
# Q5 :::: ['P2', 'P3', 'P1'] ['P2', 'P1', 'P3'] * done
# Q6 :::: ['P1', 'P2', 'P3'] ['P1', 'P2', 'P3']
# Q7 :::: ['P2', 'P1', 'P3'] ['P2', 'P1', 'P3']
# Q8 :::: ['P2', 'P1', 'P3'] ['P2', 'P1', 'P3']
# Q9 :::: ['P1', 'P2', 'P3'] ['P2', 'P3', 'P1'] *
# Q10 :::: ['P2', 'P3', 'P1'] ['P2', 'P3', 'P1']
# Q11 :::: ['P1', 'P3', 'P2'] ['P2', 'P3', 'P1'] *
#ignore
# Q12 :::: ['P1', 'P3', 'P2'] ['P3', 'P1', 'P2'] *

#-------

# effectiveness with risk 0
# Q2 :::: ['P2', 'P1', 'P3'] ['P2', 'P3', 'P1'] *
# Q4 :::: ['P3', 'P2', 'P1'] ['P3', 'P2', 'P1']
# Q5 :::: ['P2', 'P1', 'P3'] ['P2', 'P1', 'P3']
# Q7 :::: ['P2', 'P1', 'P3'] ['P2', 'P1', 'P3']
# Q9 :::: ['P3', 'P2', 'P1'] ['P2', 'P3', 'P1'] *
# Q11 :::: ['P2', 'P1', 'P3'] ['P2', 'P3', 'P1'] *
#------


# Q2 :::: ['P3', 'P2', 'P1'] ['P2', 'P3', 'P1'] *
# Q4 :::: ['P3', 'P1', 'P2'] ['P3', 'P2', 'P1'] *
# Q5 :::: ['P2', 'P3', 'P1'] ['P2', 'P1', 'P3'] *
# Q9 :::: ['P1', 'P2', 'P3'] ['P2', 'P3', 'P1'] *
# Q11 :::: ['P1', 'P3', 'P2'] ['P2', 'P3', 'P1'] *



# fixed bug in analyse

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
