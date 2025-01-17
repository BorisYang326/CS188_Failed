# factorOperations.py
# -------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from functools import reduce
from bayesNet import Factor
import operator as op
import util

def joinFactorsByVariableWithCallTracking(callTrackingList=None):


    def joinFactorsByVariable(factors, joinVariable):
        """
        Input factors is a list of factors.
        Input joinVariable is the variable to join on.

        This function performs a check that the variable that is being joined on 
        appears as an unconditioned variable in only one of the input factors.

        Then, it calls your joinFactors on all of the factors in factors that 
        contain that variable.

        Returns a tuple of 
        (factors not joined, resulting factor from joinFactors)
        """

        if not (callTrackingList is None):
            callTrackingList.append(('join', joinVariable))

        currentFactorsToJoin =    [factor for factor in factors if joinVariable in factor.variablesSet()]
        currentFactorsNotToJoin = [factor for factor in factors if joinVariable not in factor.variablesSet()]

        # typecheck portion
        numVariableOnLeft = len([factor for factor in currentFactorsToJoin if joinVariable in factor.unconditionedVariables()])
        if numVariableOnLeft > 1:
            print ("Factor failed joinFactorsByVariable typecheck: ", factor)
            raise ValueError ("The joinBy variable can only appear in one factor as an \nunconditioned variable. \n" +  
                               "joinVariable: " + str(joinVariable) + "\n" +
                               ", ".join(map(str, [factor.unconditionedVariables() for factor in currentFactorsToJoin])))
        
        joinedFactor = joinFactors(currentFactorsToJoin)
        return currentFactorsNotToJoin, joinedFactor

    return joinFactorsByVariable

joinFactorsByVariable = joinFactorsByVariableWithCallTracking()


def joinFactors(factors):
    """
    Question 3: Your join implementation 

    Input factors is a list of factors.  
    
    You should calculate the set of unconditioned variables and conditioned 
    variables for the join of those factors.

    Return a new factor that has those variables and whose probability entries 
    are product of the corresponding rows of the input factors.

    You may assume that the variableDomainsDict for all the input 
    factors are the same, since they come from the same BayesNet.

    joinFactors will only allow unconditionedVariables to appear in 
    one input factor (so their join is well defined).

    Hint: Factor methods that take an assignmentDict as input 
    (such as getProbability and setProbability) can handle 
    assignmentDicts that assign more variables than are in that factor.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """

    # typecheck portion
    factors = list(factors)
    setsOfUnconditioned = [set(factor.unconditionedVariables()) for factor in factors]
    if len(factors) > 1:
        intersect = reduce(lambda x, y: x & y, setsOfUnconditioned)
        if len(intersect) > 0:
            print ("Factor failed joinFactors typecheck: ", factor)
            raise ValueError ("unconditionedVariables can only appear in one factor. \n"
                    + "unconditionedVariables: " + str(intersect) + 
                    "\nappear in more than one input factor.\n" + 
                    "Input factors: \n" +
                    "\n".join(map(str, factors)))

    "*** YOUR CODE HERE ***"
    sub_uncondition_list = []
    sub_condition_list = []
    uncondition = ()
    condition = ()
    tem_set_unc = set([])
    tem_set_con = set([])
    final_dic = []
    i=0
    for factor in factors:
        sub_uncondition_list.append(factor.unconditionedVariables())
        tem_set_unc |= factor.unconditionedVariables()
        tem_set_con |= factor.conditionedVariables()
        sub_condition_list.append(factor.conditionedVariables())
        # for tem_var in sub_condition_list:
        uncondition = list(tem_set_unc)
        condition = list(tem_set_con - (tem_set_con & set(uncondition)))
    JointFactor = Factor(uncondition, condition, factors[0].variableDomainsDict())
    #print JointFactor
    #print 'print in joint'
    for new_dic in JointFactor.getAllPossibleAssignmentDicts():
        prob = 1.0
        for factor in factors:
            prob *= factor.getProbability(new_dic)
            #print  str(factor.getProbability(new_dic)) +'       '+str(prob)
        #print new_dic
        final_dic.append((new_dic,prob))
    #print final_dic
    for i in final_dic:
        #print '*********'
        #print i[0]
        JointFactor.setProbability(i[0], i[1])
    #print JointFactor
    #print 'print prob'
    return JointFactor
    # for i in factors:
    #     print (i.getAllPossibleAssignmentDicts())
    #     x=i.getProbability(i.getAllPossibleAssignmentDicts)
    #     x*=i.
    #util.raiseNotDefined()


