##This code implements naive-bayes for summary extraction
#future work will account for dependencies via a HMM

#Nitin Kapania
#______________________________________________________________#




#until we get actual test data, lets fake some data and some features

#dict from reference ID's to labels - this will be loaded
#from Sean's library in the future

def getTrainData():
    trainData = {'a': 1, 'b': 1, 'c': 0, 'd': 0}
    return trainData


#primitive featurizer - will be loaded from Sean's library
#in future
def getFeatures(review):
    if trainData[review] == 1:
        return {'F1': 1, 'F2': 1}
    else:
        return {'F3': 1, 'F4': 1}


#return list of feauture dicts. User specifies whether list
#is made for all summary sentences in trainData (label = 1)
#or for non-summary sentences (label = 0).
#Dict feature is a map from feature name to feature value
def getListOfFeatures(trainData, label):
    featureList = []
    for review in trainData.keys():
        if trainData[review] == label:
            featureList.append(getFeatures(review))
    return featureList


trainData= getTrainData()
posFeatures = getListOfFeatures(trainData, 1)
negFeatures = getListOfFeatures(trainData, 0)

print posFeatures
print negFeatures
            
            
    

