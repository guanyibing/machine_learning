# -*- encoding:utf8 -*-
from numpy import *
from Tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import  FigureCanvasTkAgg
import matplotlib.pyplot as plt
import regTrees
#构建基本界面
def reDraw(tolS,tolN):
    fig.clf()
    a=fig.add_subplot(111)
    # if chkBtnVar.get():#勾选 check button,就画模型树
    #     if tolN<2:
    #         tolN=2
    #     myTree=regTrees.createTree(loadData,regTrees.modelLeaf,regTrees.modelErr,ops=(tolS,tolN))
    #     yHat=regTrees.createForeCast(myTree,testData,regTrees.regTreeEval)
    # else:#默认，就画回归树
    myTree=regTrees.createTree(loadData,ops=(tolS,tolN))
    yHat=regTrees.createForeCast(myTree,testData)
    a.scatter(loadData[:,0],loadData[:,1],marker="s",s=5)
    a.plot(testData,yHat,linewidth=2.0)
    canvas.show()


def getInputs():
    try:
        tolS=float(tolSEntry.get())
    except:
        tolS=1.0
        print "Enter float for tolS"
        tolSEntry.delete(0,END)
        tolSEntry.insert(0,"1.0")
    try:
        tolN=int(tolNEntry.get())
    except:
        tolN=10
        print "Enter float for tolN"
        tolNEntry.delete(0,END)
        tolNEntry.insert(0,"10")
    return tolS,tolN

def drawNewTree():
    tolS,tolN=getInputs()
    reDraw(tolS,tolN)

root=Tk()

fig=plt.figure(figsize=(5,4),dpi=100)#默认是dpi=80
canvas=FigureCanvasTkAgg(fig,root)
canvas.show()
canvas.get_tk_widget().grid(row=1,columnspan=3)

Label(root,text="Plot Place Holder").grid(row=0,columnspan=3)

Label(root,text="tolS").grid(row=2,column=0)
tolSEntry=Entry(root)
tolSEntry.grid(row=2,column=1)
tolSEntry.insert(0,1.0)
Label(root,text="tolN").grid(row=3,column=0)
tolNEntry=Entry(root)
tolNEntry.grid(row=3,column=1)
tolNEntry.insert(0,10)

Button(root,text="ReDraw",command=drawNewTree).grid(row=3,column=2,columnspan=3)
chkBtnVar=IntVar()
chkBtn=Checkbutton(root,text="Model Tree",variable=chkBtnVar)
chkBtn.grid(row=4,columnspan=3)

loadData=mat(regTrees.loadDataSet("sine.txt"))#放在reDraw函数外，只需一开始加载一次数据
testData=arange(min(loadData[:,0]),max(loadData[:,0]),0.01)
#
reDraw(1.0,10)

root.mainloop()