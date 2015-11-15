from sets import Set

def createSparseMatrix(dataFile, labelFile, numFeatures):
    sparseMatrix = []

    with open(labelFile, 'r') as f:
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
    
    with open(labelFile, 'r') as f:
        docId = 0
        for line in f:
            sparseMatrix[docId][-1] = int(line)
            docId+= 1

    return sparseMatrix

# preprocess the words/features
def PPWords(makeset):
    numFeatures = 0
    featuresSet = []
    if makeset:
        featuresSet = Set(featuresSet)

    wordsSet = []
    with open('words.txt', 'r') as f:
        for line in f:
            if makeset:
                featuresSet.add(numFeatures)
            else:
                featuresSet.append(numFeatures)
            wordsSet.append(line.rstrip())
            numFeatures+= 1

    return (numFeatures, featuresSet, wordsSet)
