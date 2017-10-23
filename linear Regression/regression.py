# -*- coding:utf8 -*-
from numpy import *

def loadDataSet(filename):
    dataMat=[]
    labelMat=[]
    f=open(filename)
    for line in f.readlines():
        lineArr=[]
        list=line.strip().split('\t')
        for i in range(len(list)-1):
            lineArr.append(float(list[i]))
        dataMat.append(lineArr)
        labelMat.append(float(list[-1]))
    return dataMat,labelMat

def standRegression(xArr,yArr):
    xMat=mat(xArr)
    yMat=mat(yArr).T
    xTx=xMat.T*xMat
    if linalg.det(xTx)==0:
        print ('the matrix is singular,can not do inverse')
        return
    else:
        weights=xTx.I*xMat.T*yMat
        return weights

xArr,yArr=loadDataSet('ex0.txt')
# ws=standRegression(xArr,yArr)
#
# xMat=mat(xArr)
# yMat=mat(yArr)
# # print yMat[0,:].flatten().A[0]
#
# import matplotlib.pyplot as plt
# fig=plt.figure()
# ax=fig.add_subplot(111)
# ax.scatter(xMat[:,1],yMat.T[:,0],marker='s',s=20)
#
# xCopy=xMat.copy()
# xCopy.sort(0)
# yHat=xCopy*ws
# ax.plot(xCopy[:,1],yHat)
# plt.show()
# print corrcoef(yHat.T,yMat)

def lwlr(testPoint,xArr,yArr,k):
    xMat=mat(xArr)
    yMat=mat(yArr).T
    m=xMat.shape[0]
    weights=mat(eye(m))#weights=eye(m)
    for j in range(m):
        diffMat=testPoint-xMat[j,:]
        weights[j,j]=exp((diffMat*diffMat.T)/(-2.0*k**2))
    xTx=xMat.T*weights*xMat
    if linalg.det(xTx)==0:
        print ("This matrix is singular,can not do inverse")
        return
    ws=xTx.I*xMat.T*weights*yMat
    return testPoint*ws
def lwlrTest(testArr,xArr,yArr,k=1.0):
    m=shape(testArr)[0]
    yHat=zeros(m)
    for i in range(m):
        yHat[i]=lwlr(testArr[i],xArr,yArr,k)
    return yHat

# yHat= lwlrTest(xArr,xArr,yArr,0.01)
# xMat=mat(xArr)
# sortIndex=xMat[:,1].argsort(0)#sortIndex=xMat[:,1].flatten().A[0].argsort()
# xSort=xMat[sortIndex][:,0,:]#xSort=xMat[sortIndex]
# print xSort
# import matplotlib.pyplot as plt
# fig=plt.figure()
# ax=fig.add_subplot(111)
# ax.plot(xSort[:,1],yHat[sortIndex])
# ax.scatter(xMat[:,1],mat(yArr).T,s=2,c='red')
# plt.show()




def rssError(yArr,yHat):
    return ((yArr-yHat)**2).sum()

# abX,abY=loadDataSet("abalone.txt")
# yHat01=lwlrTest(abX[100:199],abX[0:99],abY[0:99],k=0.1)
# yHat1=lwlrTest(abX[100:199],abX[0:99],abY[:99],k=1)
# yHat10=lwlrTest(abX[100:199],abX[0:99],abY[0:99],k=10)
#
# print rssError(abY[100:199],yHat01.T)
# print rssError(abY[100:199],yHat1.T)
# print rssError(abY[100:199],yHat10.T)

#岭回归
def ridgeRegress(xMat,yMat,lam):
    xTx=xMat.T*xMat
    denom=xTx+eye(xMat.shape[1])*lam
    if linalg.det(denom)==0:
        print ("This matrix is singular,can not do inverse")
    ws=denom.I*(xMat.T*yMat)
    return ws

def ridgeTest(xArr,yArr):
    #数据标准化
    xMat=mat(xArr)
    yMat=mat(yArr).T
    yMean=yMat.mean(0)
    yMat=yMat-yMean
    xMean=mean(xMat,0)
    xVar=var(xMat,0)
    xMat=(xMat-xMean)/xVar

    numTest=30
    wsMat=zeros((numTest,xMat.shape[1]))
    for i in range(numTest):
        ws=ridgeRegress(xMat,yMat,lam=exp(i-10))
        # print ws.T
        wsMat[i,:]=ws.T
    return wsMat
#
# abX,abY=loadDataSet("abalone.txt")
# ridgeWeight=ridgeTest(abX,abY)
# import matplotlib.pyplot as plt
# fig=plt.figure()
# ax=fig.add_subplot(111)
# ax.plot(ridgeWeight)
# plt.show()

#向前逐步回归
def stageWise(xArr,yArr,eps=0.1,numIter=100):
    xMat=mat(xArr)
    yMat=mat(yArr).T
    yMean=mean(yMat,0)
    yMat=yMat-yMean
    xMean=mean(xMat,0)
    xVar=var(xMat,0)
    xMat=(xMat-xMean)/xVar
    m,n=xMat.shape
    returnMat=zeros((numIter,n))
    ws=zeros((n,1))
    wsMax=ws.copy()
    for i in range(numIter):
        lowestError=inf
        for j in range(n):
            for sign in [-1,1]:
                wsTest=ws.copy()
                wsTest[j]+=eps*sign
                yTest=xMat*wsTest
                rssE=rssError(yMat.A,yTest.A)
                if rssE<lowestError:
                    lowestError=rssE
                    wsMax=wsTest
        ws= wsMax.copy()
        # print ws.T
        returnMat[i,:]=wsMax.T
    return returnMat

# xArr,yArr=loadDataSet("abalone.txt")
# stageWeights=stageWise(xArr,yArr,0.001,5000)
# import matplotlib.pyplot as plt
# fig=plt.figure()
# fig.add_subplot(111)
# plt.plot(stageWeights)
# plt.show()

#预测乐高玩具价格
#交叉验证岭回归

def  crossValidation(xArr,yArr,numVal=10):
    m=len(yArr)
    indexList=range(m)
    errorMat=zeros((numVal,30))
    for i in range(numVal):
        trainX=[];trainY=[]
        testX=[];testY=[]
        random.shuffle(indexList)
        for j in range(m):
            if j<0.9*m:
                trainX.append(xArr[indexList[j]])
                trainY.append(yArr[indexList[j]])
            else:
                testX.append(xArr[indexList[j]])
                testY.append(yArr[indexList[j]])
        wsMat=ridgeTest(trainX,trainY)
        for k in range(30):
            matTestX=mat(testX)
            #用训练数据将测试数据标准化
            matTrainX=mat(trainX)
            meanTrainX=mean(matTrainX,0)
            trainXVar=var(matTrainX,0)
            matTestX=(matTestX-meanTrainX)/trainXVar
            yEst=matTestX*mat(wsMat[k,:]).T+mean(trainY)
            errorMat[i,k]=rssError(yEst.T.A,array(testY))
    meanError=mean(errorMat,0) #列均值，求的是k值
    # minMean=float(min(meanError))
    # bestWeights=wsMat[nonzero(meanError==minMean)]
    bestWeights=wsMat[argmin(meanError)]
    xMat=mat(xArr)
    varX=var(xMat,0)
    unReg=bestWeights/varX
    print ("The best model from ridge regression is:",unReg)
    return unReg

abX,abY=loadDataSet("abalone.txt")
unReg=crossValidation(abX,abY)
