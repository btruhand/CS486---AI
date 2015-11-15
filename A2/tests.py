from factor import Factor

def main():
    values = [['t', 't', 't', 't', 'f', 'f', 'f', 'f'],
              ['t', 't', 'f', 'f', 't', 't', 'f', 'f'],
              ['t', 'f', 't', 'f', 't', 'f', 't', 'f']]
    variables = ['X', 'Y', 'Z']
    mappedValues = [0.1, 0.9, 0.2, 0.8, 0.4, 0.6, 0.3, 0.7]

    aFactor = Factor(variables, values, mappedValues)
    print aFactor
    aFactor.restrict('Z', 'f')
    print aFactor
    aFactor.restrict('X', 't')
    print aFactor

    del aFactor

    factor1 = Factor(['A', 'B'], [['t', 't', 'f', 'f'], ['t', 'f', 't', 'f']], [0.1, 0.9, 0.2, 0.8])
    factor2 = Factor(['B', 'C'], [['t', 't', 'f', 'f'], ['t', 'f', 't', 'f']], [0.3, 0.7, 0.6, 0.4])
    print factor1
    print factor2
    newFactor = Factor.multiply(factor1, factor2)
    del factor1
    del factor2
    print newFactor
    newFactor.normalize()
    print newFactor
    del newFactor

    anotherFactor = Factor(['A','B','C'],
                            [['t','t','t','t','f','f','f','f'],
                            ['t','t','f','f','t','t','f','f'],
                            ['t','f','t','f','t','f','t','f']],
                            [0.03,0.07,0.54,0.36,0.06,0.14,0.48,0.32])
    anotherFactor.sumout('B')
    print anotherFactor
    
    # example from slide 75
    factorA = Factor(['A'],[['t','f']], [0.3, 0.7])
    factorCA = Factor(['A','C'],[['t','t','f','f'],['t','f','t','f']],[0.8, 0.2, 0.15, 0.85])
    factorGC = Factor(['C', 'G'],[['t','t','f','f'],['t','f','t','f']],[1.0, 0.0, 0.2, 0.8])
    factorLG = Factor(['G', 'L'],[['t','t','f','f'],['t','f','t','f']],[0.7, 0.3, 0.2, 0.8])
    factorStrueL = Factor(['L','S'],[['t','t','f','f'],['t','f','t','f']],[0.9,0.1,0.3,0.7])

    resultFactor = Factor.inference([factorA,factorCA,factorGC,factorLG,factorStrueL],['S'],['L','G','C','A'],[])
    print resultFactor

main()
