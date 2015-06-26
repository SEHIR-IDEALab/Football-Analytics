import csv
import math
from src.sentio.Sklearn.Survey_Read import Survey

__author__ = 'aliuzun'


# our_c=[['P2', 'P3', 'P1'],['P3', 'P1', 'P2'],['P2', 'P1', 'P3'], ['P3', 'P1', 'P2'], ['P2', 'P1', 'P3'], ['P2', 'P3', 'P1'], ['P3', 'P1', 'P2'], ['P3', 'P1', 'P2'], ['P2', 'P1', 'P3'], ['P2', 'P3', 'P1'], ['P1', 'P3', 'P2'], ['P3', 'P2', 'P1']]

our_c=[['P2', 'P3', 'P1'],['P3', 'P1', 'P2'],['P2', 'P1', 'P3'], ['P3', 'P1', 'P2'], ['P2', 'P1', 'P3'], ['P3', 'P2', 'P1'], ['P3', 'P1', 'P2'], ['P2', 'P3', 'P1'], ['P2', 'P1', 'P3'], ['P2', 'P3', 'P1'], ['P1', 'P3', 'P2'], ['P3', 'P1', 'P2']]

common_c=[['P3', 'P2', 'P1'],['P2', 'P3', 'P1'],['P2', 'P1', 'P3'], ['P3', 'P2', 'P1'], ['P2', 'P1', 'P3'], ['P1', 'P2', 'P3'], ['P2', 'P1', 'P3'], ['P2', 'P1', 'P3'], ['P2', 'P3', 'P1'], ['P2', 'P3', 'P1'], ['P2', 'P3', 'P1'], ['P3', 'P1', 'P2']]

q=Survey()

class Compare():

    def __init__(self):
        pass

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
        num_cevap=self.convert_Q_Num(our_c)
        # while k <12:
        tmp_list=[]
        # for g in self.convert_all()[k]:
        for g in self.convert_Q_Num(common_c):
            score = "%.2f" % (math.sqrt(math.pow(math.fabs(num_cevap[k][0]-g[0]),2) + math.pow(math.fabs(num_cevap[k][1]-g[1]),2) + math.pow(math.fabs(num_cevap[k][2]-g[2]),2)))
            tmp_list.append(score)
            # tmp_list.append(math.sqrt(tmp_sum))
        # score_list.append(tmp_list)
            # k+=1
        return tmp_list

    def NewDisstanceCal(self):
        num_cevap=self.convert_Q_Num(our_c)
        data=self.convert_Q_Num(common_c)
        # print num_cevap
        # print data
        k=0
        tmp_list=[]
        while k< 12:
            score = "%.2f" % (math.sqrt(math.pow((math.fabs(num_cevap[k][0]-data[k][0])),2) + math.pow(math.fabs(num_cevap[k][1]-data[k][1]),2) + math.pow(math.fabs(num_cevap[k][2]-data[k][2]),2)))
            tmp_list.append(score)
            k+=1
        return tmp_list

    def D2(self):
        k=0
        score_list=[]
        tmp_list=[]

        while k < 12:
            # score=0
            poss_cevap=[(our_c[k][0],our_c[k][1]),(our_c[k][0],our_c[k][2]),(our_c[k][1],our_c[k][2])]
            # print poss_cevap
            # for g in q.separate_Q()[k]:
                # print g
            # for g in common_c:
            score=0

            if (common_c[k][0],common_c[k][1]) in poss_cevap:
                score+=1
            else:
                score-=1
            if (common_c[k][0],common_c[k][2]) in poss_cevap:
                score+=1
            else:
                score-=1
            if (common_c[k][1],common_c[k][2]) in poss_cevap:
                score+=1
            else:
                score-=1

            score = "%.2f" % score
            tmp_list.append(score)
            # score_list.append(tmp_list)
            # tmp_list=[]
            k+=1

        return tmp_list
    def D3(self):
        k=0
        score_list=[]
        tmp_list=[]

        while k < 12:

            poss_cevap=[(our_c[k][0],our_c[k][1]),(our_c[k][0],our_c[k][2]),(our_c[k][1],our_c[k][2])]

            score=0

            if (common_c[k][0],common_c[k][1]) in poss_cevap:
                score+=1

            if (common_c[k][0],common_c[k][2]) in poss_cevap:
                score+=1

            if (common_c[k][1],common_c[k][2]) in poss_cevap:
                score+=1

            score = "%.2f" % score
            tmp_list.append(score)

            k+=1

        return tmp_list



    # def Distance2(self,cevap):
    #     k=0
    #     score_list=[]
    #     tmp_list=[]
    #
    #     while k < 12:
    #         # score=0
    #         poss_cevap=[(cevap[k][0],cevap[k][1]),(cevap[k][0],cevap[k][2]),(cevap[k][1],cevap[k][2])]
    #         # print poss_cevap
    #         # for g in q.separate_Q()[k]:
    #             # print g
    #         # for g in self.convert_Q_Num(cevap)
    #             if len(g)==3:
    #                 score=0
    #
    #                 if (g[0],g[1]) in poss_cevap:
    #                     score+=1
    #                 else:
    #                     score-=1
    #                 if (g[0],g[2]) in poss_cevap:
    #                     score+=1
    #                 else:
    #                     score-=1
    #                 if (g[1],g[2]) in poss_cevap:
    #                     score+=1
    #                 else:
    #                     score-=1
    #
    #                 score = "%.2f" % score
    #                 tmp_list.append(score)
    #         score_list.append(tmp_list)
    #         tmp_list=[]
    #         k+=1
    #
    #     return score_list

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
    a=Compare()
    # print a.convert_Q_Num(cevap)[0]
    # print a.convert_all()[0]
    # print a.DisstanceCalculation()
    # print q.calculate_score()
    # print a.Distance2(cevap2)
    # print a.write_to_csv(a.DisstanceCalculation())
    # print a.write_to_csv(a.Distance2(cevap))
    print a.NewDisstanceCal()
    print a.D2()
    print a.D3()
    for i in range(len(common_c)):
        print i+1,"-",our_c[i],"----",common_c[i],"-->",a.NewDisstanceCal()[i],"--",a.D2()[i],"--",a.D3()[i]


    # k=1
    # for i in common_c:
    #     print k,"--",i
    #     k=k+1
#[1.4142135623730951, 0.0, 1.4142135623730951, 1.4142135623730951, 0.0, 1.4142135623730951, 2.8284271247461903, 1.4142135623730951, 0.0, 1.4142135623730951, 0.0, 1.4142135623730951, 1.4142135623730951, 1.4142135623730951, 2.449489742783178]


# ['1.41', '2.45', '0.00', '1.41', '0.00', '2.45', '1.41', '1.41', '2.83', '0.00', '1.41', '1.41']
# ['1.41', '2.45', '0.00', '1.41', '0.00', '2.83', '1.41', '2.83', '2.83', '0.00', '1.41', '0.00']

# ['1.00', '-1.00', '3.00', '1.00', '3.00', '-1.00', '-3.00', '-3.00', '1.00', '3.00', '-3.00', '1.00']
# ['1.00', '-1.00', '3.00', '1.00', '3.00', '-3.00', '-3.00', '1.00', '1.00', '3.00', '-3.00', '3.00']

# ['2.00', '1.00', '3.00', '2.00', '3.00', '1.00', '0.00', '0.00', '2.00', '3.00', '0.00', '2.00']
# ['2.00', '1.00', '3.00', '2.00', '3.00', '0.00', '0.00', '2.00', '2.00', '3.00', '0.00', '3.00']