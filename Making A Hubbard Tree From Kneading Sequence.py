#TO USE THIS SIMPlY WRITE THE TAU KNEADING SEQUENCE YOU WANT TO INVESTIGATE IN LINE 272. Make sure to put parenthese around the part that is perioidic.


from collections import Counter
import random
import matplotlib.pyplot as plt
import math
import pylab as pl
import networkx as nx
import copy

def shift(sequence):
    listOfSequence = list(sequence)
    firstDigit = listOfSequence[0]
    listOfSequence.remove(firstDigit)
    listOfSequence.append(firstDigit)
    return(''.join(listOfSequence))

def vote(a,b,c, tau):
    firstDigits = [a[0], b[0], c[0]]
    data = Counter(firstDigits)
    mostCommon = data.most_common(1)

    #the next line says "if the most common first character appears once (i.e they all appear once) then just print T. This way we just know it's tau"
    if(mostCommon[0][1] == 1):
        nextChar = tau
    else:
        nextChar = mostCommon[0][0]
        if(a[0] == nextChar):
            a =shift(a)
        else:
            a=shift(tau)

        if(b[0] == nextChar):

            b = shift(b)
        else:
            b=shift(tau)

        if(c[0] == nextChar):
            c = shift(c)
        else:
            c=shift(tau)
    return(nextChar, a, b, c)

def votingSequence(a,b,c, tau):
    sequence = ""
    n= 0
    while(n<len(tau)):
        nextChar, a, b, c = vote(a,b,c, tau)
        sequence = sequence+nextChar
        if(nextChar == tau):
            return sequence
        n+=1

    return sequence

def nonPeriodicShift(sequence):
    sequence = sequence[1:]
    return(sequence)

def MakeTree(tau, intAdd):
    ogTau=tau
    n=3*len(tau) #you can change this number to make the itinerary of points longer


    endPoints=[]
    tauIsPeriodic = False

    indexOfParen = tau.index(")")
    tau = expand(tau, n)
    m=len(ogTau)-2
    endPoints = [tau[:m]]
    for k in range(0, indexOfParen):
        tau = nonPeriodicShift(tau)
        shortenedTau = tau[:m]
        if(shortenedTau not in endPoints):
            endPoints.append(shortenedTau)


    tau=endPoints[0]
    count = 0
    branchPoints=endPoints[:]
    branchPointCoordinates = []

    count = 0


    count = 0
    for i in range(0, len(branchPoints)-2):
        for j in range(i+1, len(branchPoints)-1):
            for k in range(j+1, len(branchPoints)):
                delta = votingSequence(branchPoints[i], branchPoints[j], branchPoints[k], tau)
                if(tauIsPeriodic):
                    delta = delta[:len(tau)]
                else:
                    delta = delta[:m]




                if delta not in branchPoints:
                    branchPoints.append(delta)





    listOfSimpleArcs = calculateSimpleArcs(branchPoints, tau, m)
    for k in range(0, len(branchPoints)):
    	print("{} = {}".format(k, branchPoints[k]))

    G= nx.Graph()
    if len(listOfSimpleArcs)==0:
        print("No simple arcs I guess")
    for k in range(len(listOfSimpleArcs)):
    	G.add_edge(listOfSimpleArcs[k][0], listOfSimpleArcs[k][1])

    """
        You can uncomment the enxt line if you want to see the tree in its most
        simplified form. i.e. only endpoints and branch points are labeled
    """
    #G=removeInteriorPoints(G)
    plt.subplot(111)
    nx.draw_planar(G, with_labels=True, font_weight='bold')
    plt.draw()
    plt.title("tau={} \n".format(ogTau, intAdd))    #If you want the internal address use plt.title("tau={} \n{}".format(ogTau, intAdd))
    plt.show()
    return(G)







def removeInteriorPoints(G):
    """
    This function removes points that are not branch points, endpoints, or the critical point
    """
    nodeList = list(G)
    for i in range(len(nodeList)):
        if(G.degree[nodeList[i]]==2 and i>0):
            neighborNodes = list(G.neighbors(nodeList[i]))
            G.remove_node(nodeList[i])
            i-=1
            G.add_edge(neighborNodes[0], neighborNodes[1])
    return(G)




