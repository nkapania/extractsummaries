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
    def summarize(self, review, k):
        w = 0.0
        T = len(review.sentences)-1
        for state in range(self.numStates):
            w += getAlpha(self, T, state)

        gamma = []
        for t in range(T):
            score = 0.0
            for state in range(self.numStates):
                if (j % 2): #odd -> summary state of HMM 
                    score -= getAlpha(self, t, state, review)*getBeta(self, t, T, review)/w
            gamma.append[score]

        sentenceRankings = np.array[gamma]
        bestIndices = sentenceRankings.argsort()
        for i in range(k):
            print review.sentences[bestIndices[i]].text
            
            
    #obtain D_o matrix - need better intution about what this really does
    def getD_o(self, review, t):
        D_o = np.asmatrix(np.zeros(self.numStates, self.numStates))
        dof = self.numFeatures
        for state in range(numStates):
            phiM = np.asmatrix(review.sentences[t].phi).T
            arg = phiM -self.B.mu[state]
            D_o[state,state] = 1 - chi2.cdf(arg.T*numpy.linalg.inv(self.B.sigma[state])*arg, dof)
        return D_o

    #recursively compute alpha score    
    def getAlpha(self, t, state, review):
        if t == 0: return self.p[0][state]
        else:
            return getD_o(self, review, t)*np.asmatrix(self.M).T*getAlpha(self, t-1, state, review)

    #recursively compute beta score
    def getBeta(self, t, T, review):
        if t == T: return 1
        else:
            return np.asmatrix(self.M)*getD_o(self, review, t)*getBeta(self, t+1, T, review)

    
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

    def printResults(self):
        for state in range( len(self.counts) ):
            print "State %d : Counts %d" % (state, self.counts[state])
            print "Feature Mu: "
            print self.mu[state]
            print ""
            #print "Feature Sigma "
            #print self.sigma[state]
                

#come up with state transition matrix from labeled data, as well
#as p distribution of initial sentences, output in a tuple of (M, p)

#M is a (2N + 1) x (2N + 1) Markov transition matrix, where N is number of summary sentences in HMM
#model, p is a (2*N + 1) distribution.

def trainHMM(labeledReviews, N = 6, numFeatures = 4):

    #get number of states from number of summary sentences N
    numStates = 2*N+1

    #initialize hidden markov model                 
    hmm = HiddenMarkovModel(numStates, numFeatures)
    
    #load reviews    
    reviews = utils.loadLabeledReviews(labeledReviews)

    #first pass - transition matrix M, probability distribution p, feature means.
    for reviewID in reviews.keys():
        print "Processing Review: %s" % reviewID
        #numSentences = reviews[reviewID].pop(0) #legacy features - now we have YelpReview implemented so can remove this. Will required modifying labeled_reviews.json
        
        review = utils.getReview(reviewID)
        #assert numSentences == len(review.sentences)  # sanity check that labeled review is the same as the sentence in the review object

        numSentences = len(review.sentences)
        try: numSummarySentences = len(reviews[reviewID])
        except TypeError: continue
        
        isSummary = getSummaryFunc(reviews[reviewID])
        #get initial state and increment p array
        state = 1 if isSummary(0) else 0
        hmm.incrementP(state)

        for i in range(1, numSentences):
            hmm.B.updateMu(state, review.sentences[i].phi)
            newState = getSucc(state, isSummary(i), N)
            hmm.incrementM(state, newState) 
            state = newState

    #second pass - feature covariance matrices
    for reviewID in reviews.keys():
        print "Processing Review (Pass 2): %s" % reviewID
        review = utils.getReview(reviewID)
        
        numSentences = len(review.sentences)
        try: numSummarySentences = len(reviews[reviewID])
        except TypeError: continue
        
        isSummary = getSummaryFunc(reviews[reviewID])
        state = 1 if isSummary(0) else 0
        for i in range(1, len(review.sentences)):
            hmm.B.updateSigma(state, review.sentences[i].phi)
            state = getSucc(state, isSummary(i), N)

    #normalize
    hmm.normalize()
    return hmm 
  

#get successor state given current state, whether next sentence is summary or not, and number of summary sentences
def getSucc(state, isSummary, N):
    if state == 2*N - 1:  #in last summary state
        return state+1 #only one transition according to conroy and o'leary paper, but this should be reconsidered

    if state == 2*N:  #last non-summary state
        return state-1 if isSummary else state

    if state % 2: return state + 2 if isSummary else state+1 #intermediate summary state
    else: return state + 1 if isSummary else state           #intermediate non-summary

def norm(A):
    numRows, numCols = A.shape
    for i in range(0, numRows): #iterate through each row
        A[i] = A[i]/sum(A[i])
    return A

#create function to query whether a sentence is a summary sentence or not
def getSummaryFunc(summaryList):
    return lambda x: x in summaryList
    

markovModel = trainHMM("Labeled_Reviews_1100-1156.json", 3, 4)
print markovModel.M
print markovModel.p
markovModel.B.printResults()