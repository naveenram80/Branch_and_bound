import copy
import math

def simplex(cost, constraints, basic, constants):
    zij = []
    cb = []
    for i in basic:
        cb.append(cost[i])
    for i in range(len(constraints[0])):
        zijVal = 0
        for j in range(len(constraints)):
            zijVal = zijVal + constraints[j][i] * cb[j]
        zijVal = zijVal - cost[i]
        zij.append(zijVal)
   
    negativeFlag = 0
    for i in zij:
        if i < 0:
            negativeFlag = 1
            break

    if negativeFlag == 0:
        return constants, basic, cb

    entering = min(zij)
    enteringVar = zij.index(entering)
 

    ratio = []
    for i in range(len(constraints)):
        if constraints[i][enteringVar] !=0:
            ratio.append(constants[i] / constraints[i][enteringVar])
        else:
            ratio.append(99999999999)
       
    leaving = min(ratio)
   
    leavingVar = 0
    for i in range(len(ratio)):
        if ratio[i] == leaving:
            leavingVar = i

 
   
    basic[leavingVar] = enteringVar

    pivot = constraints[leavingVar][enteringVar]
    for i in range(len(constraints[0])):
        constraints[leavingVar][i] /= pivot
    constants[leavingVar] /= pivot
       
    for i in range(len(constraints)):
        if i != leavingVar:
            multiply = constraints[i][enteringVar]
            for j in range(len(constraints[0])):
                constraints[i][j] = constraints[i][j] - constraints[leavingVar][j] * multiply
            constants[i] -= constants[leavingVar] * multiply
    cons, bas, cb = simplex(cost, constraints, basic, constants)
    return cons, bas ,cb

def branchAndBound(objFuncCoeff, constraints, basicVar, constants, z, c):
   
    twoPhaseConstraintsBB=copy.deepcopy(constraints)
    twoPhaseConstantsBB = copy.deepcopy(constants)
    twoPhaseObjFuncCoeffBB = copy.deepcopy(objFuncCoeff)
    twoPhaseBasicBB = copy.deepcopy(basicVar)


    subBBLeftConstraints = copy.deepcopy(constraints)
    subBBLeftConstants = copy.deepcopy(constants)
    subBBLeftObjFuncCoeff = copy.deepcopy(objFuncCoeff)
    subBBLeftBasic = copy.deepcopy(basicVar)

    subBBRightConstraints = copy.deepcopy(constraints)
    subBBRightConstants = copy.deepcopy(constants)
    subBBRightObjFuncCoeff = copy.deepcopy(objFuncCoeff)
    subBBRightBasic = copy.deepcopy(basicVar)
   

    toSplit = 0
    prevFrac = 2
    for i in range(len(c)):

        frac, whole = math.modf(c[i])
       
        if prevFrac > frac:
            prevFrac = frac
            toSplit = c[i]
            splitVar = twoPhaseBasicBB[i]
    ub=  math.ceil(toSplit)
    lb = math.floor(toSplit)
    newConstraint = []

    for i in constraints:
        i.append(0)
    for i in range(len(constraints[0])):
        if i == splitVar or i == len(constraints[0])-1:
            newConstraint.append(1)
        else:
            newConstraint.append(0)
    constraints.append(newConstraint)

    objFuncCoeff.append(0)
    basicVarBB = []
    for i in range(noOfVariables, len(constraints[0])):
        basicVarBB.append(i)
    constants.append(lb)
   
    c1, b1, cb1 = simplex(objFuncCoeff, constraints, basicVarBB, constants)
   

    z = 0
    for i in range(len(c1)):
        z += c1[i] * cb1[i]
    print("Max z = ",z)




   
    artificialBB = []
    for i in range(len(twoPhaseConstraintsBB[0])+1):
        artificialBB.append(0)
    artificialBB.append(-1)

    for i in twoPhaseConstraintsBB:
        i.append(0)
        i.append(0)

    newConstraint = []
    for i in range(len(twoPhaseConstraintsBB[0])):
        if i == splitVar or i == len(twoPhaseConstraintsBB[0])-1:
            newConstraint.append(1)
        elif i == len(twoPhaseConstraintsBB[0])-2:
            newConstraint.append(-1)
        else:
            newConstraint.append(0)
    twoPhaseConstraintsBB.append(newConstraint)

    basicVarBB2 = []
    for i in range(noOfVariables, len(twoPhaseConstraintsBB[0])):
        if i != len(twoPhaseConstraintsBB[0])-2:
            basicVarBB2.append(i)
    twoPhaseConstantsBB.append(ub)
    twoPhaseConstantsBBPhase2, basicVarBB2Phase2, cb = simplex(artificialBB, twoPhaseConstraintsBB, basicVarBB2, twoPhaseConstantsBB)
    for i in twoPhaseConstraintsBB:
        del i[len(twoPhaseConstraintsBB[0])-1]


    c2, b2, cb2 = simplex(twoPhaseObjFuncCoeffBB, twoPhaseConstraintsBB, basicVarBB2Phase2, twoPhaseConstantsBBPhase2)
 
    z = 0
    for i in range(len(c1)):
        z += c2[i] * cb2[i]
    print("Max z = ",z)

   
    branchAndBound(subBBLeftObjFuncCoeff, subBBLeftConstraints, subBBLeftBasic, subBBLeftConstants, z, c1[:2])    

    branchAndBound(subBBRightObjFuncCoeff, subBBRightConstraints, subBBRightBasic, subBBRightConstants, z, c2[:2])    





