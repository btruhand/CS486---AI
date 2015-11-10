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
        return  (-class1 * log(class1 / numDataPoints, 2) - \ 
                  (numDataPoints - class1)* log(class2 / numDataPoints, 2)) / numDataPoints


    # compute the best feature and their respective info gain
    # for each value of the feature of this node
    def bestFeatureAndInfoGain(self, featureSets, mode):
        maxInfoGainP = 0
        maxInfoGainNP = 0
        
        bestFeatureP = None
        bestFeatureNP = None

        # get all the data points that don't have the feature present
        split1 = filter(data for data in self.dataset if data[self.feature] == 0)
        # get all the data points that have the feature present
        split2 = filter(data for data in self.dataset if data[self.feature] == 1)
        infoContent1 = DecisionTreeNode.calcInfoContent(split1)
        infoContent2 = DecisionTreeNode.calcInfoContent(split2)

        numFeaturePresent = len(split1)
        numFeatureNotPresent = len(split2)
        for feature in featureSets:
            for presence in (0,1):
                if presence == 0:
                    IE = infoContent1
                    splitFeatureP = filter(split1, lambda data: data[feature] == 1)
                    splitFeatureNP = filter(split1, lambda data: data[feature] == 0)
                else:
                    IE = infoContent2
                    splitFeatureP = filter(split2, lambda data: data[feature] == 1)
                    splitFeatureNP = filter(split2, lambda data: data[feature] == 0)

                IE1 = DecisionTreeNode.calcInfoContent(splitFeatureP)
                IE2 = DecisionTreeNode.calcInfoContent(splitFeatureNP)

                if mode == DecisionTreeNode.PROPORTIONMODE:
                    numSplitPData = len(splitFeatureP)
                    numSplitNPData = len(splitFeatureNP)
                    IEsplit = (numSplitData * IE1 + numSplitNPData * IE2) / (numSplitPData + numSplitNPData)
                else:
                    IEsplit = (splitInfoContent1 + splitInfoContent2) / 2

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

    def __init__(self, parentNode, dataset, selfFeature, infoContent, bestFeatureInfoGain):
        self.parentNode = parentNode
        self.dataset = dataset
        self.feature = selfFeature
        self.infoContent = infoContent
        self.presentFeatureNode = None
        self.notPresentFeatureNode = None
        # get the majority class of this node
        self.pointEstimate = Counter(dataset).most_common(1)[0][1]
        self.bestFeatureInfoGain = bestFeatureInfoGain
