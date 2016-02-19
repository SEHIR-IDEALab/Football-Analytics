import csv
import math
from src.sentio.Sklearn.Survey_Read import Survey
from SurveyAnalysis.analyse2 import *


__author__ = 'aliuzun'



q=Survey()

class ScoreCal():

    def __init__(self):
        # a=SurveyAnalyse()
        # a.Write_to_csv()
        # a.sortPossitions()
        # self.our_answer=a.get_result_list()
        self.survey_answer=[['P3', 'P2', 'P1'],['P2', 'P3', 'P1'],['P2', 'P1', 'P3'], ['P3', 'P2', 'P1'], ['P2', 'P1', 'P3'], (['P1', 'P2', 'P3'],['P3', 'P2', 'P1']), ['P2', 'P1', 'P3'], ['P2', 'P1', 'P3'], ['P2', 'P3', 'P1'], ['P2', 'P3', 'P1'], ['P2', 'P3', 'P1'], (['P3', 'P1', 'P2'],['P1', 'P3', 'P2'])]
        # self.survey_answer=[['P3', 'P2', 'P1'],['P2', 'P3', 'P1'],['P2', 'P1', 'P3'], ['P3', 'P2', 'P1'], ['P2', 'P1', 'P3'], ['P1', 'P2', 'P3'], ['P2', 'P1', 'P3'], ['P2', 'P1', 'P3'], ['P2', 'P3', 'P1'], ['P2', 'P3', 'P1'], ['P2', 'P3', 'P1'], ['P3', 'P1', 'P2']]
        # self.our_answer=None



    def convert_Q_Num(self,Q):
        data=[]
        for cc in Q:
            tmp_list=[]
            if len(cc)==3:
                for index,P in enumerate(cc):
                    if P=='P1':
                        cc[index]=1
                    elif P=='P2':
                        cc[index]=2
                    elif P=='P3':
                        cc[index]=3
                tmp_list.extend(cc)
            if len(tmp_list)==3:
                data.append(tmp_list)
        return data

    def convert_all(self):
        data=[]
        for Q in  q.separate_Q():
            data.append(self.convert_Q_Num(Q))
        return data


    def DisstanceCalculation(self):
        k=0
        score_list=[]
        num_cevap=self.convert_Q_Num(self.our_answer)
        # while k <12:
        tmp_list=[]
        # for g in self.convert_all()[k]:
        for g in self.convert_Q_Num(self.survey_answer):
            score = "%.2f" % (math.sqrt(math.pow(math.fabs(num_cevap[k][0]-g[0]),2) + math.pow(math.fabs(num_cevap[k][1]-g[1]),2) + math.pow(math.fabs(num_cevap[k][2]-g[2]),2)))
            tmp_list.append(score)
            # tmp_list.append(math.sqrt(tmp_sum))
        # score_list.append(tmp_list)
            # k+=1
        return tmp_list

    def NewDisstanceCal(self):
        num_cevap=self.convert_Q_Num(self.our_answer)
        data=self.convert_Q_Num(self.survey_answer)
        # print num_cevap
        # print data
        k=0
        tmp_list=[]
        while k< 12:
            score = "%.2f" % (math.sqrt(math.pow((math.fabs(num_cevap[k][0]-data[k][0])),2) + math.pow(math.fabs(num_cevap[k][1]-data[k][1]),2) + math.pow(math.fabs(num_cevap[k][2]-data[k][2]),2)))
            tmp_list.append(score)
            k+=1
        return tmp_list

    def getScore(self,survey_answer,our_answer):
        survey_pair=[(survey_answer[0],survey_answer[1]),(survey_answer[0],survey_answer[2]),(survey_answer[1],survey_answer[2])]
        tool_pair=[(our_answer[0],our_answer[1]),(our_answer[0],our_answer[2]),(our_answer[1],our_answer[2])]
        score=0
        # print survey_pair,"s"
        # print tool_pair,"t"
        for pair in tool_pair:
            if pair in survey_pair:
                score=score+1

        return score

    def CostScore2(self,solution,pair):
        i=pair
        a=SurveyAnalyse(solution)
        a.Write_to_csv()
        a.sortPossitions()
        self.our_answer = a.get_result_list()
        k=0
        tmp_list=[]
        # try:
        while k < 12:
            if (k==i):
                pass
            else:
                if k==5 or k==11:
                    sa1,sa2=self.survey_answer[k][0],self.survey_answer[k][1]
                    score1=self.getScore(sa1,self.our_answer[k])
                    score2=self.getScore(sa2,self.our_answer[k])
                    tmp_list.append(max(score1,score2))
                else:
                    score=self.getScore(self.survey_answer[k],self.our_answer[k])
                    tmp_list.append(score)

            k+=1
        # print tmp_list

        return sum(tmp_list)
        # except TypeError:
        #     pass




    def CostScore3(self,solution):
        a=SurveyAnalyse(solution)
        a.Write_to_csv()
        a.sortPossitions()
        self.our_answer = a.get_result_list()
        k=0
        tmp_list=[]

        while k < 12:

            poss_cevap=[(self.our_answer[k][0],self.our_answer[k][1]),(self.our_answer[k][0],self.our_answer[k][2]),(self.our_answer[k][1],self.our_answer[k][2])]

            score=0

            if (self.survey_answer[k][0],self.survey_answer[k][1]) in poss_cevap:
                score+=1

            elif (self.survey_answer[k][0],self.survey_answer[k][2]) in poss_cevap:
                score+=1

            elif (self.survey_answer[k][1],self.survey_answer[k][2]) in poss_cevap:
                score+=1

            score = "%.2f" % score
            tmp_list.append(score)

            k+=1

        return sum(tmp_list)


    def write_to_csv(self,data):
        aaa=list()
        # aaa.extend('sep="/t"')
        # aaa.extend(["Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9","Q10","Q11","Q12"])
        out = csv.writer(open("survey_results4.csv","a"), delimiter='\t', quoting=csv.QUOTE_NONE)
        out.writerow(aaa)
        del aaa[:]

        for index,each in enumerate(data):
            each.insert(0,("Q"+str(index+1)))
            aaa.extend(each)
            out.writerow(aaa)
            del aaa[:]

