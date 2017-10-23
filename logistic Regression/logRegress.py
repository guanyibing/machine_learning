# -*- coding:utf8 -*-
from numpy import *
def loadDataSet():
    f=open('testSet.txt')
    dataMat=[]
    labelMat=[]
    for line in f.readlines():
        lineArr=line.strip().split('\t')
        dataMat.append([1.0,float(lineArr[0]),float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat,labelMat

def sigmoid(inX):
    return 1.0/(1+exp(-inX))

def gradAscent(dataMatIn,classLabel,maxIter):
    dataMatrix=mat(dataMatIn)
    labelMatrix=mat(classLabel).transpose()
    m,n=dataMatrix.shape
    weights=ones((n,1))
    alpha=0.001
    for i in range(maxIter):
        h=sigmoid(dataMatrix*weights)
        error=labelMatrix-h
        weights=weights+alpha*dataMatrix.transpose()*error
    return weights

# dataMat,labelMat=loadDataSet()
# weights=gradAscent(dataMat,labelMat,500)
# print weights


#随机梯度上升算法，对于大数据，每次更新回归数据都遍历一遍整个数据集的话，计算量过大
def stocGradAscent(dataMat,labelMat,maxIter):
    dataArr=array(dataMat)
    m,n=shape(dataArr)
    weights=ones(n)
    for j in range(maxIter):
        for i in range(m):
            alpha=4/(1+i+j)+0.01
            randIndex=int(random.uniform(0,m))
            h=sigmoid(sum(dataArr[randIndex]*weights))
            error=labelMat[randIndex]-h
            weights=weights+alpha*error*dataArr[randIndex]
    return weights
dataMat,labelMat=loadDataSet()  
weights=stocGradAscent(dataMat,labelMat,200)



def plotBestFit(weights):
    import matplotlib.pyplot as plt
    dataMat,labelMat=loadDataSet()
    dataArr=array(dataMat)
    m=dataArr.shape[0]
    x1=[];y1=[]
    x2=[];y2=[]
    for i in range(m):
        if labelMat[i]==1:
            x1.append(dataMat[i][1])
            y1.append(dataMat[i][2])
        if labelMat[i]==0:
            x2.append(dataArr[i,1])
            y2.append(dataArr[i,2])

    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.scatter(x1,y1,s=30,c='red',marker='s')
    ax.scatter(x2,y2,s=30,c='green')
    x=arange(-3.0,3.0,0.1)
    y=(-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x,y.T)
    plt.show()

# plotBestFit(weights)

def classifyVector(inX,weights):
    prob=sigmoid(sum(inX*weights))
    if prob>0.5:return 1
    else:return 0

def colicTest():
    trainingSet=[]
    trainingLabels=[]
    fTrain=open("horseColicTraining.txt")
    for line in fTrain.readlines():
        list=line.strip().split('\t')
        listFloat=[]
        for i in range(len(list)-1):
            listFloat.append(float(list[i]))
        trainingSet.append(listFloat)
        trainingLabels.append(float(list[-1]))
    weights=stocGradAscent(trainingSet,trainingLabels,500)
    fTest=open("horseColicTest.txt")
    numTestVec=0.0
    errorcount=0.0
    for line in fTest.readlines():
        numTestVec+=1
        list=line.strip().split("\t")
        lineFloat=[]
        for i in range(len(list)-1):
            lineFloat.append(float(list[i]))
        if int(classifyVector(array(lineFloat),weights))!=int(list[-1]):
            errorcount+=1
    errorRate=errorcount/numTestVec
    print ("the error rate is:%sf"%errorRate)
    return errorRate

def multiTest():
    numTests=10
    errorSum=0.0
    for i in range(numTests):
        errorSum+=colicTest()
    print ("After %f iterations the average error rate is %f"%(numTests,errorSum/numTests))

multiTest()


