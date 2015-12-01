from __future__ import division
from expectationMaximizer import ExpectationMaximizer as EM
from math import sqrt

def createDataSet(filename):
    matrix = []
    with open(filename, 'r') as f:
        for line in f:
            matrix.append([int(x) for x in line.strip().split()])

    return matrix

def calcMeanAndStdDev(accuracies):
    mean = sum(accuracies)/len(accuracies)
    stddev = sqrt((1/(len(accuracies)-1)) * reduce(lambda x,y: x + (y-mean)**2, accuracies, 0))

    return (mean,stddev)

def main():
    numDeltas = 25
    trainData = createDataSet('traindata.txt')
    testData = createDataSet('testdata.txt')
    em = EM(25, trainData, None)
    
    meanAccuracyBefore = []
    meanAccuracyAfter = []
    for i in xrange(0, numDeltas):
        # take numDeltas many deltas
        accuracyBeforeAndAfter = [[],[]]
        
        for j in xrange(0, 20):
            # do 20 trials everytime
            em.randomizeCPTs()
            beforeEM = em.predict(testData)
            
            em.runEM()
            afterEM = em.predict(testData)
            
            accuracyBeforeAndAfter[0].append(beforeEM)
            accuracyBeforeAndAfter[1].append(afterEM)
       
        meanAccuracyBefore.append(calcMeanAndStdDev(accuracyBeforeAndAfter[0]))
        meanAccuracyAfter.append(calcMeanAndStdDev(accuracyBeforeAndAfter[1]))

        em.changeDelta()

    print 'Mean Before and After EM\r'
    print 'Delta\r'
    for delta in xrange(0, numDeltas):
        print '{:<5f}, {:3.3f}, {:.3f}\r'.format(delta * (4/numDeltas), meanAccuracyBefore[delta][0],\
                meanAccuracyAfter[delta][0])
                
    print '\r\n'

    print 'StdDev Before and After EM\r'
    print 'Delta\r'
    for delta in xrange(0, numDeltas):
        print '{:<5.2f}, {:3.3f}, {:.3f}\r'.format(delta * (4/numDeltas), meanAccuracyBefore[delta][1],\
                meanAccuracyAfter[delta][1])
                
    print '\r\n'

main()