if __name__ == "__main__":
    a=ScoreCal()
    # print a.convert_Q_Num(cevap)[0]
    # print a.convert_all()[0]
    # print a.DisstanceCalculation()
    # print q.calculate_score()
    # print a.Distance2(cevap2)
    # print a.write_to_csv(a.DisstanceCalculation())
    # print a.write_to_csv(a.Distance2(cevap))
    # print a.NewDisstanceCal()
    print a.CostScore2([1,5])
    # print a.CostScore2([682.0, 708.0, 745.0])
    # print a.CostScore3()
    # for i in range(len(common_c)):
    #     print i+1,"-",our_c[i],"----",self.survey_answer[i],"-->",a.NewDisstanceCal()[i],"--",a.CostScore2()[i],"--",a.CostScore3()[i]







# Q1 :::: ['P3', 'P2', 'P1'] ['P3', 'P2', 'P1'] ++++++
# Q2 :::: ['P2', 'P3', 'P1'] ['P2', 'P3', 'P1']
# Q3 :::: ['P2', 'P1', 'P3'] ['P2', 'P1', 'P3']
# Q4 :::: ['P3', 'P2', 'P1'] ['P3', 'P2', 'P1']
# Q5 :::: ['P2', 'P1', 'P3'] ['P2', 'P1', 'P3']
# Q6 :::: ['P1', 'P2', 'P3'] (['P1', 'P2', 'P3'], ['P3', 'P2', 'P1']) *
# Q7 :::: ['P2', 'P1', 'P3'] ['P2', 'P1', 'P3']
# Q8 :::: ['P1', 'P2', 'P3'] ['P2', 'P1', 'P3'] *
# Q9 :::: ['P3', 'P1', 'P2'] ['P2', 'P3', 'P1'] *
# Q10 :::: ['P2', 'P3', 'P1'] ['P2', 'P3', 'P1']
# Q11 :::: ['P2', 'P1', 'P3'] ['P2', 'P3', 'P1'] *
# Q12 :::: ['P3', 'P2', 'P1'] (['P3', 'P1', 'P2'], ['P1', 'P3', 'P2']) *






