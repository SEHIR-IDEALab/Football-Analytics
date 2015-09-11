import math

__author__ = 'aliuzun'
from Survey_Read import *

q=Survey()


class FriedmanTest():
    def __init__(self):
        self.container=[]
        self.order=['P1', 'P2', 'P3']
        self.all_average = []
        self.k = 3.0 # number of categories /1,2,3
        self.n = None

    def convert_number(self):
        data=q.separate_Q()
        for ans in data:
            tmp_cont=[]
            for c in ans:
                tmp_dict={}
                for index,item in enumerate(c):
                    if index==0:
                        tmp_dict[item]=3
                    if index==1:
                        tmp_dict[item]=2
                    if index==2:
                        tmp_dict[item]=1
                tmp_cont.append(tmp_dict)
            self.container.append(tmp_cont)
        # return self.container


    def get_average(self,data):
        average=[]
        s=0
        for p in self.order:
            counter=0
            for di in data:
                if len(di.keys()) == 3:
                    s+=di[p]
                    counter+= 1        # n
            average.append(s*1.0/counter)
            self.n = counter
            s=0
        return average

    def get_r(self,data):
        return sum(self.get_average(data))/self.k


    def get_SSt(self,data):
        SSt=0
        for i in range(3):
            SSt+=self.n*(math.pow((self.get_average(data)[i]-self.get_r(data)),2))
        return SSt

    def get_SSe(self,data):
        tmp_val=0
        for p in self.order:
            for dic in data:
                if len(dic.keys())==3:
                    # print dic[p]
                    tmp_val+=math.pow((dic[p]-self.get_r(data)),2)
        return tmp_val*(1.0/(self.n*(self.k-1)))

    def get_Q_value(self,data):
        return self.get_SSt(data)/self.get_SSe(data)

    def get_p_value(self,data):
        print self.n ,"nnnn"
        T=self.n*3*3/2.0
        A=0
        p=3
        result=0
        for po in self.order:
            for dic in data:
                if len(dic.keys())==3:
                    A+=math.pow(dic[po],2)

        C=self.n*p*math.pow((p+1),2)/4.0
        val1=(p-1)/(A-C)
        # print A,C
        for i in range(p):
            result+=val1*math.pow((self.get_average(data)[i]*self.n/T-self.n*(p+1)/2.0),2)
        return result



    def new_Q(self,data):
        Rj=[]
        for i in self.get_average(data):
            i=i*self.n
            Rj.append(i)
        print Rj
        const=12.0/(self.n*self.k*(self.k+1))
        tmp_val=0
        for i in range(len(Rj)):
            # print Rj[i]
            tmp_val+=pow(Rj[i],2)-3*self.n*(self.k+1)
        return const*tmp_val



if __name__ == "__main__":
    w=FriedmanTest()
    print w
    # d2=w.convert_number()[0]
    # print d2
    # d=d2.convert_number()
    # cs=[]
    # pv=[]
    # new_cs=[]
    # print w.get_average(d)
    # print d
    # print w.get_SSt(d2),w.get_SSe(d2)
    # print w.get_Q_value(d2)
    # print len(d),"---"
    # for l in d:
    #     w.get_average(l),"average",w.get_r(l)
    #     w.get_Q_value(l),w.new_Q(l),"Q"
    #     # print "------------------"
    #     cs.append(w.get_Q_value(l))
    #     pv.append(w.get_p_value(l))
    #     new_cs.append(w.new_Q(l))
    # print cs
    # print pv
    # print new_cs




