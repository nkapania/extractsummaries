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
from scipy.stats import chi2

class HiddenMarkovModel(object):
    def __init__(self, numStates, numFeatures):
        self.M = np.zeros((numStates, numStates))
        self.B = MultivariableNormals(numStates, numFeatures) #initialize collection of multivariable functions
        self.p=  np.zeros((1, numStates))
        self.numStates = numStates
        self.numFeatures = numFeatures

    def incrementP(self, state):
        self.p[0][state] += 1

    def incrementM(self, state, newState):
        self.M[state][newState] += 1

    def normalize(self):
        self.B.normalizeSigma()
        norm(self.M)
        norm(self.p)

    #given a hidden markov model and YelpReview object, summarize it in k sentences 
    def summarize(self, review, k, verbose = 0):
        D = FeatureSimilarityMatrices(self, review)
        T = len(review.sentences)
        w = sum( self.getAlpha(T-1, D) )

        gamma = []
        for t in range(T):
            score = 0.0
            alpha = self.getAlpha(t, D)
            beta =  self.getBeta(t, D)
            for state in range(self.numStates):
                if (state % 2): #odd -> summary state of HMM
                    score -= float(alpha[state])*float(beta[state])/float(w)
            gamma.append(score)

        bestIndices = np.array(gamma).argsort()

        indices = sorted(bestIndices[:k])
        for ind in indices: print review.sentences[ind].text
        return indices

    #recursively compute alpha score    
    def getAlpha(self, t, D):
        #if t == 0: return np.asmatrix(self.p).T
        if t == 0: return np.asmatrix(self.p).T
        else:
            return D.get(t) * np.asmatrix(self.M).T * self.getAlpha(t-1, D)

    #recursively compute beta score
    def getBeta(self, t, D):
        if t == D.len()-1: return np.ones( (self.numStates, 1) )
        else:
            return np.asmatrix(self.M) * D.get(t+1) * self.getBeta(t+1, D)

    
class MultivariableNormals(object):
    def __init__(self, numStates, numFeatures):
        self.mu = []
        self.sigma = np.asmatrix(np.zeros( (numFeatures, 1) ) )
        self.counts = []
        self.numStates = numStates
        self.numFeatures = numFeatures
        for i in range(numStates):
            self.counts.append(0)
            self.mu.append(np.asmatrix(np.zeros( (numFeatures, 1) ) ) )

    def updateMu(self, state, phi):
        phiM = np.asmatrix(phi).T
        self.mu[state] = (self.mu[state]*self.counts[state] + phiM)/(self.counts[state] + 1)
        self.counts[state] += 1

    def updateSigma(self, state, phi):
        temp = np.asmatrix(phi).T - self.mu[state]
        cov = temp * temp.T
        self.sigma = self.sigma + cov

    def normalizeSigma(self):
        self.sigma = self.sigma / sum(self.counts)

    def printResults(self):
        print "Sigma: "
        print self.sigma
        for state in range( self.numStates ):
            print "State %d : Counts %d" % (state, self.counts[state])
            print "Feature Mu: "
            print self.mu[state]
            print ""

class FeatureSimilarityMatrices(object):
    def __init__(self, hmm, review):
        self.D = []
        Sinv = np.linalg.inv(hmm.B.sigma)
        
        for sentence in review.sentences:
            D_o = np.asmatrix(np.zeros( (hmm.numStates, hmm.numStates) ) )
            dof = hmm.numFeatures
            for state in range(hmm.numStates):
                phiM = np.asmatrix(sentence.phi).T
                arg = phiM - hmm.B.mu[state]
                D_o[state,state] = 1 - chi2.cdf(arg.T*Sinv*arg, dof)

            self.D.append(D_o)

    def len(self):
        return len(self.D)

    def get(self, sentence):
        return self.D[sentence]

    def printResults(self):
        print "Object Contains %d Matrices" % len(self.D)
        for i in range(len(self.D)):
            print self.D[i]
            print ""
                            

#come up with state transition matrix from labeled data, as well
#as p distribution of initial sentences, output in a tuple of (M, p)

#M is a (2N + 1) x (2N + 1) Markov transition matrix, where N is number of summary sentences in HMM
#model, p is a (2*N + 1) distribution.

def trainHMM(labeledReviews, naiveBayesModel, N = 6, numFeatures = 5):

    #get number of states from number of summary sentences N
    numStates = 2 if N == 1 else 2*N+1 #N = 1 is special case - simple two state model

    #initialize hidden markov model                 
    hmm = HiddenMarkovModel(numStates, numFeatures)
    
    #load reviews    
    reviews = utils.loadLabeledReviews(labeledReviews)

    #first pass - transition matrix M, probability distribution p, feature means.
    for reviewID in reviews.keys():
        print "Processing Review: %s" % reviewID
        
        review = utils.getReview(reviewID, naiveBayesModel)

        numSentences = len(review.sentences)
        try: numSummarySentences = len(reviews[reviewID])
        except TypeError: continue
        
        isSummary = getSummaryFunc(reviews[reviewID])
        #get initial state and increment p array
        state = 1 if isSummary(0) else 0
        hmm.incrementP(state)

        for i in range(numSentences):
            hmm.B.updateMu(state, review.sentences[i].phi)
            if i < numSentences - 1:
                newState = getSucc(state, isSummary(i+1), N)
                hmm.incrementM(state, newState) 
                state = newState

    #second pass - feature covariance matrices
    for reviewID in reviews.keys():
        print "Processing Review (Pass 2): %s" % reviewID
        review = utils.getReview(reviewID, naiveBayesModel)
        
        numSentences = len(review.sentences)
        try: numSummarySentences = len(reviews[reviewID])
        except TypeError: continue
        
        isSummary = getSummaryFunc(reviews[reviewID])
        state = 1 if isSummary(0) else 0
        for i in range(numSentences):
            hmm.B.updateSigma(state, review.sentences[i].phi)
            if i < numSentences - 1:
                state = getSucc(state, isSummary(i+1), N)

    #normalize
    hmm.normalize()
    return hmm 
  

#get successor state given current state, whether next sentence is summary or not, and number of summary sentences
def getSucc(state, isSummary, N):

    if N == 1:  #special case - simple two state Markov Model
        return 1 if isSummary else 0
    
    
    if state == 2*N - 1:  #in last summary state
        return state+1 #only one transition according to conroy and o'leary paper, but this should be reconsidered

    if state == 2*N:  #last non-summary state
        return state-1 if isSummary else state

    if state % 2: return state + 2 if isSummary else state+1 #intermediate summary state
    else: return state + 1 if isSummary else state           #intermediate non-summary

def norm(A):
    numRows, numCols = A.shape
    for i in range(0, numRows): #iterate through each row
        if sum(A[i]) != 0:
            A[i] = A[i]/sum(A[i])
    return A

#create function to query whether a sentence is a summary sentence or not
def getSummaryFunc(summaryList):
    return lambda x: x in summaryList
