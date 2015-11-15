from __future__ import division
from naiveBayesLearner import NaiveBayesLearner as NBL
from preprocess import createSparseMatrix as CSM, PPWords

# predict all the documents, return the accuracy percentage
def predictDocs(learner, docs):
    numCorrectPredictions = 0
    for doc in docs:
        # correct prediction
        if learner.predict(doc) == doc[-1]:
            numCorrectPredictions+= 1
    
    return numCorrectPredictions/len(docs)

def main():
    numFeatures, featuresSet, wordsSet = PPWords(False)
    trainingMatrix = CSM('trainData.txt', 'trainLabel.txt', numFeatures)
    testMatrix = CSM('testData.txt', 'testLabel.txt', numFeatures)

    learner = NBL(featuresSet, trainingMatrix)

    trainingAccuracy = predictDocs(learner, trainingMatrix)
    testAccuracy = predictDocs(learner, testMatrix)

    print 'Training Accuracy: {:.3f}  Testing Accuracy: {:.3f}'.format(trainingAccuracy*100, testAccuracy*100)

    learner.printMostDiscriminative(wordsSet)

main()
