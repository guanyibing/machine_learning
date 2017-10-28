# -*- coding:utf8 -*-
from numpy import *

def loadDataSet(filename):
    dataMat=[]
    fr=open(filename)
    for line in fr.readlines():
        currLine=line.strip().split('\t')
        currList=list(map(float,currLine))
        dataMat.append(currList)
    return dataMat
def binSplitDataSet(dataSet,feature,value):
    dataMat=mat(dataSet)
    print (dataMat)
    # print nonzero(dataMat[:,feature]<=value)
    mat0=dataMat[nonzero(dataMat[:,feature]>value)[0],:]
    mat1=dataMat[nonzero(dataMat[:,feature]<=value)[0],:]
    # print dataMat[nonzero(dataMat[:,feature]<=value)[0],:][0]
    return mat0,mat1
def regLeaf(dataSet):
    dataMat=mat(dataSet)
    return mean(dataMat[:,-1])
def regErr(dataSet):
    dataMat=mat(dataSet)
    m=dataMat.shape[0]
    return var(dataMat[:,-1])*m
def chooseBestSplit(dataSet, leafType, errType, ops=(1,4)):
    tolS=ops[0]
    tolN=ops[1]
    if len(set(dataSet[:,-1].T.tolist()[0]))==1:
        return None,leafType(dataSet)
    m,n=dataSet.shape
    S=errType(dataSet)
    bestS=inf;bestIndex=0;bestValue=0
    for featIndex in range(n-1):
        for splitVal in set(dataSet[:,featIndex].T.tolist()[0]):
            mat0,mat1=binSplitDataSet(dataSet,featIndex,splitVal)
            if mat0.shape[0]<tolN or mat1.shape[0]<tolN:
                continue
            newS=errType(mat0)+errType(mat1)
            if newS<bestS:
                bestS=newS
                bestIndex=featIndex
                bestValue=splitVal
    if (S-bestS)<tolS:
        return None,leafType(dataSet)
    mat0,mat1=binSplitDataSet(dataSet,bestIndex,bestValue)
    if (mat0.shape[0]<tolN) or (mat1.shape[0]<tolN):
        return None,leafType(dataSet)
    return bestIndex,bestValue

def createTree(dataSet,leafType=regLeaf,errType=regErr,ops=(1,4)):
    feat,val=chooseBestSplit(dataSet,leafType,errType,ops)
    if feat==None:
        return val
    retTree={}
    retTree["spInd"]=feat
    retTree["spVal"]=val
    lSet,rSet=binSplitDataSet(dataSet,feat,val)
    retTree["left"]=createTree(lSet,leafType,errType,ops)
    retTree["right"]=createTree(rSet,leafType,errType,ops)
    return retTreed
# testSet=eye(4)
# print testSet
# mat0,mat1=binSplitDataSet(testSet,1,0.5)
# myDat=mat(loadDataSet("ex00.txt"))
# print createTree(myDat)
# myDat1=mat(loadDataSet("ex0.txt"))
# print createTree(myDat1)

#树剪枝
def isTree(obj):
        return (type(obj).__name__=="dict")
def getMean(tree):
    if isTree(tree["right"]):
        tree["right"]=getMean(tree["right"])
    if isTree(tree["left"]):
        tree["left"]=getMean(tree["left"])
    return (tree["left"]+tree["right"])/2.0

def prune(tree,testData):
    if testData.shape[0]==0:
        return getMean(tree)
    if isTree(tree["left"]) or isTree(tree["right"]):
        lSet,rSet=binSplitDataSet(testData,tree["spInd"],tree["spVal"])
        if isTree(tree["left"]):
            tree["left"]=prune(tree["left"],lSet)
        if isTree(tree["right"]):
            tree["right"]=prune(tree["right"],rSet)
    if not isTree(tree["left"]) and not isTree(tree["right"]):
        lSet,rSet=binSplitDataSet(testData,tree["spInd"],tree["spVal"])
        errNoMerge=sum(power(lSet[:,-1]-tree["left"],2))+sum(power(rSet[:,-1]-tree["right"],2))
        treeMean=(tree["left"]+tree["right"])/2.0
        errMerge = sum(power(testData[:,-1] - treeMean,2))
        if errMerge<errNoMerge:
            print ("merging")
            return treeMean
        else:return tree
    else:return tree
# mySet2=loadDataSet("ex2.txt")
# myMat2=mat(mySet2)
# mytree=createTree(myMat2,ops=(0,1))
# testSet=loadDataSet("ex2test.txt")
# testMat=mat(testSet)
# print prune(mytree,testMat)

# 构建模型树
def linearSolve(dataSet):
    m,n=dataSet.shape
    X=mat(ones((m,n)))
    Y=mat(ones((m,1)))
    X[:,1:n]=dataSet[:,0:n-1]
    Y[:,0]=dataSet[:,-1]
    xTx=X.T*X
    if linalg.det(xTx)==0:
        raise NameError( "matrix is singular,can not do inverse")
    ws=xTx.I*(X.T*Y)
    return ws,X,Y
def modelLeaf(dataSet):
    ws,X,Y=linearSolve(dataSet)
    return ws
def modelErr(dataSet):
    ws,X,Y=linearSolve(dataSet)
    Yhat=X*ws
    err=sum(power(Yhat-Y,2))
    return err

myMat2=loadDataSet("sine.txt")
myMat2=mat(myMat2)
modelTree=createTree(myMat2,leafType=modelLeaf,errType=modelErr,ops=(1,10))
print (modelTree)

#树回归与标准回归的比较
#用树回归进行预测
def regTreeEval(model,inDat):
    return float(model)
def modelTreeEval(model,inDat):
    n=inDat.shape[1]
    X=mat(ones((1,n+1)))
    X[:,1:n+1]=inDat
    return float(X*model)
def treeForeCast(tree,inDat,evalMethod=regTreeEval):
    if not isTree(tree):
        return evalMethod(tree,inDat)
    if inDat[tree["spInd"]]>tree["spVal"]:#判断走左树
        if isTree(tree["left"]):
            return treeForeCast(tree["left"],inDat,evalMethod) #观察右树代码实现，同样正确
        else:
            return evalMethod(tree["left"],inDat)
    else:
        return treeForeCast(tree["right"],inDat,evalMethod)
def createForeCast(tree,testData,evalMethod=regTreeEval):
    m=len(testData)
    yHat=mat(zeros((m,1)))
    for i in range(m):
        yHat[i,0]=treeForeCast(tree,testData[i],evalMethod)
    return yHat

trainMat=mat(loadDataSet("bikeSpeedVsIq_train.txt"))
testMat=mat(loadDataSet("bikeSpeedVsIq_test.txt"))
#创建一颗回归树
myTree=createTree(trainMat,ops=(1,20))
yHat=createForeCast(myTree,testMat[:,0])
# print yHat
corr=corrcoef(yHat,testMat[:,1],rowvar=0)[0,1]
print (corr)
print ("***************************")
#创建一颗模型树
myTree2=createTree(trainMat,modelLeaf,modelErr,(1,20))
yHat2=createForeCast(myTree2,testMat[:,0],evalMethod=modelTreeEval)
# print yHat2
corr2=corrcoef(yHat2,testMat[:,1],rowvar=0)[0,1]
print (corr2)

#标准回归
ws,X,Y=linearSolve(trainMat)
m=testMat.shape[0]
yHat3=zeros((m,1))
for i in range(m):
    yHat3[i]=ws[0,0]+testMat[i,0]*ws[1,0]
print ("*******************************")
print (corrcoef(yHat3,testMat[:,1],rowvar=0)[0,1])

