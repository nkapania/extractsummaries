"""
#########################################################################
Created by: Nitin Kapania
Created date: 11/12/14
Modified data: 11/13/14
-------------------------------------------------------------------------
Code that implements naive - bayes for Yelp sentence extraction.  
-------------------------------------------------------------------------
#########################################################################
"""

from sets import Set

def getReviews():
    reviewJSON = r"Labeled_Reviews.json"
    handle = open(reviewJSON, 'r')
    
    for line in handle:
        print line
        review = json.loads(line)
        print review
    return 0

#primitive featurizer - will be loaded from Sean's library
#in future
def getFeatures(review):
    if review == 'a' or review == 'b':
        return {'F1': 1, 'F2': 1}
    elif review == 'e':
        return {'F1':1}
    elif review == 'f':
        return {'F3':1}
    else:
        return {'F3': 1, 'F4': 1}

#return list of feauture dicts. User specifies whether list
#is made for all summary sentences in trainData (label = 1)
#or for non-summary sentences (label = 0).
#Dict feature is a map from feature name to feature value
def createTrainData(reviews, label):
    trainData = []
    for reviewID in reviews.keys():
        if reviews[reviewID] == label:
            trainData.append(getFeatures(reviewID))
    return trainData

def getFeatureSet(posFeatures, negFeatures):
    featureSet = Set()
    for review in posFeatures:
        for key in review.keys():
            featureSet.add(key)
    for review in negFeatures:
        for key in review.keys():
            featureSet.add(key)
    return featureSet

#really bad laplace smoothing right now - need to fix this
def getConditionals(trainData, featureSet):
    den = len(trainData)+1
    conditional = {}
    
    for feature in featureSet:
        num = 1.0
        for review in trainData:
            if feature in review: num += 1  
        conditional[feature] = num/den
    return conditional

def getPrior(posData, negData):
    return float(len(posData)) / (len(posData) + len(negData))

def classify(testData, py, posConditionals, negConditionals):
    valPos = math.log(py)
    valNeg = math.log(1-py)
    for feature in testData.keys():
        valPos += math.log( posConditionals[feature] )
        valNeg += math.log( negConditionals[feature] )

    return 1 if valPos > valNeg else 0
    

reviews = getReviews()
#reviews= getReviews()
#posData = createTrainData(reviews, 1)
#negData = createTrainData(reviews, 0)
#featureSet = getFeatureSet(posData, negData)
#posConditionals = getConditionals(posData, featureSet)
#negConditionals = getConditionals(negData, featureSet)
#py = getPrior(posData, negData)
#testData = getFeatures('f')


#print py
#print posData
#print negData
#print featureSet
#print posConditionals
#print negConditionals
#print classify(testData, py, posConditionals, negConditionals)
    

