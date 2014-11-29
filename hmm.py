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
import YelpReview
import numpy as np


class MultivariableNormals(object):
    def __init__(self, numStates, numFeatures):
        self.mu = []
        self.sigma = []
        self.counts = []
        for i in range(numStates):
            self.counts.append(0)
            self.mu.append(np.asmatrix(np.zeros( (numFeatures, 1) ) ) )
            self.sigma.append(np.asmatrix(np.zeros( (numFeatures, 1) ) ) )

    def updateMu(self, state, phi):
        phiM = np.asmatrix(phi).T
        self.mu[state] = (self.mu[state]*self.counts[state] + phiM)/(self.counts[state] + 1)
        self.counts[state] += 1

    def updateSigma(self, state, phi):
        temp = np.asmatrix(phi).T - self.mu[state]
        cov = temp * temp.T 
        self.sigma[state] = self.sigma[state] + cov

    def normalizeSigma(self):
        for state in range( len(self.counts) ):
            self.sigma[state] = self.sigma[state] / self.counts[state]
            

#come up with state transition matrix from labeled data, as well
#as p distribution of initial sentences, output in a tuple of (M, p)

#M is a (2N + 1) x (2N + 1) Markov transition matrix, where N is number of summary sentences in HMM
#model, p is a (2*N + 1) distribution.

def getMaxLikelihoodEstimates(N = 6, numFeatures = 4):

    #initialize estimates for parameters b, p, and M
    b = MultivariableNormals(N, numFeatures) #initialize collection of multivariable functions                   
    p = np.zeros((1, 2*N+1))
    M = np.zeros((2*N+1, 2*N+1))
    
    reviews = utils.loadLabeledReviews("Labeled_Reviews.json")

    #first pass - transition matrix M, probability distribution p, feature means.
    for reviewID in reviews.keys():
        numSentences = reviews[reviewID].pop(0)
        isSummary = getSummaryFunc(reviews[reviewID])
        review = utils.getReview(reviewID)
        assert numSentences == len(review.sentences)  # sanity check that labeled review is the same as the sentence in the review object

        #get initial state and increment p array        
        state = 1 if isSummary(0) else 0
        p[0][state] += 1

        for i in range(1, numSentences):
            b.updateMu(state, review.sentences[i].phi)
            newState = getSucc(state, isSummary(i), N)
            M[state, newState] += 1
            state = newState

    #second pass - feature covariance matrices
    for reviewID in reviews.keys():
        isSummary = getSummaryFunc(reviews[reviewID])
        review = utils.getReview(reviewID)

        state = 1 if isSummary(0) else 0
        for i in range(1, len(review.sentences)):
            b.updateSigma(state, review.sentences[i].phi)
            state = getSucc(state, isSummary(i), N)

    #normalize 
    p = normalize(p)
    M = normalize(M)
    b.normalizeSigma()
        
    return(M, p, b) 
  

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

M, p, b = getMaxLikelihoodEstimates(3)
print M
print p