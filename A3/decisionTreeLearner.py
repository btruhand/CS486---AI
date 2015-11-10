from decisionTreeNode import DecisionTreeNode as DTN
import heapq

class DecisionTreeLearner(object):
    def __init__(dataset, features, mode):
        self.dTree = DTN.computeFirstNode(dataset, mode)
        self.featureSets = features
        self.mode = mode

    def learn():
        priorityQ = [self.dTree]

        expandNum = 100
        for i in xrange(0, expandNum):
            expandTree = heapq.heappop(priorityQ)
            Pnode, NPnode = expandTree.expand(self.featureSets 
