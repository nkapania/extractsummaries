import collections
import hmm
import json
import pickle
import utils
import YelpReview
import utils
import naiveBayes


HMM_MODEL_FILE = "hmm_model"
NB_MODEL_FILE = "nb_model"

def saveModel(corpusJSON, N, numFeatures, nb):
    model = hmm.trainHMM(corpusJSON, nb, N, numFeatures)
    with open(HMM_MODEL_FILE, 'wb') as output:
        pickle.dump(model, output, pickle.HIGHEST_PROTOCOL)
       
def loadModel():
    with open(HMM_MODEL_FILE, 'rb') as input:
        hmmModel = pickle.load(input)
    return hmmModel

def filterReviews(reviewJSON):
    reviews = utils.loadLabeledReviews(reviewJSON)
    outputDict = {}
    for key, value in reviews.items():
        if key not in outputDict:
            try:
                len(value)
                outputDict[key] = value
            except TypeError:
                print key, value
                continue

    output = open("output.json", 'w')
    json.dump(outputDict, output, indent=2)
    output.close()

def removeFirstElement(reviewJSON):
    reviews = utils.loadLabeledReviews(reviewJSON)
    outputDict = {}
    for key, value in reviews.items():
        if key not in outputDict: outputDict[key] = value[1:]

    output = open("output.json", 'w')
    json.dump(outputDict, output, indent=2)
    output.close()

"""
For each summary sentence in the dataset of labeled reviews, build a corpus of terms.
"""
def createSummarySentenceTermCorpus():
    corpus = collections.Counter()
    reviews = utils.loadLabeledReviews("Labeled_Reviews_All.json")
    for key, value in reviews.items():
        review = utils.getReview(key)
        for ind in value:
            s = review.sentences[ind]
            for term in utils.processSentenceText(s.text):
                corpus[term] += 1

    handle = open("corpus_ss.json", 'w')
    json.dump(corpus, handle, indent=2)
    handle.close()

def calculateF1(tp, fp, tn):
    precision = tp/(tp + fp)
    recall = tp/(tp + fn)
    F1 = 2 * precision * recall / (precision + recall)
    return F1

#filterReviews("Labeled_Reviews_All.json")
#removeFirstElement("Labeled_Reviews_Sean.json")
createSummarySentenceTermCorpus()

#utils.createRestaurantCorpus()
#createSummarySentenceTermCorpus()
naiveBayes.saveNB("Labeled_Reviews_All.json", NB_MODEL_FILE)
naiveBayesModel = naiveBayes.loadNB(NB_MODEL_FILE)
saveModel("Labeled_Reviews_All.json", 3, 5, naiveBayesModel )
model = loadModel()
#print model.M
#print model.p
#model.B.printResults()


print model.M
print model.p
model.B.printResults()
reviews = utils.loadLabeledReviews("Labeled_Reviews_1158-1200.json")

count = 0
TP = 0.0
FP = 0.0
FN = 0.0

for key, value in reviews.items():
    r = utils.getReview(key, naiveBayesModel)
    "value", value
    try:
        predicted = model.summarize(r, len(value))
        print key, predicted
        print "Labeled indices", value
        tp = 0.0
        fp = 0.0
        fn = 0.0
        for i in predicted:
            if i in value: tp += 1
            else: fp += 1
        for i in value:
            if i not in predicted: fn += 1
        TP += tp
        FP += fp
        FN += fn
        print "tp: %d. fp: %d, fn: %d" % (tp, fp, fn)
        print "TP: %d. FP: %d, FN: %d" % (TP, FP, FN)

        
    except ZeroDivisionError:
        print "ZeroDivisionError Encountered with review ", key, "\n"
        count += 1
        continue

print count
used = len(reviews) - count
print used

print FP
print FN

P = TP/(TP + FP)
R = TP/(TP + FN)
print P, R
F1 = 2 * P * R / (P + R)
print "Total F1", F1