def calculateSimpleArcs(branchPoints, tau, m):
    simpleArcs=[]
    for i in range(0, len(branchPoints)-1):
        for j in range(i+1, len(branchPoints)):
            for k in range(0, len(branchPoints)):
                if((branchPoints[k] == branchPoints[i] or branchPoints[k]==branchPoints[j]) and j!=len(branchPoints)-1):
                    continue
                else:
                    otherTry = votingSequence(branchPoints[i], branchPoints[j], branchPoints[k], tau)
                    otherTry = otherTry[:m]
                    if(not(otherTry == branchPoints[i] or otherTry == branchPoints[j])):
                        break
                    else:
                        if (k==len(branchPoints)-1):
                            simpleArcs.append([i,j])
    return(simpleArcs)


def expand(tau, n):
    indexOfParen = tau.index("(")
    tau = tau.replace("(", "")
    tau = tau.replace(")","")
    repeatedPart=tau[indexOfParen:]
    while (len(tau) < 2*n):
        tau = tau+repeatedPart
    return tau


def isItValid(tau):
    """
    Recall that a kneading sequence is admissable iff for every shift, \sigma^j,
    there is an index k such that 0\neq \tau_k \neq \sigma^j(\tau)_k \neq 0
    So in this function we compare the various shifts of tau to make sure each
    is admissable
    """
    tau=tau.replace("(","")
    tau=tau.replace(")","")
    print(tau)
    shiftyBoy = tau #shiftyboy is the thing which will be shifted and compared to tau
    for n in range(len(tau)-1):
        shiftyBoy = shift(shiftyBoy)
        notAdmiss=True
        for j in range(0, len(tau)):
            if((shiftyBoy[j]!=tau[j]) and (shiftyBoy[j]!="0") and (tau[j]!="0")):
                notAdmiss = False
                continue
        if(notAdmiss):
            return False
    return True

def makeIntAdd(tau):
    intAdd=[1]
    nextNum = 1
    for i in range(len(tau)):
        nextNum = rho(nextNum, tau)

        if(nextNum != "infty"):
            intAdd.append(nextNum)
        else:
            return intAdd


def expandBruin(tau,n):
    while (len(tau) < 2*n):
        tau = tau+tau
    return tau


def rho(m, tau):
    for k in range(m, len(tau)-1):
        if(tau[k]!= tau[k-m]):
            return k+1
    return "infty"


def convertTauToBruin(tau):
    """
    Inthe literature it is common to say that the itinerary of the image
    of the critical point is the kneading sequence rather than the itinerary
    of the critical point itself.
    """
    if(tau[0]=="("):
        tau=tau.replace("0","")
        tau=tau.replace(")","")
        tau=tau.replace("(","")

        tau=tau+"0"
        tau=expandBruin(tau, 100)

    else:
        tau=expand(tau, 100)
        tau=tau.replace("0","")
        tau=tau.replace(")","")
        tau=tau.replace("(","")


    return tau



def opposite(oneOrTwo):
    if(oneOrTwo == "1"):
        return("2")
    else:
        return("1")


def listToString(list):
    str1 = " "
    return (str1.join(list))


def main():
    """




    AIGHT DUDES CHANGE THE TAU IN THE FOLLOWING LINE
    Type the kneading sequence in question as a string below tau="".
    Surround the part of the kneading sequence that is periodic with parenthese ()




    """
    tau = "(0112112)"

    #All preperiodic kneading sequence are valid (i.e. admissable).
    #So it suffices to verify just the periodic sequences
    if(tau[0]=="("):
        itIsValid = isItValid(tau)
    else:
        itIsValid = True


    if(itIsValid):
        print("This is a valid kneading sequence! Building the tree now.")
        diffTau=convertTauToBruin(tau)
        intAdd = makeIntAdd(diffTau)
        print(intAdd)
        tree1 = MakeTree(tau, intAdd)
    else:
        print("This is an invalid internal address, but let's run this bitch")
        diffTau=convertTauToBruin(tau)
        intAdd = makeIntAdd(diffTau)
        print(intAdd)
        tree1 = MakeTree(tau, intAdd)







if __name__== "__main__":
  main()
