'''
Created on Oct 14, 2010

@author: Peter Harrington
'''
import matplotlib.pyplot as plt
from trees import createTree

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")

def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':#test to see if the nodes are dictonaires, if not they are leaf nodes
            numLeafs += getNumLeafs(secondDict[key])
        else:   numLeafs +=1
    return numLeafs

def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':#test to see if the nodes are dictonaires, if not they are leaf nodes
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:   thisDepth = 1
        if thisDepth > maxDepth: maxDepth = thisDepth
    return maxDepth

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt,  xycoords='axes fraction',
             xytext=centerPt, textcoords='axes fraction',
             va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)
    
def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)

def plotTree(myTree, parentPt, nodeTxt):#if the first key tells you what feat was split on
    """
    按照从上到下，从左到右的方式遍历，即深度优先遍历
    """
    numLeafs = getNumLeafs(myTree)  #this determines the x width of this tree
    depth = getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]     #the text label for this node should be this
    # 初始偏移量为-1/totalW/2，此时绘制的Node一定是decisionNode，否则直接调用叶子节点
    # 整体的中心根据其下属叶子节点数量计算，偏移量为【原始偏移量+1/2/totalW(修正偏移居中)+leafs/totalW/2(宽度占比的一半)】
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    # y的更新为每次减少【1/深度】，用于绘制叶子节点
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD 
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':#test to see if the nodes are dictonaires, if not they are leaf nodes
            plotTree(secondDict[key],cntrPt,str(key))        #recursion, only starting has no txtString
        else:   #it's a leaf node print the leaf node
            # 每次绘制叶子节点，x的偏移都向右移动1/totalW，如果先绘制叶子再绘制决策点，那么决策点会在最后一个叶子的右边
            # 如果先绘制决策点，再绘制叶子，那么叶子会在决策点最右边子叶的右边一单位
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW # 绘制叶子节点，让xOff右边移动1/W
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    # 绘制完成叶子节点，把yOff恢复到上一级，因为plotTree是递归调用的，调用完之后要回到上一级，展示其他相邻的叶子节点
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD 
#if you do get a dictonary you know it's a tree, and the first element will be another dict

def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[i/10.0 for i in range(11)], yticks=[i/10.0 for i in range(11)])
    # 函数内定义属性，可以用func.attr
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)    #no ticks
    #createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses 
    plotTree.totalW = float(getNumLeafs(inTree)) # width
    plotTree.totalD = float(getTreeDepth(inTree))# depth
    # 对于子节点的偏移，即为当前节点再往左移1/2*totalW
    plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0; #xoff=-0.125
    # 从中央顶部开始绘制起点
    plotTree(inTree, (0.5,1.0), '')
    plt.show()

#def createPlot():
#    fig = plt.figure(1, facecolor='white')
#    fig.clf()
#    createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses 
#    plotNode('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode)
#    plotNode('a leaf node', (0.8, 0.1), (0.3, 0.8), leafNode)
#    plt.show()

def retrieveTree(i):
    listOfTrees =[{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                  {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
                  ]
    return listOfTrees[i]

#createPlot(thisTree)
if __name__ == '__main__':
    print('hello world')
    tree = retrieveTree(1)
    tree['no surfacing']['2']={'maybe':{0:'haha',1:'gaga'}}
    createPlot(tree)

    fr = open('lenses.txt')
    lenses = [inst.strip().split('\t') for inst in fr.readlines()]
    print(lenses, lenses[0].__len__(), end='\n')
    lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRates']
    lensesTree = createTree(lenses, lensesLabels)
    lensesTree
    createPlot(lensesTree)