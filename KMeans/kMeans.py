# -*- coding:utf8 -*-
from numpy import *
def loadDataSet(filename):
    dataMat=[]
    fr=open(filename)
    for line in fr.readlines():
        currentLine=line.strip().split("\t")
        lineList=map(float,currentLine)
        dataMat.append(lineList)
    return dataMat

def distEclud(vecA,vecB):
    return sqrt(sum(power((vecA-vecB),2)))

def randCent(dataSet,k):
    dataMat=mat(dataSet)
    n=dataMat.shape[1]
    centroids=mat(zeros((k,n)))
    for j in range(n):
        minJ=min(dataMat[:,j])
        rangeJ=float(max(dataMat[:,j])-minJ)#将矩阵转换成浮点数
        centroids[:,j]=minJ+rangeJ*random.rand(k,1)
    return centroids

def kMeans(dataSet,k):
    dataMat=mat(dataSet)
    m=dataMat.shape[0]
    centroids=randCent(dataMat,k)

    clusterAssem=mat(zeros((m,2)))
    clusterChanged=True
    while clusterChanged:
        clusterChanged=False
        for i in range(m):
            minDist=inf
            minIndex=-1
            for j in range(k):
                distIJ=distEclud(centroids[j,:],dataMat[i,:])
                if distIJ<minDist:
                    minDist=distIJ
                    minIndex=j
            if clusterAssem[i,0]!=minIndex: #此次所有i都正确聚类，clusterChanged被修改为False，循环停止
                clusterChanged=True
            clusterAssem[i,:]=minIndex,minDist**2
        for cent in range(k):
            dataInCluster=dataMat[nonzero(clusterAssem[:,0]==cent)[0]]
            centroids[cent,:]=mean(dataInCluster,axis=0)
    return centroids,clusterAssem


dataSet=loadDataSet("testSet.txt")
centroids,clusterAssem=kMeans(dataSet,4)

import matplotlib.pyplot as plt
fig=plt.figure()
ax0=fig.add_axes([0.1,0.1,0.8,0.8],label="ax0",**{"xticks":[],"yticks":[]})#**dict(xticks=[].yticks=[]),不显示坐标
# plt.xticks([])
# plt.yticks([])
imp=plt.imread("Portland.png")
ax0.imshow(imp)
ax1=fig.add_axes([0.1,0.1,0.8,0.8],label="ax1",frameon=False)
ax1.scatter(mat(dataSet)[:,0],mat(dataSet)[:,1],marker='s')
plt.show()


def biKmeans(dataSet,k):
    dataMat=mat(dataSet)
    m=dataMat.shape[0]
    clusterAssem=mat(zeros((m,2)))
    centroid0=mean(dataMat,axis=0).tolist()[0]
    centList=[centroid0]
    for j in range(m):
        clusterAssem[j,1]=distEclud(centroid0,dataMat[j,:])**2
    while (len(centList)<k):
        lowestSSE=inf
        for i in range(len(centList)):
            ptsInCurrCluster=dataMat[nonzero(clusterAssem[:,0]==i)[0],:]
            centroidMat,splitClusterAss=kMeans(dataSet,2)
            asseSplit=sum(splitClusterAss[:,1])  #再次2分后两个聚类的误差和
            asseNotSplit=sum(clusterAssem[nonzero(clusterAssem[:,0]!=i)[0],1]) #未被再次2分的数据原分类误差和
            print ("asseSplit,asseNotSplit",asseSplit,asseNotSplit)

            if (asseSplit+asseNotSplit)<lowestSSE:
                bestCentToSplit=i
                bestClusterAssem=splitClusterAss.copy()
                lowestSSE=asseSplit+asseNotSplit
                bestNewCents=centroidMat
        #更新簇的分配结果
        bestClusterAssem[nonzero(bestClusterAssem[:,0]==0)[0],0]=bestCentToSplit
        bestClusterAssem[nonzero(bestClusterAssem[:,0]==1)[0],0]=len(centList)
        centList[bestCentToSplit]=bestNewCents[0,:]
        centList.append(bestNewCents[1,:])

        #更新clusterAssem
        clusterAssem[nonzero(clusterAssem[:,0]==bestCentToSplit)[0],:]=bestClusterAssem

        return centList,clusterAssem

# dataSet=loadDataSet("testSet2.txt")
# centList,clusterAssem= biKmeans(dataSet,3)
# print centList
# print "***********************"
# print clusterAssem







