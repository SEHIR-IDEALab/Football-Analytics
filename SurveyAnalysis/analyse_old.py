import csv
from src.sentio.gui.SnapShot import SnapShot
from src.sentio.pass_evaluate.Pass import Pass

__author__ = 'doktoray'


import glob

def main():
    aaa=list()
    aaa.extend(["Effectiveness","Gain","Goal_Change","Risk","Overal_Risk"])
    out = csv.writer(open("dd.csv","a"), delimiter='\t', quoting=csv.QUOTE_NONE)
    out.writerow(aaa)
    del aaa[:]
    for file_path in sorted(glob.glob('../SampleScenarios/Possitions/*.csv')):
        print file_path
        snapShot = SnapShot(file_path)
        teams = snapShot.loadTeams()
        defined_passes = snapShot.getLoadedPassesFor(teams)
        # print defined_passes
        pas = Pass(teams)
        for pass_event in defined_passes:
            p1, p2 = pass_event.pass_source, pass_event.pass_target
            # print "%s --> %s" %(p1.getJerseyNumber(), p2.getJerseyNumber())
            effectiveness_score = pas.effectiveness(p1, p2)
            overal_risk=pas.overallRisk(p1,p2)
            pass_advantages=pas.passAdvantage(p1)
            goal_change=pas.goalChance(p1)
            gain=pas.gain(p1,p2)
            # print [overal_risk,gain,pass_advantages,goal_change,effectiveness_score]
            aaa.extend([overal_risk,gain,pass_advantages,goal_change,effectiveness_score])
            out.writerow(aaa)
            del aaa[:]
            print overal_risk,gain,pass_advantages,goal_change,effectiveness_score
        print "Done with this one!!!!"
        print


if __name__ == "__main__":
    main()