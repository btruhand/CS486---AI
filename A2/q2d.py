from factor import Factor

def main():
    hiddenVariables = ['Trav','FP','Fraud','IP','OC','CRP']
    factorTrav = Factor(['Trav'], [['t','f']], [0.05,0.95])
    factorFraudTrav = Factor(['Fraud','Trav'],[['t','t','f','f'],['t','f','t','f']],[0.01,0.004,0.99,0.996])
    factorFPFraudTrav = Factor(['FP','Fraud','Trav'],[['t','t','t','t','f','f','f','f'],
                                                      ['t','t','f','f','t','t','f','f'],
                                                      ['t','f','t','f','t','f','t','f']],
                                                      [0.9,0.1,0.9,0.01,0.1,0.9,0.1,0.99])
    factorIPFraudOC = Factor(['IP','Fraud','OC'],[['t','t','t','t','f','f','f','f'],
                                                  ['t','t','f','f','t','t','f','f'],
                                                  ['t','f','t','f','t','f','t','f']],
                                                  [0.02,0.011,0.01,0.001,0.98,0.989,0.99,0.999])
    factorCRPOC = Factor(['CRP','OC'],[['t','t','f','f'],['t','f','t','f']],[0.1,0.001,0.9,0.999])
    factorOC = Factor(['OC'],[['t','f']],[0.6,0.4])

    copyfactorTrav = factorTrav.copy()
    copyfactorFraudTrav = factorFraudTrav.copy()
    copyfactorFPFraudTrav = factorFPFraudTrav.copy()
    copyfactorIPFraudOC = factorIPFraudOC.copy()
    copyfactorCRPOC = factorCRPOC.copy()
    copyfactorOC = factorOC.copy()
    Factor.inference([copyfactorTrav,copyfactorFraudTrav,copyfactorFPFraudTrav,copyfactorIPFraudOC,copyfactorOC,copyfactorCRPOC],
                     ['Fraud'],hiddenVariables,[['IP','t']])
    Factor.inference([factorTrav,factorFraudTrav,factorFPFraudTrav,factorIPFraudOC,factorOC,factorCRPOC],
                     ['Fraud'],hiddenVariables,[['IP','t'],['CRP','t']])


main()
