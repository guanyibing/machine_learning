# -*- coding:utf8 -*-
import matplotlib.pyplot as plt
from trees import grapTree
decisionNode=dict(boxstyle='sawtooth',fc='0.8')#facecolor rgb格式，范围0-1
leafNode=dict(boxstyle='round4',fc='0.8')
arrow_props=dict(arrowstyle='<|-',connectionstyle='arc3',fc='r')

def plotNode(nodeTxt,parentPt,centerPt,nodeType):
    createPlot.ax.annotate(nodeTxt,xy=parentPt,xycoords='axes fraction',xytext=centerPt,textcoords='axes fraction',ha='center',va='center',bbox=nodeType,arrowprops=arrow_props)

def plotMidText(parentPt,centerPt,txtString):
    xMid=(parentPt[0]-centerPt[0])/2+centerPt[0]
    yMid=(parentPt[1]-centerPt[1])/2+centerPt[1]
    createPlot.ax.text(xMid,yMid,txtString)
def plotTree(myTree,parentPt,nodeTxt):
     firstFloor=myTree.keys()[0]
     numLeafs=getNumLeafs(myTree)
     deepth=getTreeDeepth(myTree)
     centerPt=(plotTree.xOff+(1.0+float(numLeafs))/2/plotTree.totalW,plotTree.yOff)
     # print centerPt
     plotMidText(parentPt,centerPt,nodeTxt)
     plotNode(firstFloor,parentPt,centerPt,decisionNode)
     secondDict=myTree[firstFloor]
     plotTree.yOff=plotTree.yOff-1/plotTree.totalD
     for key in secondDict.keys():
         if type(secondDict[key]).__name__=="dict":
             plotTree(secondDict[key],centerPt,str(key))
         else:
             plotTree.xOff=plotTree.xOff+1/plotTree.totalW
             # print plotTree.xOff
             plotNode(secondDict[key],centerPt,(plotTree.xOff,plotTree.yOff),leafNode)
             plotMidText(centerPt,(plotTree.xOff,plotTree.yOff),str(key))
     plotTree.yOff=plotTree.yOff+1/plotTree.totalD #很重要，重置总高度，使得另一深分支与兄弟分支同一高度，而不是成为它的下一层
def createPlot(inTree):
    fig=plt.figure()
    fig.clf()
    createPlot.ax=fig.add_subplot(111)
    plotTree.totalW=float(getNumLeafs(inTree))
    plotTree.totalD=float(getTreeDeepth(inTree))
    plotTree.xOff=-0.5/plotTree.totalW
    plotTree.yOff=1.0
    plotTree(inTree,(0.5,1.0),"")
    plt.show()

def getNumLeafs(myTree):
    numLeafs=0
    firstFloor=myTree.keys()[0]
    secondDict=myTree[firstFloor]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=="dict":
            numLeafs+=getNumLeafs(secondDict[key])
        else:
            numLeafs+=1
    return numLeafs
def getTreeDeepth(myTree):
    maxDeepth=0
    firstFloor=myTree.keys()[0]
    secondDict=myTree[firstFloor]
    thisDeepth=0
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=="dict":
            thisDeepth+=getTreeDeepth(secondDict[key])
        else:
            thisDeepth=1
        if thisDeepth>maxDeepth:maxDeepth=thisDeepth
    return maxDeepth
def retriveTree(i):
    listOfTree=[{
        "no surfacing":{0:'no',1:{
            "flippers":{
                0:"no",1:'yes'
            }
        }}},
        {"no surfacing":{0:'no',1:{
            "flippers":{
                0:{"head":{0:"no",1:'yes'}},1:"no"
            }
        }
                         }
    }]
    return listOfTree[i]

# myTree=retriveTree(0)
# myTree["no surfacing"][3]="maybe"
# # print myTree
# numLeafs=getNumLeafs(myTree)
# print numLeafs
# treeDeepth=getTreeDeepth(myTree)
# print treeDeepth
# # myTree=createPlot(myTree)
# # print myTree
myTree=grapTree("glasses.txt")
print createPlot(myTree)
