from src.sentio.gui.SnapShot import SnapShot
from src.sentio.pass_evaluate.Pass import Pass
import csv

__author__ = 'doktoray'


import glob

def main():
    aaa=list()
    aaa.extend(["Q #","overal_risk","gain","pass_advantages","goal_chance","effectiveness_score"])
    out = csv.writer(open("PossitionsInfo.csv","a"), delimiter='\t', quoting=csv.QUOTE_NONE)
    out.writerow(aaa)
    PosDict={}
    del aaa[:]
    i=0
    tmp_overallRisk, tmp_gain, tmp_pass_advantages, tmp_goalChance, tmp_effectiveness=0,0,0,0,0
    for file_path in glob.glob('../SampleScenarios/Positions/*.csv'):
        Q=file_path[len(file_path)-8:len(file_path)-4]
        snapShot = SnapShot(file_path)
        teams = snapShot.loadTeams()
        defined_passes = snapShot.getLoadedPassesFor(teams)
        pas = Pass()
        pas.teams = teams
        for pass_event in defined_passes:
            p1, p2 = pass_event.pass_source, pass_event.pass_target
            overallRisk, gain, pass_advantages, goalChance, effectiveness = pas.effectiveness_withComponents(p1,p2)
            if Q not in PosDict:
                PosDict[Q]=[Q,overallRisk, gain, pass_advantages, goalChance, effectiveness]
            else:
                PosDict[Q]=[Q,PosDict[Q][1]+overallRisk, PosDict[Q][2]+gain, PosDict[Q][3]+pass_advantages, PosDict[Q][4]+goalChance, PosDict[Q][5]+effectiveness]

    for Qs in sorted(PosDict.keys()):

        aaa.extend(PosDict[Qs])
        out.writerow(aaa)
        del aaa[:]



def sortPoss():
    risk_info,effectiveness_info,gchange_info,pass_adv=[],[],[],[]
    sorted_risk,sorted_effectiveness,sorted_gc,sorted_pass_adv=[],[],[],[]

    with open("PossitionsInfo.csv") as file:
        file.readline()
        data=csv.reader(file, delimiter="\t")
        for line in data:
            risk_info.append((line[0],float(line[1])))
            gchange_info.append((line[0],float(line[4])))
            effectiveness_info.append((line[0],float(line[5])))
            pass_adv.append((line[0],float(line[3])))

    for i in range(0,33,3):
        sorted_risk.append(sorted(risk_info[i:i+3],key=lambda element: (element[1])))
        sorted_effectiveness.append(sorted(effectiveness_info[i:i+3], reverse=False, key=lambda element: (element[1])))
        sorted_gc.append(sorted(gchange_info[i:i+3], key=lambda element: (element[1])))
        sorted_pass_adv.append(sorted(pass_adv[i:i+3], reverse= True, key=lambda element: (element[1])))
    # print sorted_effectiveness[0]
    return sorted_risk,sorted_effectiveness,sorted_gc,sorted_pass_adv

our_c=[['P2', 'P3', 'P1'],['P3', 'P1', 'P2'],['P2', 'P1', 'P3'], ['P3', 'P1', 'P2'], ['P2', 'P1', 'P3'], ['P3', 'P2', 'P1'], ['P3', 'P1', 'P2'], ['P2', 'P3', 'P1'], ['P2', 'P1', 'P3'], ['P2', 'P3', 'P1'], ['P1', 'P3', 'P2'], ['P3', 'P1', 'P2']]
common_c=[['P3', 'P2', 'P1'],['P2', 'P3', 'P1'],['P2', 'P1', 'P3'], ['P3', 'P2', 'P1'], ['P2', 'P1', 'P3'], ['P1', 'P2', 'P3'], ['P2', 'P1', 'P3'], ['P2', 'P1', 'P3'], ['P2', 'P3', 'P1'], ['P2', 'P3', 'P1'], ['P2', 'P3', 'P1'], ['P3', 'P1', 'P2']]

def convertPs(sorted_risk,sorted_effectiveness,sorted_gc,sorted_pass_adv):
    riskPs,effectivenessPs,gcPs,pass_adv=[],[],[],[]
    dd={"a":"P1","b":"P2","c":"P3"}
    for i in range(10):
        (x1r,y1r),(x2r,y2r),(x3r,y3r)=sorted_risk[i]
        riskPs.append((dd[x1r[-1]],dd[x2r[-1]],dd[x3r[-1]]))

        (x1e,y1e),(x2e,y2e),(x3e,y3e)=sorted_effectiveness[i]
        effectivenessPs.append((dd[x1e[-1]],dd[x2e[-1]],dd[x3e[-1]]))

        (x1g,y1g),(x2g,y2g),(x3g,y3g)=sorted_gc[i]
        gcPs.append((dd[x1g[-1]],dd[x2g[-1]],dd[x3g[-1]]))

        (x1pa,y1pa),(x2pa,y2pa),(x3pa,y3pa)=sorted_pass_adv[i]
        pass_adv.append((dd[x1pa[-1]],dd[x2pa[-1]],dd[x3pa[-1]]))
    #print riskPs,"\n",effectivenessPs, "\n", gcPs
    bb=[riskPs,effectivenessPs,gcPs,pass_adv]
    for i in range(1,13,1):
        if i in [1,3]:
            print "Q0"+str(i),"::::", bb[0][i/2],"<=>",common_c[i-1]
        elif i in [2,4]:
            print "Q0"+str(i),"::::", bb[1][(i-1)/2],"<=>",common_c[i-1]

        elif i in [6,8]:
            print "Q0"+str(i),"::::", bb[0][i-3],"<=>",common_c[i-1]
        elif i in [9,11,12]:
            print "Q0"+str(i),"::::", bb[1][i-3],"<=>",common_c[i-1]

        elif i==7:
            bb2=[bb[1][i-3][2],bb[1][i-3][1],bb[1][i-3][0]]
            print "Q0"+str(i),"::::", bb2,"<=>",common_c[i-1]

        elif i==5:
            print "Q0"+str(i),"::::", bb[3][i-3],"<=>",common_c[i-1]

        elif i==10:
            print "Q"+str(i),"::::", bb[2][i-3],"<=>",common_c[i-1]






if __name__ == "__main__":
    # main()
    # get_Double()
    # reWritetoFile()
    r,e,c,p=sortPoss()
    convertPs(r,e,c,p)


