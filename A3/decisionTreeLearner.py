from decisionTreeNode import DecisionTreeNode as DTN
import heapq

class DecisionTreeLearner(object):
    def __init__(self, dataset, features, mode):
        self.dTree = DTN.computeFirstNode(dataset, features, mode)
        self.mode = mode

    def learn(self, wordsSet=None):
        priorityQ = [self.dTree]

        expandNum = 100
        for i in xrange(0, expandNum):
            expandTree = heapq.heappop(priorityQ)
            Pnode, NPnode = expandTree.expand(self.mode)

            if Pnode and NPnode:
                # if we actually expanded
                heapq.heappush(priorityQ, Pnode)
                heapq.heappush(priorityQ, NPnode)

            if wordsSet:
                if i == 0:
                    if self.mode == DTN.PROPORTIONMODE:
                        print 'Weighted Information Gain\r'
                    else:
                        print 'Average Information Gain\r'
                    print '=========================='

                if i <= 9:
                    # print the tree
                    expandTree.printSelf(wordsSet)
            yield self.dTree
