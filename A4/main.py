from expectationMaximizer import ExpectationMaximizer as EM

def createDataSet(filename):
    matrix = []
    with open(filename, 'r') as f:
        for line in f:
            matrix.append([int(x) for x in line.strip().split()])

    return matrix


def main():
	numDeltas = 25
	trainData = createDataSet('traindata.txt')
	testData = createDataSet('testdata.txt')
	em = EM(25, trainData, None)

	for i in xrange(0, numDeltas):
		# take numDeltas many deltas
		accuracyBeforeAndAfter = []
	
		for j in xrange(0, 20):
			# do 20 trials everytime
			em.randomizeCPTs()
			beforeEM = em.predict(testData)

			em.runEM()
			afterEM = em.predict(testData)

			accuracyBeforeAndAfter.append((beforeEM, afterEM))	

		print '{!s:10},  {!s}, Delta:{}\r'.format('Before EM', 'After EM', em.delta)
		for accuracy in accuracyBeforeAndAfter:
			print '{:<10.3f},  {:.3f}\r'.format(accuracy[0], accuracy[1])

		print '\r\n'

		em.changeDelta()

main()
