from math import log10,floor

class Factor(object):
    # width during formatting
    STRWIDTH = 10
    # round up to roundTo decimal places
    ROUNDTO = 3

    # method to round up to n significant figures
    @staticmethod
    def round_to_n_sigfig(x):
        return round(x, -int(floor(log10(x))-(Factor.ROUNDTO-1)))

    # Parameters:
    # varList: a list of variables
    # varValues: a 2D array where each i-th array represents the values
    #            of the i-th variable in each row in a row-based factor.
    #            Hence the representation here is column-based
    # mappedValues: a 1D array where the i-th entry is the probability
    #               of the i-th row in a row-based factor
    def __init__(self, varList, varValues, mappedValues):
        self.factorTable = dict()
        self.mappedValues = mappedValues
        for i in xrange(0,len(varList)):
            self.factorTable[varList[i]] = varValues[i]

    # Restrict this factor on a variable with a particular value
    def restrict(self, variable, value):
        # grab the indices where value occur for given variable
        valueIndex = [i for i, val in enumerate(self.factorTable[variable]) if val == value]
        # take out the variable from the table
        del self.factorTable[variable]
      
        # restricting step
        vars = self.factorTable.keys()

        restrictedVars = map(lambda var: [val for i, val in enumerate(self.factorTable[var]) if i in valueIndex], vars)
        self.mappedValues = [val for i, val in enumerate(self.mappedValues) if i in valueIndex]
        for i in xrange(0, len(vars)):
            self.factorTable[vars[i]] = restrictedVars[i]

    # calculate the product of two factors
    # assumption is that the two factors have a set of variables in common
    @staticmethod
    def multiply(factor1, factor2):
        factor1Vars = factor1.factorTable.keys()
        factor2Vars = factor2.factorTable.keys()
        newVariables = [var for var in factor1Vars if var in factor2Vars]

        # grab the rows of factor2 that needs to
        # be multiplied with the rows of factor1
        multiplyWith = [[] for i in xrange(len(factor1.mappedValues))]
        numMappedValues = 0
        for i in xrange(len(multiplyWith)):
            for j in xrange(len(factor2.mappedValues)):
                sameOverlapValues = True
                for var in newVariables:
                    if factor1.factorTable[var][i] != factor2.factorTable[var][j]:
                        sameOverlapValues = False
                        # end early
                        break
                # if overlap variables has same values
                if sameOverlapValues:
                    multiplyWith[i].append(j)
                    numMappedValues+= 1
                

        newVariables.extend([var for var in factor1Vars if var not in newVariables])
        newVariables.extend([var for var in factor2Vars if var not in newVariables])

        newValues = [[] for i in xrange(len(newVariables))]
        newMappedValues = []

        enumerated = tuple(enumerate(newVariables))
        # for each row in factor1
        for row in xrange(len(multiplyWith)):
            # for each rows in factor2 to be multiplied
            # with a row in in factor1
            for rowInFactor2 in multiplyWith[row]:
                for i, var in enumerated:
                    # insert each variable's values on each row
                    newValues[i].append(factor1.factorTable[var][row] if var in factor1Vars \
                                        else factor2.factorTable[var][rowInFactor2])
                # append mutiplied values, up to 3 decimal places
                newMappedValues.append(Factor.round_to_n_sigfig(factor1.mappedValues[row] * factor2.mappedValues[rowInFactor2]))

        return Factor(newVariables, newValues, newMappedValues)

    # sum a variable in a factor
    def sumout(self, variable):
        if len(self.factorTable.keys()) == 1:
            # by the definition of summing out a variable from a factor
            # we cannot sumout a factor that only has 1 variable
            return

        # get the domain of the variable
        uniqueValuesForVar = set(self.factorTable[variable])
        # delete the variable from the factor table
        del self.factorTable[variable]
        sumRows = []
        allVars = self.factorTable.keys()
        for i in xrange(len(self.mappedValues)):
            if i in sumRows:
                # if i is already in sumRows continue to next iteration
                continue

            limitMatch = len(self.mappedValues) / len(uniqueValuesForVar)

            # only check forward
            for j in xrange(i+1, len(self.mappedValues)):
                sameValues = True
                for var in allVars:
                    if self.factorTable[var][i] != self.factorTable[var][j]:
                        sameValues = False
                # if variables not to be summed have same value
                # in another row and not already registered
                if sameValues and j not in sumRows:
                    sumRows.append(j)
                    limitMatch-= 1

                # if we've found matches up to limitMatch amount
                if limitMatch == 0:
                    # end early
                    break

        newValues = [[] for i in xrange(len(allVars))]
        # create a new list of mapped values with length
        newMappedValues = []
        enumerated = list(enumerate(allVars))
        sumRowIndex = 0
        for i in xrange(len(self.mappedValues)):
            # if we're currently at the index that
            # we're trying to sum with
            if i in sumRows:
                continue

            for k, var in enumerated:
                newValues[k].append(self.factorTable[var][i])

            # add the rows for a particular variable value
            sum = self.mappedValues[i]
            for j in xrange(0, len(uniqueValuesForVar)-1):
                sum+= self.mappedValues[sumRows[sumRowIndex]]
                sumRowIndex+= 1
            
            newMappedValues.append(sum)

        for j, var in enumerated:
            # clear the values for the table
            del self.factorTable[var][:]
            self.factorTable[var].extend(newValues[j])

        # clear mapped values
        del self.mappedValues[:]
        self.mappedValues.extend(newMappedValues)

    # normalize a factor
    def normalize(self):
        addUpMappedValues = sum(self.mappedValues)
        self.mappedValues[:] = map(lambda x: Factor.round_to_n_sigfig(x/addUpMappedValues), self.mappedValues)

    # inference using factors
    @staticmethod
    def inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList):
        # filter out the variables which are in the
        # query and evidence from orderedListOfHiddenVariables
        if len(evidenceList) > 0:
            evidenceVars = zip(*evidenceList)[0]
        else:
            evidenceVars = []
        orderedListOfHiddenVariables = filter(lambda x: x not in queryVariables \
                                                   and x not in evidenceVars, orderedListOfHiddenVariables)

        for evidence in evidenceList:
            for factor in factorList:
                # if the evidence variable is in the factor
                if evidence[0] in factor.factorTable.keys():
                    factor.restrict(evidence[0], evidence[1])
        
        evidences = reduce(lambda x,y: '{!s}, {!s}'.format(x,y), evidenceList) if len(evidenceList) > 0 else 'nothing'
        Factor.textFormattedPrint('Result of restricting factors on evidence {!s}'.format(evidences), 50, factorList)

        for hiddenVar in orderedListOfHiddenVariables:
            factorsWithHiddenVar = []
            for factor in factorList:
                if hiddenVar in factor.factorTable.keys():
                    factorsWithHiddenVar.append(factor)
        
            # take out all the factors with a hidden variable from the list
            factorList = filter(lambda x: x not in factorsWithHiddenVar, factorList)

            # get product of hidden variables
            if len(factorsWithHiddenVar) > 0:
                Factor.textFormattedPrint('Summing over {!s}'.format(hiddenVar), 30, [])
                # if there are actually factors to multiply
                productFactor = reduce(Factor.multiply, factorsWithHiddenVar)
            else:
                # no factors to multiply, nothing to do here
                continue

            Factor.textFormattedPrint('Intermediate product factor on {!s}'.format(hiddenVar),30,[productFactor])
            
            # summing over the hidden variable on the product factor 
            productFactor.sumout(hiddenVar)
            Factor.textFormattedPrint('Summing out variable {!s}'.format(hiddenVar),30,[productFactor])

            # insert the result back to the list 
            factorList.append(productFactor)

        # the only thing left now can only be factors with
        # only the query variable, we multiply them together
        inferredFactor = reduce(Factor.multiply, factorList)
        Factor.textFormattedPrint('Result of multiplying factors with query variables: {!s}'.\
                                        format(queryVariables),45,[inferredFactor])

        # normalize stage
        inferredFactor.normalize()
        Factor.textFormattedPrint('Normalized result',30,[inferredFactor])

    # method to create an exact copy of a factor
    def copy(self):
        keyvalues = self.factorTable.items()
        return Factor(map(lambda x: x[0], keyvalues), map(lambda x: x[1], keyvalues), self.mappedValues)


    # used to get the string form of this factor
    def __str__(self):
        formatting = ''
        vars = self.factorTable.keys()
        # create a format string to use
        for i in xrange(0, len(vars)+1):
            formatting+= '{!s:{width}}'
            if i == len(vars):
                formatting+= '\r\n'

        # create the formatted header
        toRet = formatting.format('MappedVal', *vars, width=Factor.STRWIDTH)
        # zip the values of each variables and the mapped value. Creates a row of values
        # with each column representing a value for each variable and the last column
        # having the mapped value when the variable has those values
        # essentially make this a table format of the factor
        zippedValues = zip(self.mappedValues, *map(lambda x: self.factorTable[x], vars))

        # for each value create the formatted row
        for values in zippedValues:
            toRet+= formatting.format(*values, width=Factor.STRWIDTH)

        return toRet

    # deletion mechanism
    def __del__(self):
        del self.mappedValues
        # clear factor table
        self.factorTable.clear()
        del self.factorTable

    @staticmethod
    def textFormattedPrint(statement, dashNum, factors):
        print statement, '\r'
        print '-' * dashNum, '\r'
        for factor in factors:
            print factor, '\r'

        print '-' * dashNum, '\r'
