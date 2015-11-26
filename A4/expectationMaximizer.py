from __future__ import division
from math import log
import random

class ExpectationMaximizer(object):
    MAX_DELTA = 4
    # numDeltas - how many different deltas we will use
    # trainData - the training set
    def __init__(self, numDeltas, trainData, seed):
        self.numDeltas = numDeltas
        self.delta = 0
        self.seed = seed

        # CPTs table are for when the variable = True
        # except for Dunetts Syndrome that has 3 possible values
        # In order:
        # * Sloepne
        # * Forienditis
        # * Degar Spots
        # * TRIMONO-HT/S
        # * Dunetts Syndrome
        self.CPTs =\
                [[[0.01, 0.03, 0.03],\
                  [0.05, 0.30, 0.20]],\
                 [0.05, 0.6, 0.3],\
                 [0.1, 0.25, 0.55],\
                 [0.1],
                 [0.5, 0.25]]
        
        self.randomizedCPTs = [None] * len(self.CPTs)
        for var in xrange(0, len(self.CPTs)):
            if var == 0:
                self.randomizedCPTs[0] = [[0]*3,[0]*3]
            else:
                self.randomizedCPTs[var] = list(self.CPTs[var])

        # read the data and expand it if needed
        self.expandedData = []

        for data in trainData:
            # Dunetts Syndrome data missing
            if data[-1] == -1:
                for i in xrange(0,3):
                    copyData = list(data)
                    copyData[-1] = i
                    self.expandedData.append(copyData)
            else:
                self.expandedData.append(list(data))

        # copy the template to store the
        # sum of the weights
        self.sumWeightsDSTHTS = \
                [[0, 0],
                 [0, 0, 0]]

        self.sumWeightsPresent = \
                [[[0, 0, 0],\
                  [0, 0, 0]],\
                 [0, 0, 0],\
                 [0, 0, 0]]

        self.sumWeightsNPresent = \
                [[[0, 0, 0],\
                  [0, 0, 0]],\
                 [0, 0, 0],\
                 [0, 0, 0]]

    # randomize the CPTs, acts as a reset too
    def randomizeCPTs(self):
        # randomize with a seed
        for variable in xrange(0, 5):
            if variable == 0:
                for THTS in xrange(0, 2):
                    for DS in xrange(0, 3):
                        random.seed(self.seed)
                        randNum = random.uniform(0, self.delta)
                        self.seed = randNum

                        self.randomizedCPTs[variable][THTS][DS] = (self.CPTs[variable][THTS][DS] + randNum)/(1+2*randNum)
            elif variable < 3:
                for DS in xrange(0, 3):
                    random.seed(self.seed)
                    randNum = random.uniform(0, self.delta)
                    self.seed = randNum

                    self.randomizedCPTs[variable][DS] = (self.CPTs[variable][DS] + randNum)/(1+2*randNum)
            elif variable == 3:
                random.seed(self.seed)
                randNum = random.uniform(0, self.delta)
                self.seed = randNum

                self.randomizedCPTs[variable][0] = (self.CPTs[variable][0] + randNum)/(1 + 2*randNum)
            else:
                for DS in xrange(0,2):
                    random.seed(self.seed)
                    randNum = random.uniform(0, self.delta)
                    self.seed = randNum
                    self.randomizedCPTs[variable][DS] = (self.CPTs[variable][DS] + randNum)/(1 + 3*randNum)

    
    def changeDelta(self):
        self.delta+= ExpectationMaximizer.MAX_DELTA/self.numDeltas

    def resetSumWeights(self):
        # reset sum weight tables
        for i in xrange(0, 2):
            for j in xrange(0, 2 if i == 0 else 3):
                self.sumWeightsDSTHTS[i][j] = 0
        for i in xrange(0, 3):
            if i == 0:
                for j in xrange(0, 2):
                    for k in xrange(0, 3):
                        self.sumWeightsPresent[i][j][k] = 0
                        self.sumWeightsNPresent[i][j][k] = 0
            else:
                for k in xrange(0, 3):
                    self.sumWeightsPresent[i][k] = 0
                    self.sumWeightsNPresent[i][k] = 0

    @staticmethod
    def updateWeights(weightToUpdate, weight, index):
        weightToUpdate[index]+= weight

    def runEM(self):
        firstTrial = True
        likelihood = None

        while True:
            sumOfAllWeights = 0
            for list_data in self.expandedData:
                # either 0, 1 or 2
                DSyndrome = list_data[-1]
                weight = 1
                for i in xrange(0, len(list_data)):
                    # Sloepnea
                    if i == 0:
                        # based on the values of TRIMONO-HT/S and Dunetts Syndrome
                        multiplier = self.randomizedCPTs[i][list_data[3]][DSyndrome] if list_data[i] == 1 else\
                                     (1 - self.randomizedCPTs[i][list_data[3]][DSyndrome])
                        weight*= multiplier 
                    # Foriennditis and Degar Spots
                    elif i < 3:
                        # based on the value of Dunetts Syndrome
                        multiplier = self.randomizedCPTs[i][DSyndrome] if list_data[i] == 1 else\
                                     (1 - self.randomizedCPTs[i][DSyndrome])
                        weight*= multiplier 
                    # TRIMONO-HT/S
                    elif i == 3:
                        multiplier = self.randomizedCPTs[i][0] if list_data[i] == 1 else\
                                    (1 - self.randomizedCPTs[i][0])
                        weight*= multiplier
                    # Dunetts Syndrome
                    else:
                        multiplier = self.randomizedCPTs[i][DSyndrome] if DSyndrome == 0 or DSyndrome == 1 else\
                                 (1 - self.randomizedCPTs[i][0] - self.randomizedCPTs[i][1])
                        weight*= multiplier  
                
                for i in xrange(0, len(list_data)):
                    # Sloepnea
                    if i == 0:
                        if list_data[i] == 1:
                            ExpectationMaximizer.updateWeights(self.sumWeightsPresent[i][list_data[3]], weight, DSyndrome)
                        else:
                            ExpectationMaximizer.updateWeights(self.sumWeightsNPresent[i][list_data[3]], weight, DSyndrome)

                    # Foriennditis and Degar Spots
                    elif i < 3:
                        # based on the value of Dunetts Syndrome
                        if list_data[i] == 1:
                            ExpectationMaximizer.updateWeights(self.sumWeightsPresent[i], weight, DSyndrome)
                        else:
                            ExpectationMaximizer.updateWeights(self.sumWeightsNPresent[i], weight, DSyndrome)
                    elif i == 3:
                        # 0th index indicates presence
                        # 1st index indicates non presence
                        ExpectationMaximizer.updateWeights(self.sumWeightsDSTHTS[i-3], weight, 1-list_data[i])
                    else:
                        ExpectationMaximizer.updateWeights(self.sumWeightsDSTHTS[i-3], weight, DSyndrome)

                sumOfAllWeights+= weight

            if firstTrial:
                firstTrial = False
            elif sumOfAllWeights - likelihood <= 0.01:
                # reset before breaking out
                self.resetSumWeights()
                # if change to likelihood is small enough
                break

            likelihood = sumOfAllWeights
           
            for variable in xrange(0, len(self.randomizedCPTs)):
                # Sloepnea
                if variable == 0:
                    # loop over the domain of TRIMONO-HT/S
                    for THTS in xrange(0, 2):
                        # loop over the domain of Dunetts Syndrome
                        for DS in xrange(0, 3):
                            weightOfDSTHTS = self.sumWeightsPresent[variable][THTS][DS] + self.sumWeightsNPresent[variable][THTS][DS] 
                            self.randomizedCPTs[variable][THTS][DS] = self.sumWeightsPresent[variable][THTS][DS]/weightOfDSTHTS
                # Foriennditis and Degar Spots
                elif variable < 3:
                    for DS in xrange(0, 3):
                        weightOfDS = self.sumWeightsPresent[variable][DS] + self.sumWeightsNPresent[variable][DS]

                        self.randomizedCPTs[variable][DS] = self.sumWeightsPresent[variable][DS]/weightOfDS
                elif variable == 3:
                    self.randomizedCPTs[variable][0] = self.sumWeightsDSTHTS[variable-3][0]/sumOfAllWeights
                else:
                    self.randomizedCPTs[variable][0] = self.sumWeightsDSTHTS[variable-3][0]/sumOfAllWeights
                    self.randomizedCPTs[variable][1] = self.sumWeightsDSTHTS[variable-3][1]/sumOfAllWeights

            # reset
            self.resetSumWeights()

    def predict(self, testData):
        numCorrect = 0
        for data in testData:
            prediction = None
            # Dunetts Syndrome is not present
            noneLikelihood = 1
            # Mild Dunetts Syndrome
            mildLikelihood = 1
            # Severe Dunetts Syndrome
            severeLikelihood = 1

            for variable in xrange(0, len(self.CPTs)):
                if variable == 0:
                    noneLikelihood*= (self.randomizedCPTs[variable][data[3]][0] if data[variable] == 1 else\
                                     (1 - self.randomizedCPTs[variable][data[3]][0]))
                    mildLikelihood*= (self.randomizedCPTs[variable][data[3]][1] if data[variable] == 1 else\
                                     (1 - self.randomizedCPTs[variable][data[3]][1]))
                    severeLikelihood*= (self.randomizedCPTs[variable][data[3]][2] if data[variable] == 1 else\
                                     (1 - self.randomizedCPTs[variable][data[3]][2]))
                elif variable < 3:
                    noneLikelihood*= (self.randomizedCPTs[variable][0] if data[variable] == 1 else\
                                     (1 - self.randomizedCPTs[variable][0]))
                    mildLikelihood*= (self.randomizedCPTs[variable][1] if data[variable] == 1 else\
                                     (1 - self.randomizedCPTs[variable][1]))
                    severeLikelihood*= (self.randomizedCPTs[variable][2] if data[variable] == 1 else\
                                     (1 - self.randomizedCPTs[variable][2]))

                elif variable == 3:
                    multiplier = (self.randomizedCPTs[variable][0] if data[variable] == 1 else\
                                 (1 - self.randomizedCPTs[variable][0]))
                    noneLikelihood*= multiplier
                    mildLikelihood*= multiplier
                    severeLikelihood*= multiplier
                else:
                    noneLikelihood*= (self.randomizedCPTs[variable][0])
                    mildLikelihood*= (self.randomizedCPTs[variable][1])
                    severeLikelihood*= ((1- self.randomizedCPTs[variable][0] - self.randomizedCPTs[variable][1]))

            prediction = 0 if noneLikelihood >= mildLikelihood and noneLikelihood >= severeLikelihood else\
                         (1 if mildLikelihood >= noneLikelihood and mildLikelihood >= severeLikelihood else 2)

            numCorrect+= 1 if prediction == data[-1] else 0

        return numCorrect/len(testData)
