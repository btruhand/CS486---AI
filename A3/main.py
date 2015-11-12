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
            print len(sparseMatrix), fileID, featureNum
            sparseMatrix[fileID-1][featureNum-1] = 1
    
    with open('trainLabel.txt', 'r') as f:
        docId = 0
        for line in f:
            sparseMatrix[docId][-1] = int(line)
            docId+= 1

    return sparseMatrix

# returns the number of predictions that are correct
def calculatePredictions(learnTreeGenerator, testDocs):
    for learnTree in learnTreeGenerator:
        numCorrectPrediction = 0
        for testDoc in testMatrix:
            prediction = DTN.predict(learnTree, testDoc)
            if prediction == testDoc[-1]:
                # if the prediction was correct
                numCorrectPrediction+= 1
        
        yield numCorrectPrediction

def main():
    numFeatures = 0
    featureSets = Set([])
    with open('words.txt', 'r') as f:
        for line in f:
            featureSets.add(numFeatures)
            numFeatures+= 1

    trainingMatrix = createSparseMatrix('trainData.txt', 'trainLabel.txt', numFeatures)
    testMatrix = createSparseMatrix('testData.txt', 'testLabel.txt', numFeatures)
    numOfTrainingDocs = len(trainingMatrix)
    numOfTestDocs = len(testMatrix)

    learnerProportion = DTL(trainingMatrix, featureSets, DTN.PROPORTION)
    learnerAvg = DTL(trainingMatrix, featureSets, DTN.AVG)

    proportionLearning = learnerProportion.learn()
    #avgLearning = learnerAvg.learn()

    # percentage of correct predictions for proportion mode decision tree
    # as the number of nodes increases/as the tree gets expanded
    correctPredictionsProportion = []

    # percentage of correct predictions for avg mode decision tree
    # as the number of nodes increases/as the tree gets expanded
    correctPredictionsAvg = []

    proportionPredictionGen = calculatePredictions(proportionLearning, testMatrix)
    for corPrediction in proportionPredictionGen:
        correctPredictionsProportion.push((corPrediction / numOfTestDocs) * 100)

    print correctPredictionsAvg

    '''
    avgPredictionGen = calculatePredictions(avgLearning, testMatrix)
    for corPrediction in proportionPredictionGen:
        correctPredictionsAvg.push((corPrediction / numOfTestDocs) * 100)
    '''

main()
