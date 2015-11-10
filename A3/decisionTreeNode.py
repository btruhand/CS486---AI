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
        numClass = map(dataset, lambda x: 1 if x[classIndex] == DecisionTreeNode.CLASSALTHEISM else 0)

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
        return  (-class1 * log(class1 / numDataPoints, 2) -\
                (numDataPoints - class1) * log(class2 / numDataPoints, 2)) / numDataPoints


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
        split1 = filter(data for data in dataset if data[feature] == 1)
        # get all the data points that have the feature present
        split2 = filter(data for data in dataset if data[self.feature] == 0)
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
    def computeFirstNode(dataset, mode):
        maxInfoGain = 0
        bestFeature = None
        infoContent = DecisionTreeNode.calcInfoContent(dataset)

        for feature in featureSets:
            split1, split2, IE1, IE2 = \
                DecisionTreeNode.computeSplitAndIC(dataset, feature)

            IEsplit = DecisionTreeNode.computeEISplit(split1, split2, IE1, IE2, mode)

            infoGain = infoContent - infoGain
            
            if infoGain >= maxInfoGain:
                maxInfoGain = infoGain
                bestFeature = feature

        return DecisionTreeNode(None, data, bestFeature, infoContent, maxInfoGain)

    # compute the best feature and their respective info gain
    # for each value of the feature of this node, essentially expanding
    # the node, return the expanded nodes

    # return:
    # PFeatureNode - the node that is reached when feature is present
    # NPFeatureNode - the node that is reached when feature is not present
    def expand(self, featureSets, mode):
        maxInfoGainP = 0
        maxInfoGainNP = 0
        
        bestFeatureP = None
        bestFeatureNP = None

        split1, split2, infoContent1, infoContent2 = \
                DecisionTreeNode.computeSplitAndIC(self.dataset, self.feature)
        
        for feature in featureSets:
            for presence in (0,1):
                if presence == 0:
                    IE = infoContent1
                    splitFeatureP, splitFeatureNP, IE1, IE2 = \
                            DecisionTreeNode.computeSplitAndIC(split1, feature)
                else:
                    IE = infoContent2
                    splitFeatureP, splitFeatureNP, IE1, IE2 = \
                            DecisionTreeNode.computeSplitAndIC(split2, feature)

                IEsplit = DecisionTreeNode.computeIESplit(splitFeatureP, splitFeatureNP, IE1, IE2, mode)

                infoGain = IE - IEsplit
                if presence == 0:
                    if infoGain >= maxInfoGainNP:
                        maxInfoGainNP = infoGain
                        bestFeatureNP = feature
                else:
                    if infoGain >= maxInfoGainP:
                        maxInfoGainP = infoGain
                        bestFeatureP = feature

        self.PFeatureNode = DecisionTree(self, split2, bestFeatureP, infoContent2, maxInfoGainP)
        self.NPFeatureNode = DecisionTree(self, split1, bestFeatureNP, infoContent1, maxInfoGainNP)
        
        # return the decision tree nodes corresponding to when the feature at this
        # node is present and when the feature is not present
        return (PFeatureNode, NPFeatureNode)

    # create a decision tree node
    # Parameters:
    # parentNode - the parent of this node
    # dataset - the dataset that this node is working with
    # selfFeature - the feature that is being used to split at this node
    # infoContent - the information content on the dataset used at this node
    # bestFeatureInfoGain - the info gain of the best feature to split on at this node
    def __init__(self, parentNode, dataset, selfFeature, infoContent, bestFeatureInfoGain):
        self.parent = parentNode
        self.dataset = dataset
        self.feature = selfFeature
        self.infoContent = infoContent
        # the decision tree node when the feature (selfFeature) is present
        self.presentFeatureNode = None
        # the decision tree node when the feature (selfFeature) is not present
        self.notPresentFeatureNode = None
        # get the majority class of this node
        self.pointEstimate = Counter(dataset).most_common(1)[0][1]
        self.bestFeatureInfoGain = bestFeatureInfoGain


    # comparison method, we reverse the results in order so
    # we can sort the nodes in the form of a max heap
    def __cmp__(self, other):
        if self.bestFeatureInfoGain < other.bestFeatureInfoGain:
            return 1
        else if self.bestFeatureInfoGain = other.bestFeatureInfoGain:
            return 0
        else:
            return 1
