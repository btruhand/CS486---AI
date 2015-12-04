from __future__ import division
import random

class ExpectationMaximizer(object):
    MAX_DELTA = 25
    # numDeltas - how many different deltas we will use
    # trainData - the training set
    def __init__(self, numDeltas, trainData, seed):
        self.numDeltas = numDeltas
        self.delta = 0
        self.seed = seed

        # CPTs table are for when the variable = True
        # except for Dunetts Syndrome that has 3 possible values (reduced to 2)
        # In order:
        # * Sloepnea:
        #   row is THTS 0th row is no presence of THTS, and so on. column is DS
        # * Foriennditis
        # * Degar Spots
        # * TRIMONO-HT/S
        # * Dunetts Syndrome
        self.CPTs =\
                [[[0.05, 0.45, 0.4],\
                  [0.01, 0.03, 0.03]],\
                 [0.05, 0.7, 0.3],\
                 [0.1, 0.25, 0.6],\
                 [0.1],\
                 [0.5, 0.25]]
        
        self.data = trainData

        self.randomizedCPTs = [None] * len(self.CPTs)
        for var in xrange(0, len(self.CPTs)):
            if var == 0:
                self.randomizedCPTs[0] = [[0]*3,[0]*3]
            else:
                self.randomizedCPTs[var] = list(self.CPTs[var])

        # sum of unnormalized weights (joint probabilities)
        self.sumOfJP = 0

        # read the data and compute joint probability
        # and likelihood
        # entries are keyed by data point (string form)
        # values is a list [joint probability of data point, likelihood of DS given data point]
        self.JPandLikelihoodTable = {}

        # copy the template to store the
        # sum of the likelihoods

        # contains the sum of all the likelihoods for:
        # * Sloepnea on THTS = x, DS = y (this is over all Sloepnea)
        # * Foriennditis on DS = x (this is over all Foriennditis)
        # * Degar Spots on DS = x (this is over all Degar Spots)
        # * THTS = x (this is over all THTS)
        # * DS = x (this is over all DS)
        self.sumAllLikelihood = \
                [[[0, 0, 0],\
                  [0, 0, 0]],\
                 [0, 0, 0],\
                 [0, 0, 0],\
                 [0],\
                 [0]]

        self.sumPresentLikelihood = \
                [[[0, 0, 0],\
                  [0, 0, 0]],\
                 [0, 0, 0],\
                 [0, 0, 0],
                 [0],\
                 [0,0]]

        random.seed(self.seed)

    def recomputeJPandLikelihoodTable(self):
        for S in xrange(0,2):
            for F in xrange(0,2):
                for D in xrange(0,2):
                    for THTS in xrange(0,2):
                        sumJP = 0
                        strForms = [None] * 3
                        for DS in xrange(0,3):
                            dataPoint = [S,F,D,THTS,DS]
                            strForm = str(dataPoint)
                            
                            jointProbability = 1
                            jointProbability*= self.randomizedCPTs[0][THTS][DS] if S == 1 else (1-self.randomizedCPTs[0][THTS][DS])
                            jointProbability*= self.randomizedCPTs[1][DS] if F == 1 else (1-self.randomizedCPTs[1][DS])
                            jointProbability*= self.randomizedCPTs[2][DS] if D == 1 else (1-self.randomizedCPTs[2][DS])
                            jointProbability*= self.randomizedCPTs[3][0] if THTS == 1 else (1-self.randomizedCPTs[3][0])
                            jointProbability*= self.randomizedCPTs[4][DS] if (DS == 0 or DS == 1) else\
                                               (1-self.randomizedCPTs[4][0]-self.randomizedCPTs[4][1])

                            strForms[DS] = strForm
                            self.JPandLikelihoodTable[strForm] = [jointProbability, 0]
                            sumJP+= jointProbability
                        
                        for strForm in strForms:
                            self.JPandLikelihoodTable[strForm][1] = self.JPandLikelihoodTable[strForm][0]/sumJP

    # randomize the CPTs, acts as a reset too
    def randomizeCPTs(self):
        # randomize with a seed
        for variable in xrange(0, 5):
            if variable == 0:
                for THTS in xrange(0, 2):
                    for DS in xrange(0, 3):
                        randNum1 = random.uniform(0, self.delta)
                        randNum2 = random.uniform(0, self.delta)
                        self.randomizedCPTs[variable][THTS][DS] = (self.CPTs[variable][THTS][DS] + randNum1)/(1 + randNum1 + randNum2)
            elif variable < 3:
                for DS in xrange(0, 3):
                    randNum1 = random.uniform(0, self.delta)
                    randNum2 = random.uniform(0, self.delta)
                    self.randomizedCPTs[variable][DS] = (self.CPTs[variable][DS] + randNum1)/(1 + randNum1 + randNum2)
            elif variable == 3:
                randNum1 = random.uniform(0, self.delta)
                randNum2 = random.uniform(0, self.delta)
                self.randomizedCPTs[variable][0] = (self.CPTs[variable][0] + randNum1)/(1 + randNum1 + randNum2)
            else:
                for DS in xrange(0,2):
                    randNum1 = random.uniform(0, self.delta)
                    randNum2 = random.uniform(0, self.delta)
                    randNum3 = random.uniform(0, self.delta)
                    self.randomizedCPTs[variable][DS] = (self.CPTs[variable][DS] + randNum1)/(1 + randNum1 + randNum2 + randNum3)
    
    def changeDelta(self):
        self.delta+= ExpectationMaximizer.MAX_DELTA/self.numDeltas

    def resetSumWeights(self):
        self.sumOfJP = 0
        # reset sum weight tables
        for var in xrange(0, 5):
            if var == 0:
                for THTS in xrange(0, 2):
                    for DS in xrange(0, 3):
                        self.sumAllLikelihood[var][THTS][DS] = 0
                        self.sumPresentLikelihood[var][THTS][DS] = 0
            else:
                for var2 in xrange(0, len(self.sumPresentLikelihood[var])):
                    if var == 4:
                        if var2 == 0:
                            self.sumAllLikelihood[var][var2] = 0
                    else:
                        self.sumAllLikelihood[var][var2] = 0
                    self.sumPresentLikelihood[var][var2] = 0

    def accumulateLikelihood(self, dataPoint, likelihoodVal):
        S = dataPoint[0]
        F = dataPoint[1]
        D = dataPoint[2]
        THTS = dataPoint[3]
        DS = dataPoint[4]
        
        # sum up all likelihood values
        self.sumAllLikelihood[0][THTS][DS]+= likelihoodVal
        self.sumAllLikelihood[1][DS]+= likelihoodVal
        self.sumAllLikelihood[2][DS]+= likelihoodVal
        self.sumAllLikelihood[3][0]+= likelihoodVal
        self.sumAllLikelihood[4][0]+= likelihoodVal

        if S == 1:
            self.sumPresentLikelihood[0][THTS][DS]+= likelihoodVal
        if F == 1:
            self.sumPresentLikelihood[1][DS]+= likelihoodVal
        if D == 1:
            self.sumPresentLikelihood[2][DS]+= likelihoodVal
        if THTS == 1:
            self.sumPresentLikelihood[3][0]+= likelihoodVal
        if DS == 0 or DS == 1:
            self.sumPresentLikelihood[4][DS]+= likelihoodVal

    def runEM(self):
        likelihood = None

        while True:
            # recompute JP and likelihood table first
            self.recomputeJPandLikelihoodTable()
            for data in self.data:
                if data[-1] == -1:
                    # splitting the data
                    for DS in xrange(0,3):
                        # change the value of DS
                        data[-1] = DS
                        strForm = str(data)
                       
                        self.sumOfJP+= self.JPandLikelihoodTable[strForm][0]
                        self.accumulateLikelihood(data, self.JPandLikelihoodTable[strForm][1])

                    # return it to -1
                    data[-1] = -1
                else:
                    # DS is observed
                    self.sumOfJP+= self.JPandLikelihoodTable[str(data)][0]
                    self.accumulateLikelihood(data, 1)

            # update CPTs
            # update Sloepnea
            for THTS in xrange(0,2):
                for DS in xrange(0,3):
                    self.randomizedCPTs[0][THTS][DS] = self.sumPresentLikelihood[0][THTS][DS] / self.sumAllLikelihood[0][THTS][DS]
            
            # update Foriennditis and Degar Spotes
            for DS in xrange(0,3):
                self.randomizedCPTs[1][DS] = self.sumPresentLikelihood[1][DS] / self.sumAllLikelihood[1][DS]
                self.randomizedCPTs[2][DS] = self.sumPresentLikelihood[2][DS] / self.sumAllLikelihood[2][DS]

            # update THTS
            self.randomizedCPTs[3][0] = self.sumPresentLikelihood[3][0] / self.sumAllLikelihood[3][0]

            # update DS
            self.randomizedCPTs[4][0] = self.sumPresentLikelihood[4][0] / self.sumAllLikelihood[4][0]
            self.randomizedCPTs[4][1] = self.sumPresentLikelihood[4][1] / self.sumAllLikelihood[4][0]

            if likelihood != None and (self.sumOfJP - likelihood) <= 0.01:
                # reset first
                self.resetSumWeights()
                # then break
                break

            likelihood = self.sumOfJP

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
                    severeLikelihood*= (1- self.randomizedCPTs[variable][0] - self.randomizedCPTs[variable][1])

            prediction = 0 if noneLikelihood >= mildLikelihood and noneLikelihood >= severeLikelihood else\
                         (1 if mildLikelihood >= noneLikelihood and mildLikelihood >= severeLikelihood else 2)

            numCorrect+= 1 if prediction == data[-1] else 0

        return numCorrect/len(testData)
