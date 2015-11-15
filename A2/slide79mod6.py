from factor import Factor

def main():
    factorC = Factor(['C'],[['t','f']],[0.32,0.68])
    factorM = Factor(['M'],[['t','f']],[0.08,0.92])
    factorBMC = Factor(['TB','M','C'], \
                       [['t','f','t','f','t','f','t','f'], \
                        ['t','t','t','t','f','f','f','f'], \
                        ['t','t','f','f','t','t','f','f']], \
                        [0.61,0.39,0.52,0.48,0.78,0.22,0.044,0.956])
    factorRB = Factor(['TB','R'],[['t','t','f','f'],['t','f','t','f']],[0.98,0.02,0.01,0.99])
    factorDR = Factor(['R','D'],[['t','t','f','f'],['t','f','t','f']],[0.96,0.04,0.001,0.999])
    

    print "Factor f0(C)"
    print factorC
    print "Factor f1(M)"
    print factorM
    print "Factor f2(TB,M,C)"
    print factorBMC
    print "Factor f3(R,TB)"
    print factorRB
    print "Factor f4(D,R)"
    print factorDR

    print Factor.inference([factorC, factorM, factorBMC, factorRB, factorDR],['C'],['R','TB','M','C'],[['D','t']])


main()
