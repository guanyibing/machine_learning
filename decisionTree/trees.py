# -*- coding:utf8 -*-
import pickle
from math import log
import operator
import copy

def calShannonEnt(dataSet):
    numEntries=len(dataSet)
    labelCounts={}
    for featVec in dataSet:
        currentLabel=featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel]=1
        else:
            labelCounts[currentLabel]+=1
    shannonEnt=0.0
    for key in labelCounts.keys():
        prob=float(labelCounts[key])/numEntries
        shannonEnt -= prob*log(prob)
    return shannonEnt
def createDataSet():
    dataSet=[
        [1,1,'yes'],
        [1,1,'yes'],
        [1,0,'no'],
        [0,1,'no'],
        [0,1,'no']
    ]
    labels=['no surfacing','flippers']
    return dataSet,labels

# dataSet,labels=createDataSet()
# dataSet[0][-1]='maybe'
# shannonEnt=calShannonEnt(dataSet)
# print shannonEnt

def splitDataSet(dataSet,axis,value):
    retDataSet=[]
    for featVec in dataSet:
        if featVec[axis]==value:
            reducedFeatVec=featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

# retDataSet=splitDataSet(dataSet,0,1)
# print retDataSet

def chooseBestFeatureToSplit(dataSet):
    numFeature=len(dataSet[0])-1
    baseEntropy=calShannonEnt(dataSet)
    bestInfoGain=0.0
    bestFeature=-1
    for i in range(numFeature):
        featureValues=[example[i] for example in dataSet]
        uniqueValues=set(featureValues)
        newEntropy=0.0
        for value in uniqueValues:
            subDataSet=splitDataSet(dataSet,i,value)
            prob=(len(subDataSet))/float(len(dataSet))
            newEntropy += prob*calShannonEnt(subDataSet)
        infoGain=baseEntropy-newEntropy
        if infoGain>bestInfoGain:
            bestInfoGain=infoGain
            bestFeature=i
    return bestFeature
# print chooseBestFeatureToSplit(dataSet)

def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote]=1
        else:
            classCount[vote]+=1
    sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):
      classList=[example[-1] for example in dataSet]
      if classList.count(classList[0])==len(classList):#类别只有一种
          return classList[0]
      if len(dataSet[0])==1:
          return majorityCnt(classList)
      bestFeat=chooseBestFeatureToSplit(dataSet)
      bestFeatLabel=labels[bestFeat]
      myTree={bestFeatLabel:{}}
      del labels[bestFeat]
      featValues=[example[bestFeat] for example in dataSet]
      uniqueValues=set(featValues)
      for value in uniqueValues:
          subLabels=copy.copy(labels)#labels[:]
          splitedDataSet=splitDataSet(dataSet,bestFeat,value)
          myTree[bestFeatLabel][value]=createTree(splitedDataSet,subLabels)
      return myTree
#创建分类器
def classify(myTree,labels,testVec):
    firstFloor=myTree.keys()[0]
    secondDict=myTree[firstFloor]
    featIndex=labels.index(firstFloor)
    classLabel=''
    for key in secondDict.keys():
        if testVec[featIndex]==key:
            if type(secondDict[key]).__name__=="dict":
                classLabel=classify(secondDict[key],labels,testVec)
            else:classLabel=secondDict[key]
    return classLabel
# dataSet,labels=createDataSet()
# myTree=createTree(dataSet,labels)#有对labels进行删除操作
# dataSet,labels=createDataSet()
# classLabel=classify(myTree,labels,[1,0])
# print classLabel

def storeTree(myTree,fileName):
    fw=open(fileName,"w")
    pickle.dump(myTree,fw)
    fw.close()
def grapTree(fileName):
    fr=open(fileName)
    myTree=pickle.load(fr)
    return myTree
# storeTree(myTree,"treeStore.txt")
# print grapTree("treeStore.txt")

#使用决策树预测隐形眼镜类型
fr=open("lenses.txt")
lenses=[lens.strip().split("\t") for lens in fr.readlines()]
lensLabels=["age","prescript","astigmatic","tearRate"]
myTree= createTree(lenses,lensLabels)
print (myTree)
storeTree(myTree,"glasses.txt")