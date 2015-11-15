from decisionTreeNode import DecisionTreeNode as DTN
import heapq

class DecisionTreeLearner(object):
    def __init__(self, dataset, features, mode):
        self.dTree = DTN.computeFirstNode(dataset, features, mode)
        self.mode = mode

    def learn(self, wordsSet=None):
        priorityQ = [self.dTree]

        expandNum = 100
        i = 0
        while i < expandNum and priorityQ:
            expandTree = heapq.heappop(priorityQ)
            if not expandTree.bestFeatureInfoGain > 0:
                # no need to expand
                continue
            Pnode, NPnode = expandTree.expand(self.mode)

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
            i+= 1
            yield self.dTree
