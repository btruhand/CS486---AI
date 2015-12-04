from __future__ import division

def expandData(data):
    expanded = []
    for d in data:
        for i in xrange(0,2):
            copy = list(d)
            copy.append(i)
            expanded.append(copy)
    return expanded

def computeNormalized(twoList, sumWeightPresent, sumWeightNPresent, CPTs):
    sumOfAllWeights = 0
    twoWeights = [0,0]
    for current in xrange(0, 2):
        data = twoList[current]
        weight = 1
        valC = data[-1]
        for var in xrange(0,len(data)):
            if var != 2:
                weight*= CPTs[var][valC] if data[var] == 1 else (1-CPTs[var][valC])
            else:
                weight*= CPTs[var][0] if data[var] == 1 else (1-CPTs[var][0])
        sumOfAllWeights+= weight
        twoWeights[current] = weight

    for current in xrange(0, 2):
        data = twoList[current]
        valC = data[-1]
        weight = twoWeights[current]/sumOfAllWeights

        for var in xrange(0, len(data)):
            if var != 2:
                if data[var] == 1:
                    sumWeightPresent[var][valC]+= weight
                else:
                    sumWeightNPresent[var][valC]+= weight
            else:
                if data[var] == 1:
                    sumWeightPresent[var][0]+= weight
                else:
                    sumWeightNPresent[var][0]+= weight

    return sumOfAllWeights

def main():
    data = []
    with open('test.txt') as f:
        for line in f:
            data.append([int(x) for x in line.strip().split()])

    CPTs = [[0.65, 0.45], [0.5, 0.3], [0.7]]
    expandedData = expandData(data)

    first = True
    likelihood = 0
    while True:
        sumWeightsPresent = [[0,0],[0,0],[0]]
        sumWeightsNPresent = [[0,0],[0,0],[0]]

        twoList = [None, None]
        count = 0
        sumOfAllWeights = 0
        for data in expandedData:
            twoList[count] = data
            count = (count+1) % 2
            if count == 0:
                sumOfAllWeights+= computeNormalized(twoList, sumWeightsPresent, sumWeightsNPresent, CPTs)

        for var in xrange(0,3):
            if var == 0:
                for valC in xrange(0,2):
                    weight = sumWeightsPresent[var][valC] + sumWeightsNPresent[var][valC]
                    CPTs[var][valC] = sumWeightsPresent[var][valC]/weight
                else:
                    CPTs[var][0] = sumWeightsPresent[var][0]/(sumWeightsPresent[var][0] + sumWeightsNPresent[var][0])
    
        if first:
            first = False
        elif sumOfAllWeights - likelihood <= 0.01:
            break
        likelihood = sumOfAllWeights

main()