noOfVariables = int(input("Enter the no. of variables   :"))
noOfConstraints = int(input("Enter the no. of constraints :"))

typeOfObj = int(input("\n\t1.Maximization type\n\t2.Minimization type\n\nENTER THE TYPE OF THE OBJECTIVE FUNCTION :"))
objFuncCoeff = []
print("\n\nEnter the coefficient of variables in objective function :")
for i in range(noOfVariables):
    objFuncCoeff.append(int(input("Enter the coefficient of x" + str(i+1) + " :")))

constraints = []
constants = []
originalConstraints = []
originalConstants =[]
constraintTypes = []
originalObjFuncCoeff = []
twoPhaseCost = []
twoPhaseFlag = 0
countOfArtificialVariable = 0

for i in range(noOfConstraints):
    print("\n\n\nEnter the coefficients of the variables in constraint " + str(i+1) + " :")
    constraintCoeff = []
    for j in range(noOfVariables):
        constraintCoeff.append(int(input("Enter the coefficient of x" + str(j+1) + " :")))
        if j == noOfVariables-1 :
            for k in range(0,i+countOfArtificialVariable):
                constraintCoeff.append(0)
            constraintType = int(input("\n\t1. <= type\n\t2. >= type\n\nEnter the type of constraint :"))
            constraintTypes.append(constraintType)
            if constraintType == 1:
                constraintCoeff.append(1)
            if constraintType == 2:
                constraintCoeff.append(-1)
                constraintCoeff.append(1)
                countOfArtificialVariable += 1
                twoPhaseFlag = 1
            const = int(input("Enter the constant term :"))
            constants.append(const)
    constraints.append(constraintCoeff)
   
print("\n\nENTERED LINEAR PROGRAMMING PROBLEM :\n")
if typeOfObj == 1:
    print("Objective function :\nmax Z = ", end = "")
elif typeOfObj == 2:
    for i in range(len(objFuncCoeff)):
        objFuncCoeff[i] *= -1
    print("Objective function :\nmin Z = ", end = "")
for i in range(noOfVariables):
    if i != noOfVariables-1:
        print(str(objFuncCoeff[i]) + "x" + str(i+1) + " + ", end = "")
    else:
        print(str(objFuncCoeff[i]) + "x" + str(i+1), end="")
       
print("\n\nConstraints :")
for i in range(noOfConstraints):
    for j in range(noOfVariables):
        if j != noOfVariables-1:
            print(str(constraints[i][j]) + "x" + str(j+1) + " + ", end = "")
        else:
            print(str(constraints[i][j]) + "x" + str(j+1), end = "")
    if constraintTypes[i] == 1:
        print(" <= ",end = "")
    elif constraintTypes[i] == 2:
        print(" >= ",end = "")
    print(constants[i])
