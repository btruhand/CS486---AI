from __future__ import division
from collections import Counter
from math import log
import sys

class DecisionTreeNode(object):
    CLASSALTATHEISM = 1
    CLASSCOMPGRAPH = 2

    PROPORTIONMODE = 0
    AVGMODE = 1

    @staticmethod
    def classProportion(dataset):
        classIndex = len(dataset[0]) - 1
        numClass = reduce(lambda x,y: (1 if y[classIndex] == DecisionTreeNode.CLASSALTATHEISM else 0) + x, dataset, 0)

        return numClass

    @staticmethod
    def calcInfoContent(dataset):
        if len(dataset) == 0:
            # dataset is empty, maximum entropy
            return 1

        # calculate information content (number of bits it takes to represent the
        # data set), we will use the maximum likelihood for the probability
        numClass = DecisionTreeNode.classProportion(dataset)
       
        numDataPoints = len(dataset)
        # logarithm base 2
        
        proportionAtheism = numClass / numDataPoints
        proportionGraphics = (numDataPoints - numClass) / numDataPoints

        calcAtheism = 0 if proportionAtheism == 0 else (-proportionAtheism * log(proportionAtheism, 2))
        calcGraphics = 0 if proportionGraphics == 0 else (-proportionGraphics * log(proportionGraphics, 2))
        return  calcAtheism + calcGraphics
                   
    # compute the splits on a dataset and a feature
    # and the resulting info content of the splits

    # result:
    # split1 - split on whether feature is present i.e 1
    # split2 - split on whether feature is not present i.e 0
    # infoContent1 - info content for split1
    # infoContent2 - info content for split2
    @staticmethod
    def computeSplitsAndIC(dataset, feature):
        # get all the data points that have the feature present
        split1 = filter(lambda data: data[feature] == 1, dataset)
        # get all the data points that don't have the feature present
        split2 = filter(lambda data: data[feature] == 0, dataset)
        infoContent1 = DecisionTreeNode.calcInfoContent(split1)
        infoContent2 = DecisionTreeNode.calcInfoContent(split2)

        return (split1, split2, infoContent1, infoContent2)

    @staticmethod
    def computeIESplit(PData, NPData, IEP, IENP, mode):
        if mode == DecisionTreeNode.PROPORTIONMODE:
            numPData = len(PData)
            numNPData = len(NPData) 

            IE1 = (numPData / (numPData + numNPData)) * IEP
            IE2 = (numNPData / (numPData + numNPData)) * IENP
            return IE1 + IE2
        # else
        return (IEP + IENP) / 2

    
    @staticmethod
    def computeFirstNode(dataset, featureSet, mode):
        maxInfoGain = None
        bestFeature = None
        infoContent = DecisionTreeNode.calcInfoContent(dataset)

        for feature in featureSet:
            split1, split2, IE1, IE2 = \
                DecisionTreeNode.computeSplitsAndIC(dataset, feature)

            IEsplit = DecisionTreeNode.computeIESplit(split1, split2, IE1, IE2, mode)

            infoGain = infoContent - IEsplit
            
            if maxInfoGain is None or infoGain > maxInfoGain:
                maxInfoGain = infoGain
                bestFeature = feature

        return DecisionTreeNode(dataset, bestFeature, maxInfoGain, featureSet, 0)

    # compute the best feature and their respective info gain
    # for each value of the feature of this node, essentially expanding
    # the node, return the expanded nodes
    # return:
    # PFeatureNode - the node that is reached when feature is present
    # NPFeatureNode - the node that is reached when feature is not present
    def expand(self, mode):
        if not self.bestFeatureInfoGain:
            # 0 or no best feature
            return (None,None)

        maxInfoGainP = None
        maxInfoGainNP = None
        bestFeatureP = None
        bestFeatureNP = None
        
        split1, split2, infoContent1, infoContent2 = \
                DecisionTreeNode.computeSplitsAndIC(self.dataset, self.feature)
        
        for feature in self.featureSet:
            for presence in (0,1):
                if presence == 1:
                    # check if split is empty if so skip
                    if not split1:
                        continue
                    IE = infoContent1
                    splitFeatureP, splitFeatureNP, IE1, IE2 = \
                            DecisionTreeNode.computeSplitsAndIC(split1, feature)
                else:
                    # same case here
                    if not split2:
                        continue
                    IE = infoContent2
                    splitFeatureP, splitFeatureNP, IE1, IE2 = \
                            DecisionTreeNode.computeSplitsAndIC(split2, feature)

                IEsplit = DecisionTreeNode.computeIESplit(splitFeatureP, splitFeatureNP, IE1, IE2, mode)

                infoGain = IE - IEsplit
                if presence == 1:
                    if maxInfoGainP is None or infoGain > maxInfoGainP:
                        maxInfoGainP = infoGain
                        bestFeatureP = feature
                else:
                    if maxInfoGainNP is None or infoGain > maxInfoGainNP:
                        maxInfoGainNP = infoGain
                        bestFeatureNP = feature

        self.PFeatureNode = DecisionTreeNode(split1, bestFeatureP, maxInfoGainP, self.featureSet, self.depth + 1)
        self.NPFeatureNode = DecisionTreeNode(split2, bestFeatureNP, maxInfoGainNP, self.featureSet, self.depth + 1)
        
        # return the decision tree nodes corresponding to when the feature at this
        # node is present and when the feature is not present
        return (self.PFeatureNode, self.NPFeatureNode)

    @staticmethod
    def predict(leafNode, document):
        while True:
            featureAtNode = leafNode.feature
            if not featureAtNode:
                # if there was no feature to split on then we break
                break

            if document[featureAtNode] == 1 and leafNode.PFeatureNode:
                # if feature is present in document and there is a correspoding presence node
                leafNode = leafNode.PFeatureNode
            elif document[featureAtNode] == 0 and leafNode.NPFeatureNode:
                leafNode = leafNode.NPFeatureNode
            else:
                # none of the conditions above are satisfied
                break
        return leafNode.pointEstimate


    # create a decision tree node
    # Parameters:
    # dataset - the dataset that this node is working with
    # selfFeature - the feature that is being used to split at this node
    # bestFeatureInfoGain - the info gain of the best feature to split on at this node
    # featureSet - the features that this node is to work with including the feature of this node itself
    # depth - for printing purposes
    def __init__(self, dataset, selfFeature, bestFeatureInfoGain, featureSet, depth):
        self.dataset = dataset
        self.feature = selfFeature
        self.bestFeatureInfoGain = bestFeatureInfoGain
        # remove the own feature from the feature set
        self.featureSet = featureSet.copy()
        if self.feature:
            self.featureSet.remove(self.feature)
        # the decision tree node when the feature (selfFeature) is present
        self.PFeatureNode = None
        # the decision tree node when the feature (selfFeature) is not present
        self.NPFeatureNode = None
        # get the majority class of this node
        numAtheism = 0
        numGraphics = 0
        for datapoint in dataset:
            if datapoint[-1] == DecisionTreeNode.CLASSALTATHEISM:
                numAtheism+= 1
            else:
                numGraphics+= 1
        self.pointEstimate = DecisionTreeNode.CLASSALTATHEISM if \
                                numAtheism > numGraphics else DecisionTreeNode.CLASSCOMPGRAPH

        self.depth = depth

    def printSelf(self, wordsSet):
        for i in xrange(0, self.depth):
            sys.stdout.write(' ')
        print 'Feature: {} Information Gain: {:.3f}\r'.format(wordsSet[self.feature], self.bestFeatureInfoGain)
        for i in xrange(0, self.depth + 3):
            sys.stdout.write(' ')
        
        presence = True if self.PFeatureNode.feature is not None else False
        notPresence = True if self.NPFeatureNode.feature is not None else False
        
        print '|________ Present child node feature: {!s} PointEstimate: {} IG: {:}\r'.format(\
                None if not presence else wordsSet[self.PFeatureNode.feature], \
                self.PFeatureNode.pointEstimate, self.PFeatureNode.bestFeatureInfoGain)
        for i in xrange(0, self.depth + 3):
            sys.stdout.write(' ')
        print '|________ Not present child node feature: {!s} PointEstimate: {} IG: {:}\r'.format(\
                None if not notPresence else wordsSet[self.NPFeatureNode.feature], \
                self.NPFeatureNode.pointEstimate, self.NPFeatureNode.bestFeatureInfoGain)

    # comparison method, we reverse the results in order so
    # we can sort the nodes in the form of a max heap
    def __cmp__(self, other):
        if self.bestFeatureInfoGain < other.bestFeatureInfoGain:
            return 1
        elif self.bestFeatureInfoGain == other.bestFeatureInfoGain:
            return 0
        else:
            return -1
