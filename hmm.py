"""
#########################################################################
Created by: Nitin Kapania
Created date: 11/26/14
-------------------------------------------------------------------------
Library of methods for HMM, specific to yelp sentence extraction.
Requires numpy package to be installed. 
-------------------------------------------------------------------------
#########################################################################
"""

import utils
import numpy as np

#come up with state transition matrix from labeled data, as well
#as p distribution of initial sentences, output in a tuple of (M, p)

#M is a (2N + 1) x (2N + 1) Markov transition matrix, where N is number of summary sentences in HMM
#model, p is a (2*N + 1) distribution.

def getStateTransitions(N = 6):
    p = np.zeros((1, 2*N+1))
    M = np.zeros((2*N+1, 2*N+1))
    
    reviews = utils.loadLabeledReviews("Labeled_Reviews.json")
    for reviewID in reviews.keys():
        numSentences = reviews[reviewID].pop(0)
        isSummary = getSummaryFunc(reviews[reviewID])

        #get initial state and increment p array        
        state = 1 if isSummary(0) else 0
        p[0][state] += 1

        for i in range(1, numSentences):
            newState = getSucc(state, isSummary(i), N)
            M[state, newState] += 1
            state = newState

    return(normalize(M), normalize(p))    

#get successor state given current state, whether next sentence is summary or not, and number of summary sentences
def getSucc(state, isSummary, N):
    if state == 2*N - 1:  #in last summary state
        return state+1 #only one transition according to conroy and o'leary paper, but this should be reconsidered

    if state == 2*N:  #last non-summary state
        return state-1 if isSummary else state

    if state % 2: return state + 2 if isSummary else state+1 #intermediate summary state
    else: return state + 1 if isSummary else state           #intermediate non-summary

#create function to query whether a sentence is a summary sentence or not
def getSummaryFunc(summaryList):
    return lambda x: x in summaryList
    
#normalize transition matrix and initial distribution
#so every column sums to 1
def normalize(A):
    numRows, numCols = A.shape
    for i in range(0, numRows): #iterate through each row
        A[i] = A[i]/sum(A[i])
    return A