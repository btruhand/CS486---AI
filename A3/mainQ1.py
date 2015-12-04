from __future__ import division
from decisionTreeNode import DecisionTreeNode as DTN
from decisionTreeLearner import DecisionTreeLearner as DTL
from preprocess import createSparseMatrix as CSM, PPWords

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
    numFeatures, featuresSet, wordsSet = PPWords(True)

    trainingMatrix = CSM('trainData.txt', 'trainLabel.txt', numFeatures)
    testMatrix = CSM('testData.txt', 'testLabel.txt', numFeatures)
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

    with open('q1predictionGraphProportion.txt','w') as f:
        f.write('{!s:10}{!s:20}{!s}\r\n'.format('Expand #', 'Testing accuracy', 'Training Accuracy'))
        for i in xrange(0, len(correctPredictionsProportionTest)):
            f.write('{:<10}{:<20.3f}{:<.3f}\r\n'.format(i+1, correctPredictionsProportionTest[i], correctPredictionsProportionTrain[i]))

    with open('q1predictionGraphAvg.txt','w') as f:
        f.write('{!s:10}{!s:20}{!s}\r\n'.format('Expand #', 'Testing Accuracy', 'Training Accuracy'))
        for i in xrange(0, len(correctPredictionsAvgTest)):
            f.write('{:<10}{:<20.3f}{:<.3f}\r\n'.format(i+1, correctPredictionsAvgTest[i], correctPredictionsAvgTrain[i]))

main()