print("\n\n")
l = len(constraints[noOfConstraints-1])
for i in range(noOfConstraints):
    for j in range(len(constraints[i]),l):
        constraints[i].append(0)  

originalConstraints=copy.deepcopy(constraints)
originalConstants=copy.deepcopy(constants)
originalObjFuncCoeff=copy.deepcopy(objFuncCoeff)



if twoPhaseFlag == 0:
    simplexConstraints=copy.deepcopy(constraints)
    simplexConstants=copy.deepcopy(constants)
    simplexObjFuncCoeff=copy.deepcopy(objFuncCoeff)
    #print("inside if",simplexConstants, simplexConstraints, simplexObjFuncCoeff)
    basicVar = []
    for i in range(noOfVariables, len(simplexConstraints[0])):  
        basicVar.append(i)
    for i in range(len(simplexObjFuncCoeff),l+1):
        simplexObjFuncCoeff.append(0)
    returnedConstants, returnedBasic, returnedCb =simplex(simplexObjFuncCoeff, simplexConstraints, basicVar, simplexConstants)
    print(returnedConstants, returnedBasic, returnedCb)
    z = 0
    for i in range(len(returnedConstants)):
        z += returnedConstants[i] * returnedCb[i]
    print(z)


    nonInt = 0
    for i in returnedConstants:
        if i != int(i):
            nonInt = 1
            break
    simplexBBConstraints=copy.deepcopy(constraints)
    simplexBBConstants=copy.deepcopy(constants)
    simplexBBObjFuncCoeff=copy.deepcopy(objFuncCoeff)

    if nonInt == 1:
        #print("normal bb",simplexBBConstraints)
        branchAndBound(simplexObjFuncCoeff, simplexBBConstraints, basicVar, simplexBBConstants, z, returnedConstants)
        print("max z = ",z)
    else:
        print("All Integer solution for the entered objective function :",returnedConstants)
        print("max z = ",z)



elif twoPhaseFlag == 1:

    twoPhaseSimplexConstraints=copy.deepcopy(constraints)
    twoPhaseSimplexConstants=copy.deepcopy(constants)
    twoPhaseSimplexObjFuncCoeff=copy.deepcopy(objFuncCoeff)

    phaseOneCoeff = []
    phaseOneBasic = []
    for i in range(len(twoPhaseSimplexConstraints[0])):
        if i < noOfVariables:
            phaseOneCoeff.append(0)
        else:
            for j in range(noOfConstraints):
                One = 0
                if constraints[j][i] == 1:
                    phaseOneCoeff.append(-1)
                    phaseOneBasic.append(i)
                    One = 1
                    break
            if One == 0:
                phaseOneCoeff.append(0)

    phaseTwoConstants, phaseTwoBasic, returnedCb = simplex(phaseOneCoeff, twoPhaseSimplexConstraints, phaseOneBasic, twoPhaseSimplexConstants)

    phCount = 0
    for i in range(0, len(phaseOneCoeff)):
        if phaseOneCoeff[i] == -1:
            for j in twoPhaseSimplexConstraints:
                del j[i-phCount]
            phCount += 1

    for i in range(noOfVariables, len(twoPhaseSimplexConstraints[0])):
        twoPhaseSimplexObjFuncCoeff.append(0)

    returnedConstants, returnedBasic, returnedCb = simplex(twoPhaseSimplexObjFuncCoeff, twoPhaseSimplexConstraints, phaseTwoBasic, phaseTwoConstants)

    z=0
    for i in range(len(returnedConstants)):
        z += returnedConstants[i] * returnedCb[i]
    print(z*-1)

    nonInt = 0
    for i in returnedConstants:
        if i != int(i):
            nonInt = 1
            break

    simplex2BBConstraints=copy.deepcopy(constraints)
    simplex2BBConstants=copy.deepcopy(constants)
    simplex2BBObjFuncCoeff=copy.deepcopy(objFuncCoeff)

    if nonInt == 1:
        print("dual bb")
        branchAndBound(twoPhaseSimplexObjFuncCoeff, simplex2BBConstraints, phaseTwoBasic, simplex2BBConstants, z, returnedConstants)    
    else:
        print("All Integer solution for the entered objective function :",returnedConstants)
        print("max z = ",z)