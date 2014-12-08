#!/usr/bin/python

import json
import utils
import sys
import collections
import math
from sets import Set
from collections import Counter

def load(reviewJSON):
    reviewDict = utils.loadLabeledReviews(reviewJSON)
    reviewList = []
    for key, value in reviewDict.items():
        print "On Review", key
        YelpReview = utils.getReview(key)
        for i in range( len(YelpReview.sentences) ):
            if i in value:
                reviewList.append( (YelpReview.sentences[i].text, 1) )
            else:
                reviewList.append( (YelpReview.sentences[i].text, -1) )
    return reviewList
        
def loadStopWords(stopWordFilename):
    handle = open(stopWordFilename, 'r')
    stopWords = [line.strip() for line in handle.readlines()]
    handle.close()
    return stopWords

def extractWordFeatures(x):
    """
    Extract word features for a string x.
    @param string x: 
    @return dict: feature vector representation of x.
    Example: "I am what I am" --> {'I': 2, 'am': 2, 'what': 1}
    """
    phi = collections.Counter()
    words = x.split()
    stopWords = loadStopWords("stopWords.txt")
    
    for word in words:
        if word.lower() in stopWords:
            continue
        phi[word.lower()] = phi.get(word.lower(), 0) + 1
    return phi


def getListOfPhi(trainExamples, featureExtractor, desiredLabel):
    output = []
    for sentence, label in trainExamples:
        if label == desiredLabel:
            output.append(extractWordFeatures(sentence))
    return output

def getAllFeatures(posFeatures, negFeatures):
    featureSet = Set()
    for review in posFeatures:
        for key in review.keys():
            featureSet.add(key)
    for review in negFeatures:
        for key in review.keys():
            featureSet.add(key)
    return featureSet

def getNumWords(listOfPhi):
    counter = 0
    for item in listOfPhi:
        counter += len(item.keys())
    return counter

def getConditionals(listOfPhi, featureSet):
    den = getNumWords(listOfPhi) + len(featureSet)
    conditional = collections.Counter()
    
    for feature in featureSet:
        num = 1.0
        for review in listOfPhi:
            if feature in review: num += 1  
        conditional[feature] = num/den
    return conditional

def getPrior(posData, negData):
    return float( len(posData)) / ( len(posData) + len(negData))

def classify(testData, py, posConditionals, negConditionals, featureExtractor, featureSet):

    tp = 0
    fp = 0
    tn = 0
    fn = 0
    
    for review, trueLabel in testData:

        if trueLabel == -1: trueLabel = 0
        
        valPos = math.log(py)
        valNeg = math.log(1-py)
        reviewFeatures = featureExtractor(review)
        for feature in reviewFeatures.keys():
            if feature not in featureSet:
                posProb = 1.0
                negProb = 1.0
            else:
                posProb = posConditionals[feature]
                negProb = negConditionals[feature]

            counts = max(1, reviewFeatures[feature])
            valPos += counts * math.log( posProb )
            valNeg += counts * math.log( negProb )

        predictedLabel = 1 if valPos > valNeg else 0
        outcome = "CORRECT" if predictedLabel == trueLabel else "INCORRECT"
        if predictedLabel and trueLabel: tp += 1
        if predictedLabel and not  trueLabel: fp += 1
        if not predictedLabel and not trueLabel: tn += 1
        if not predictedLabel and trueLabel: fn += 1
    prec = float(tp)/(tp+fp)
    rec  = float(tp)/(tp+fn)
    F1 = 2*prec*rec/(prec+rec)
    print (tp, fp, tn, fn)
    print (prec, rec, F1)            
        
        #print "valPos = %d  valNeg = %d Prediction = %d Label = %d (%s)" %(valPos, valNeg, predictedLabel, trueLabel, outcome)
    

def extractCharacterFeatures(n):
    '''
    Return a function that takes a string |x| and returns a sparse feature
    vector consisting of all n-grams of |x| without spaces.
    EXAMPLE: (n = 3) "I like tacos" --> {'Ili': 1, 'lik': 1, 'ike': 1, ...
    '''
    def extract(x):
        xt = x.replace(" ","") #whitespaces trimmed
        phi = {}
        
        for i in range(0, len(xt)):
            key = xt[i:i+n]
            if len(key) == n: 
                phi[key] = phi.get(key, 0) + 1
        return phi
        
    return extract


    
    
    
    
            
            
        
        
        
                        
        
