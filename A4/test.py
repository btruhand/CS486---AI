from __future__ import division

def test(t):
   t[0] = 3

def main():
    l = [1,2,3]
    test(l)
    print l

main()
