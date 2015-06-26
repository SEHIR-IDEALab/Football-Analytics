import csv
import math

__author__ = 'aliuzun'

cevap=[['P2', 'P3', 'P1'],['P3', 'P1', 'P2'],['P2', 'P1', 'P3'], ['P3', 'P1', 'P2'], ['P2', 'P1', 'P3'], ['P2', 'P3', 'P1'], ['P3', 'P1', 'P2'], ['P3', 'P1', 'P2'], ['P2', 'P1', 'P3'], ['P2', 'P3', 'P1'], ['P1', 'P3', 'P2'], ['P3', 'P2', 'P1']]

cevap2=[['P3', 'P2', 'P1'],['P2', 'P3', 'P1'],['P2', 'P1', 'P3'], ['P3', 'P2', 'P1'], ['P2', 'P1', 'P3'], ['P1', 'P2', 'P3'], ['P2', 'P1', 'P3'], ['P2', 'P1', 'P3'], ['P2', 'P3', 'P1'], ['P2', 'P3', 'P1'], ['P2', 'P3', 'P1'], ['P3', 'P1', 'P2']]


class Survey():
    def __init__(self):
        pass
    def get_answer(self):
        with open("tests_result/new_data.csv") as file:
            file.readline()
            data=csv.reader(file, delimiter="\t")
            answer_all=[]
            for line in data:
                na=[]
                for a in line[0].split(";"):
                    na.append(a.split("-"))
                answer_all.append(na)
        return answer_all


    def separate_Q(self):
        i=0
        q_seperated=[]

        while i<12:
            a=[]
            for person in self.get_answer():
                a.append(person[i])
            q_seperated.append(a)
            i+=1
        return q_seperated

    def calculate_score(self):
        k=0
        score_list=[]
        score=0
        while k < 12:
            # score=0
            poss_cevap=[(cevap[k][0],cevap[k][1]),(cevap[k][0],cevap[k][2]),(cevap[k][1],cevap[k][2])]
            # print poss_cevap
            for g in self.separate_Q()[k]:
                try:
                    if (g[0],g[1]) in poss_cevap:
                        score+=1
                    if (g[0],g[2]) in poss_cevap:
                        score+=1
                    if (g[1],g[2]) in poss_cevap:
                        score+=1
                except:
                    IndexError
            score_list.append(score)
            k+=1

        return score



        # while k < 12:
        #     for index,p in enumerate(cevap[k]):
        #         print p
        #         tmp_list=[]
        #         for g in self.separate_Q()[k]:
        #             tmp_scr=0
        #             if len(g)==3:
        #                 for index2,cev in enumerate(g):
        #                     if p==cev:
        #                         tmp_scr+=math.pow(math.fabs(index-index2),2)
        #                 tmp_list.append(math.sqrt(tmp_scr))
        #     score_list.append(tmp_list)
        #     k+=1
        # return score_list











if __name__ == "__main__":
    q=Survey()
    print q.separate_Q()
    # print q.calculate_score()
    # print q.DisstanceCal()