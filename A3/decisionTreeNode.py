from collections import Counter
from math import log

class DecisionTreeNode(object):
    CLASSALTATHEISM = 0
    CLASSCOMPGRAPH = 1

    PROPORTIONMODE = 0
    AVGMODE = 1

    @staticmethod
    def classProportion(dataset):
        classIndex = len(dataset[0]) - 1
        numClass = reduce(dataset, lambda x,y: 1 if x[classIndex] == DecisionTreeNode.CLASSALTHEISM else 0 + y, 0)

        return numClass

    @staticmethod
    def calcInfoContent(dataset):
        if dataset.length == 0:
            # dataset is empty, maximum entropy
            return 1

        # calculate information content (number of bits it takes to represent the
        # data set, we will use the maximum likelihood for the probability
        numClass = DecisionTreeNode.classProportion(dataset)
        
        numDataPoints = len(dataset)
        # logarithm base 2
        return  (-numClass * log(numClass / numDataPoints, 2) -\
                   (numDataPoints - numClass) * log(class2 / numDataPoints, 2)) / numDataPoints


    # compute the splits on a dataset and a feature
    # and the resulting info content of the splits

    # result:
    # split1 - split on whether feature is present i.e 1
    # split2 - split on whether feature is not present i.e 0
    # infoContent1 - info content for split1
    # infoContent2 - info content for split2
    @staticmethod
    def computeSplitsAndIC(dataset, feature):
        # get all the data points that don't have the feature present
        split1 = filter(dataset, lambda data: data[feature] == 1)
        # get all the data points that have the feature present
        split2 = filter(dataset, lambda data: data[feature] == 0)
        infoContent1 = DecisionTreeNode.calcInfoContent(split1)
        infoContent2 = DecisionTreeNode.calcInfoContent(split2)

        return (split1, split2, infoContent1, infoContent2)

    @staticmethod
    def computeIESplit(PData, NPData, IEP, IENP, mode):
        if mode == DecisionTreeNode.PROPORTIONMODE:
            numPData = len(PData)
            numNPData = len(NPData)
            return (numPData * IEP + numNPData * IENP) / (numPData + numNPData)
        # else
        return (IEP + IENP) / 2

    
    @staticmethod
    def computeFirstNode(dataset, featureSet, mode):
        maxInfoGain = 0
        bestFeature = None
        infoContent = DecisionTreeNode.calcInfoContent(dataset)

        for feature in featureSet:
            split1, split2, IE1, IE2 = \
                DecisionTreeNode.computeSplitsAndIC(dataset, feature)

            IEsplit = DecisionTreeNode.computeIESplit(split1, split2, IE1, IE2, mode)

            infoGain = infoContent - infoGain
            
            if infoGain >= maxInfoGain:
                maxInfoGain = infoGain
                bestFeature = feature

        return DecisionTreeNode(None, data, bestFeature, maxInfoGain, featureSet)

    # compute the best feature and their respective info gain
    # for each value of the feature of this node, essentially expanding
    # the node, return the expanded nodes

    # return:
    # PFeatureNode - the node that is reached when feature is present
    # NPFeatureNode - the node that is reached when feature is not present
    def expand(self, mode):
        maxInfoGainP = 0
        maxInfoGainNP = 0
        
        bestFeatureP = None
        bestFeatureNP = None
        
        split1, split2, infoContent1, infoContent2 = \
                DecisionTreeNode.computeSplitAndIC(self.dataset, self.feature)
        
        for feature in self.featureSets:
            for presence in (0,1):
                if presence == 1:
                    IE = infoContent1
                    splitFeatureP, splitFeatureNP, IE1, IE2 = \
                            DecisionTreeNode.computeSplitAndIC(split1, feature)
                else:
                    IE = infoContent2
                    splitFeatureP, splitFeatureNP, IE1, IE2 = \
                            DecisionTreeNode.computeSplitAndIC(split2, feature)

                IEsplit = DecisionTreeNode.computeIESplit(splitFeatureP, splitFeatureNP, IE1, IE2, mode)

                infoGain = IE - IEsplit
                if presence == 1:
                    if infoGain >= maxInfoGainP:
                        maxInfoGainP = infoGain
                        bestFeatureP = feature
                else:
                    if infoGain >= maxInfoGainNP:
                        maxInfoGainNP = infoGain
                        bestFeatureNP = feature

        self.PFeatureNode = DecisionTree(self, split1, bestFeatureP, maxInfoGainP, self.featureSet)
        self.NPFeatureNode = DecisionTree(self, split2, bestFeatureNP, maxInfoGainNP, self.featureSet)
        
        # return the decision tree nodes corresponding to when the feature at this
        # node is present and when the feature is not present
        return (self.PFeatureNode, self.NPFeatureNode)

    @staticmethod
    def predict(leafNode, document):
        while True:
            featureAtNode = leafNode.feature
            if document[leafNode.feature] == 1 and leafNode.PFeatureNode:
                # if feature is present in document and there is a correspoding presence node
                leafNode = leafNode.PFeatureNode
            elif document[leafNode.feature] == 0 and leafNode.NPFeatureNode:
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
    def __init__(self, dataset, selfFeature, bestFeatureInfoGain, featureSet):
        self.dataset = dataset
        self.feature = selfFeature
        self.bestFeatureInfoGain = bestFeatureInfoGain
        # remove the own feature from the feature set
        self.featureSet = featureSet.copy().remove(self.feature)
        # the decision tree node when the feature (selfFeature) is present
        self.PFeatureNode = None
        # the decision tree node when the feature (selfFeature) is not present
        self.NPFatureNode = None
        # get the majority class of this node
        self.pointEstimate = Counter(dataset).most_common(1)[0][1]


    # comparison method, we reverse the results in order so
    # we can sort the nodes in the form of a max heap
    def __cmp__(self, other):
        if self.bestFeatureInfoGain < other.bestFeatureInfoGain:
            return 1
        elif self.bestFeatureInfoGain == other.bestFeatureInfoGain:
            return 0
        else:
            return 1
