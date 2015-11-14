from __future__ import division
from decisionTreeNode import DecisionTreeNode as DTN
from decisionTreeLearner import DecisionTreeLearner as DTL
from sets import Set

def createSparseMatrix(dataFile, labelFile, numFeatures):
    sparseMatrix = []

    with open('trainLabel.txt', 'r') as f:
        docId = 0
        for line in f:
            sparseMatrix.append([0] * (numFeatures + 1))
            sparseMatrix[docId][-1] = int(line)
            docId+= 1
    
    with open(dataFile, 'r') as f:
        for line in f:
            lineSplit = line.split()
            fileID = int(lineSplit[0])
            featureNum = int(lineSplit[1])

            # 0 indexing remember while the ID and features are 1 indexing
            # indicate presence of word/feature
            sparseMatrix[fileID-1][featureNum-1] = 1
    
    with open('trainLabel.txt', 'r') as f:
        docId = 0
        for line in f:
            sparseMatrix[docId][-1] = int(line)
            docId+= 1

    return sparseMatrix

# returns the number of predictions that are correct
def calculatePredictions(learnTreeGenerator, docs1, docs2, predictionRatio1, predictionRatio2):
    numDocuments1 = len(docs1)
    numDocuments2 = len(docs2)
    for learnTree in learnTreeGenerator:
        numCorrectPredictionDocs1 = 0
        numCorrectPredictionDocs2 = 0
        for doc in docs1:
            prediction = DTN.predict(learnTree, doc)
            if prediction == doc[-1]:
                # if the prediction was correct
                numCorrectPredictionDocs1+= 1
        
        for doc in docs2:
            prediction = DTN.predict(learnTree, doc)
            if prediction == doc[-1]:
                numCorrectPredictionDocs2+= 1
        
        predictionRatio1.append(numCorrectPredictionDocs1/numDocuments1 * 100)
        predictionRatio2.append(numCorrectPredictionDocs2/numDocuments2 * 100)

def main():
    numFeatures = 0
    featuresSet = Set([])
    wordsSet = []
    with open('words.txt', 'r') as f:
        for line in f:
            featuresSet.add(numFeatures)
            wordsSet.append(line.rstrip())
            numFeatures+= 1

    trainingMatrix = createSparseMatrix('trainData.txt', 'trainLabel.txt', numFeatures)
    testMatrix = createSparseMatrix('testData.txt', 'testLabel.txt', numFeatures)
    numOfTrainingDocs = len(trainingMatrix)
    numOfTestDocs = len(testMatrix)

    learnerProportion = DTL(trainingMatrix, featuresSet, DTN.PROPORTIONMODE)
    learnerAvg = DTL(trainingMatrix, featuresSet, DTN.AVGMODE)

    proportionLearning = learnerProportion.learn(wordsSet)
    avgLearning = learnerAvg.learn(wordsSet)

    # percentage of correct predictions for proportion mode decision tree
    # as the number of nodes increases/as the tree gets expanded
    correctPredictionsProportionTest = []
    correctPredictionsProportionTrain = []

    # percentage of correct predictions for avg mode decision tree
    # as the number of nodes increases/as the tree gets expanded
    correctPredictionsAvgTest = []
    correctPredictionsAvgTrain = []

    calculatePredictions(proportionLearning, testMatrix, trainingMatrix, \
                            correctPredictionsProportionTest, correctPredictionsProportionTrain)
    calculatePredictions(avgLearning, testMatrix, trainingMatrix, \
                            correctPredictionsAvgTest, correctPredictionsAvgTrain)
'''
    with open('q1predictionGraphProportion.txt','w') as f:
        f.write('{!s:10}{!s:20}{!s}\r\n'.format('expand #', 'testing accuracy', 'training accuracy'))
        for i in xrange(0, len(correctPredictionsProportionTest)):
            f.write('{:<10}{:<20.3f}{:<.3f}\r\n'.format(i, correctPredictionsProportionTest[i], correctPredictionsProportionTrain[i]))

    with open('q1predictiongraphAvg.txt','w') as f:
        f.write('{!s:10}{!s:20}{!s}\r\n'.format('expand #', 'testing accuracy', 'training accuracy'))
        for i in xrange(0, len(correctPredictionsAvgTest)):
            f.write('{:<10}{:<20.3f}{:<.3f}\r\n'.format(i, correctPredictionsAvgTest[i], correctPredictionsAvgTrain[i]))
'''
main()
