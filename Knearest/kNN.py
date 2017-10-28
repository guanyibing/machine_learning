from __future__ import division
from numpy import *
import operator
import matplotlib.pyplot as plt
import os
def classify0(inX,dataSet,labels,k):
    dataSize=dataSet.shape[0]
    diffMat=tile(inX,(dataSize,1))-dataSet
    sqdiffMat=diffMat**2
    sqdistance=sqdiffMat.sum(axis=1)
    distance=sqdistance**0.5
    sortedDistanceIndices=distance.argsort()
    classCount={}
    for i in range(k):
        voteIlabel=labels[sortedDistanceIndices[i]]
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1
    sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]
def file2matrix(filename):
    f=open(filename)
    lines=f.readlines()
    numberofLines=len(lines)
    returnMat=zeros((numberofLines,3))
    classLabelVector=[]
    index=0
    for line in lines:
        line.replace('\n',' ')
        line.strip()
        listFromLine=line.split('\t')
        returnMat[index,0:3]=listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index+=1
    return returnMat,classLabelVector
# datingMatrix,datingLabels=file2matrix("datingTestSet2.txt")
# print datingMatrix,datingLabels
# fig=plt.figure(figsize=(8,8))
# ax=fig.add_subplot(111)
# ax.scatter(datingMatrix[:,1],datingMatrix[:,2],15*array(datingLabels),15*array(datingLabels))
# plt.show()
def autoNorm(dataSet):
     minVals=dataSet.min(0)
     maxVals=dataSet.max(0)
     ranges=maxVals-minVals
     m=dataSet.shape[0]
     normalDataSet=zeros(shape(dataSet))
     normalDataSet=(dataSet-tile(minVals,(m,1)))/tile(ranges,(m,1))
     return normalDataSet,minVals,ranges
def datingClassTest():
    hoRatio=0.10
    datingDataMat,datingLabels=file2matrix("datingTestSet2.txt")
    normalMat=autoNorm(datingDataMat)
    m=normalMat.shape[0]
    numTestVecs=int(m*hoRatio)
    errorcount=0
    for i in range(numTestVecs):
        classfierresult=classify0(normalMat[i,:],normalMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print ("the classifier come back with:%d,the real answer is :%d"%(classfierresult,datingLabels[i]))
        if classfierresult!=datingLabels[i]:
            errorcount+=1
    print (errorcount)
    print (numTestVecs)
    print ("the total error rate is %f"%(errorcount/numTestVecs))
# datingClassTest()

def classifyPerson():
    resultList=['not at all','in small does','in large does']
    percentGames=float(input('percentage of time spending playing games:'))
    flymiles=float(input("frequent flier miles earned per year:"))
    icecream=float(input("liters of icecream consumed per year:"))
    inputarray=array([percentGames,flymiles,icecream])
    datingMat,datingLabels=file2matrix('datingTestSet2.txt')
    normalMat,minVals,ranges=autoNorm(datingMat)
    classifyresult=classify0((inputarray-minVals)/ranges,normalMat,datingLabels,3)
    print ("The answer is %s"%resultList[classifyresult-1])
# classifyPerson()

def img2vector(filename):
    f=open(filename)
    returnvector=zeros([1,1024])
    for i in range(32):
        line=f.readline()
        for j in range(32):
            returnvector[0,32*i+j]=line[j]
    return returnvector
x=img2vector("trainingDigits\\0_0.txt")
print (x[0,1:20])

def handwritingClassTest():
    hwLabels=[]
    trainingFileList=os.listdir('trainingDigits')
    mtrain=len(trainingFileList)
    trainingMat=zeros([mtrain,1024])
    for i in range(mtrain):
        fileName=trainingFileList[i]
        fileNum=fileName.split('.')[0]
        classNum=int(fileNum.split('_')[0])
        hwLabels.append(classNum)
        trainingMat[i,:]=img2vector('trainingDigits/%s'%fileName)
    testFileList=os.listdir('testDigits')
    mtest=len(testFileList)
    errorcount=0
    for i in range(mtest):
        fileName=testFileList[i]
        fileNum=fileName.split(".")[0]
        classNum=int(fileNum.split("_")[0])
        testMat=img2vector('testDigits/%s'%fileName)
        classifyresult=classify0(testMat,trainingMat,hwLabels,3)
        print ("the classify come back is %d,the answer is %d"%(classifyresult,classNum))
        if classifyresult!=hwLabels[i]:
            errorcount+=1
        print ("the total rate is %s"%(errorcount/mtest))

handwritingClassTest()













