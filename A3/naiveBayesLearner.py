from __future__ import division
from math import log, fabs
import heapq

class NaiveBayesLearner(object):
    ALTATHEISM = 1
    COMPGRAPHICS = 2

    def __init__(self, featuresSet, documents):
        labeledAtheism = filter(lambda doc: doc[-1] == NaiveBayesLearner.ALTATHEISM, documents)
        labeledGraphics = filter(lambda doc: doc[-1] == NaiveBayesLearner.COMPGRAPHICS, documents)
        # prior probability, this is the probability
        # using maximum likelihood
        self.priorAtheism = len(labeledAtheism)/len(documents)
        self.priorGraphics = len(labeledGraphics)/len(documents)

        # for each feature calculate the likelihood
        # P(feature = true|class=1) and P(feature = true|class=2)
        # done with laplace correction with alpha = 2 beta = 2
        
        self.likelihoods = [((reduce(lambda x,y: (1 if y[feature] else 0) + x, labeledAtheism, 0) + 1)/(len(labeledAtheism) + 2),\
                            (reduce(lambda x,y: (1 if y[feature] else 0) + x, labeledGraphics, 0) + 1)/(len(labeledGraphics) + 2))\
                                for feature in featuresSet]
    
    def predict(self, doc):
        posteriorAth = log(self.priorAtheism)
        posteriorGraph = log(self.priorGraphics)
        
        # compute Pr(label, features of documents)
        # do not include the classification
        for i in xrange(0,len(self.likelihoods)):
            # update the probabilities by Pr(feature=true/false | Atheism/PosteriorGraph)
            posteriorAth+= log(self.likelihoods[i][0]) if doc[i] else log(1-self.likelihoods[i][0])
            posteriorGraph+= log(self.likelihoods[i][1]) if doc[i] else log(1-self.likelihoods[i][1])
        
        # return the classification that has the higher probability
        return NaiveBayesLearner.ALTATHEISM if posteriorAth >= posteriorGraph else NaiveBayesLearner.COMPGRAPHICS

    # print out the top 10 most discriminative words
    def printMostDiscriminative(self, wordsSet):
        res = []
        for i in xrange(0,len(self.likelihoods)):
            discriminateMeasure = fabs(log(self.likelihoods[i][0], 2) - log(self.likelihoods[i][1], 2))
            res.append((i,discriminateMeasure))
     
        res.sort(lambda x,y: cmp(x[1],y[1]), None, True)
        for i in xrange(0, 10):
            print 'Word: {!s} Discrimination: {}'.format(wordsSet[res[i][0]], res[i][1])
