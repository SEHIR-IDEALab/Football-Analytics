import random
import os
from sklearn import svm

__author__ = 'aliuzun'

import csv

dk=0
for i in range(100):
    data1,own1=[],[]
    data0,own0=[],[]
    with open("tests_result/result_test1.csv") as file:
        file.readline()
        data=csv.reader(file, delimiter="\t")
        for line in data:
                try:
                    a=int(line[3])
                    if a==1:
                        tmp=line[4][1:-1].split(",")
                        data1.append([float(i) for i in tmp] )
                        own1.append(1)
                    elif a==0 :
                        data0.append([float(i) for i in tmp])
                        own0.append(0)
                    else:
                        pass
                except ValueError:
                    pass

    #print len(own0),len(own1)
    length_own1=len(own1)
    length_own0=len(own0)
    trainData,own=[],[]
    for i in range(1,210):
        #try:
        index=random.randint(0,(length_own1-i))
        #print index,kk,len(data0)
        trainData.append(data1[index])
        own.append(own1[index])
        data1.pop(index)
        own1.pop(index)

    for i in range(1,210):
        #try:
        index=random.randint(0,(length_own0-i))
        trainData.append(data0[index])
        own.append(own0[index])
        data0.pop(index)
        own0.pop(index)



    testdata,realvalues=[],[]
    testdata.extend(data1[:15] + data0[:15])
    realvalues.extend(own1[:15] + own0[:15])


    #clf=svm.SVC(degree=3,kernel='poly',gamma=0.0)
    clf=svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=3,
    gamma=0.05, kernel='rbf', max_iter=-1, probability=False,
    random_state=None, shrinking=True, tol=0.001, verbose=False)
    clf.fit(trainData,own)
    predicted=[]
    for data in testdata:
        predicted.extend(clf.predict(data))
    kl=0
    for i in range(len(predicted)):
        if predicted[i] != realvalues[i]:
            kl+=1
    dk+=kl
    print kl,len(predicted),len(own)
print dk/100.0