def eliminateWithCallTracking(callTrackingList=None):

    def eliminate(factor, eliminationVariable):
        """
        Question 4: Your eliminate implementation 

        Input factor is a single factor.
        Input eliminationVariable is the variable to eliminate from factor.
        eliminationVariable must be an unconditioned variable in factor.
        
        You should calculate the set of unconditioned variables and conditioned 
        variables for the factor obtained by eliminating the variable
        eliminationVariable.

        Return a new factor where all of the rows mentioning
        eliminationVariable are summed with rows that match
        assignments on the other variables.

        Useful functions:
        Factor.getAllPossibleAssignmentDicts
        Factor.getProbability
        Factor.setProbability
        Factor.unconditionedVariables
        Factor.conditionedVariables
        Factor.variableDomainsDict
        """
        # autograder tracking -- don't remove
        if not (callTrackingList is None):
            callTrackingList.append(('eliminate', eliminationVariable))

        # typecheck portion
        if eliminationVariable not in factor.unconditionedVariables():
            print ("Factor failed eliminate typecheck: ", factor)
            raise ValueError ("Elimination variable is not an unconditioned variable " \
                            + "in this factor\n" + 
                            "eliminationVariable: " + str(eliminationVariable) + \
                            "\nunconditionedVariables:" + str(factor.unconditionedVariables()))
        
        if len(factor.unconditionedVariables()) == 1:
            print ("Factor failed eliminate typecheck: ", factor)
            raise ValueError ("Factor has only one unconditioned variable, so you " \
                    + "can't eliminate \nthat variable.\n" + \
                    "eliminationVariable:" + str(eliminationVariable) + "\n" +\
                    "unconditionedVariables: " + str(factor.unconditionedVariables()))

        "*** YOUR CODE HERE ***"
        sub_condition_list = []
        tem_set_unc = set([])
        tem_set_con = set([])
        final_dic = {}
        tem_set_unc |= factor.unconditionedVariables()
        tem_set_con |= factor.conditionedVariables()
        sub_condition_list.append(factor.conditionedVariables())
        uncondition = list(tem_set_unc-set([eliminationVariable]))
        condition = list(tem_set_con - (tem_set_con & set(uncondition)))
        ElminatedFactor = Factor(uncondition, condition, factor.variableDomainsDict())
        for new_dic in ElminatedFactor.getAllPossibleAssignmentDicts():
            prob=0
            for eliminate_domian in factor.variableDomainsDict()[eliminationVariable]:
                extra_dic={eliminationVariable:eliminate_domian}
                input_dic=new_dic.copy()
                #print(extra_dic)
                #print (new_dic)
                input_dic.update(extra_dic)
                #print input_dic
                prob+=factor.getProbability(input_dic)
            ElminatedFactor.setProbability(new_dic,prob)
        return ElminatedFactor
    return eliminate

eliminate = eliminateWithCallTracking()


def normalize(factor):
    """
    Question 5: Your normalize implementation 

    Input factor is a single factor.

    The set of conditioned variables for the normalized factor consists 
    of the input factor's conditioned variables as well as any of the 
    input factor's unconditioned variables with exactly one entry in their 
    domain.  Since there is only one entry in that variable's domain, we 
    can either assume it was assigned as evidence to have only one variable 
    in its domain, or it only had one entry in its domain to begin with.
    This blurs the distinction between evidence assignments and variables 
    with single value domains, but that is alright since we have to assign 
    variables that only have one value in their domain to that single value.

    Return a new factor where the sum of the all the probabilities in the table is 1.
    This should be a new factor, not a modification of this factor in place.

    If the sum of probabilities in the input factor is 0,
    you should return None.

    This is intended to be used at the end of a probabilistic inference query.
    Because of this, all variables that have more than one element in their 
    domain are assumed to be unconditioned.
    There are more general implementations of normalize, but we will only 
    implement this version.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """

    # typecheck portion
    variableDomainsDict = factor.variableDomainsDict()
    for conditionedVariable in factor.conditionedVariables():
        if len(variableDomainsDict[conditionedVariable]) > 1:
            print ("Factor failed normalize typecheck: ", factor)
            raise ValueError ("The factor to be normalized must have only one " + \
                            "assignment of the \n" + "conditional variables, " + \
                            "so that total probability will sum to 1\n" + 
                            str(factor))

    "*** YOUR CODE HERE ***"
    # print (factor)
    tem_set_con = []
    x=set([])
    # print factor.variableDomainsDict()
    for k in factor.variableDomainsDict().keys():
        if(len(factor.variableDomainsDict()[k])==1):
            if(k not in (factor.unconditionedVariables() or factor.conditionedVariables())):
                #print k+'   no con/inc var'
                pass
            else:
                #print k not in (factor.unconditionedVariables() or factor.conditionedVariables())
                #print k
                tem_set_con.append(k)
        else:pass
    #print factor.unconditionedVariables()
    #print factor.conditionedVariables()
    #print tem_set_con
    #print factor.variableDomainsDict()
    tem_set_con+=list(factor.conditionedVariables())
    #print tem_set_con
    tem_set_unc=[i for i in factor.unconditionedVariables() if i not in tem_set_con]
    sum_prob=0
    # print set(tem_set_con)
    # print x
    # print tem_set_con_1
    # print tem_set_unc
    #print factor.conditionedVariables()
    #print factor.unconditionedVariables()
    #print factor.variableDomainsDict()
    NormalizedFactor = Factor(tem_set_unc,tem_set_con,factor.variableDomainsDict())
    for sum_dic in factor.getAllPossibleAssignmentDicts():
        sig_prob=factor.getProbability(sum_dic)
        sum_prob+=sig_prob

    for sum_dic_2 in factor.getAllPossibleAssignmentDicts():
        NormalizedFactor.setProbability(sum_dic_2, factor.getProbability(sum_dic_2) / sum_prob)
    return NormalizedFactor
    #util.raiseNotDefined()

