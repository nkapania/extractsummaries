import collections
import hmm
import json
import pickle
import utils
import YelpReview
import utils


YelpHMM = hmm.trainHMM("Labeled_Reviews_1000-1090.json", N = 2, numFeatures = 3)
print YelpHMM.M
print YelpHMM.p
YelpHMM.B.printResults()

TestReview = utils.getReview("htx37hVCEdIQf03QfnL77w")
YelpHMM.summarize(TestReview, 4)
=======

#YelpHMM = hmm.trainHMM("Labeled_Reviews_1000-1090.json", N = 2, numFeatures = 3)
"""
reviews = utils.loadLabeledReviews("Labeled_Reviews.json")

outputDict = {}
for key, value in reviews.items():
    if key not in outputDict:
        try:
            outputDict[key] = value[1:]
        except TypeError: continue

output = open("output.json", 'w')
json.dump(outputDict, output, indent=2)
output.close()
"""

HMM_MODEL_FILE = "hmm_model"

def saveModel(corpusJSON, N, numFeatures):
    model = hmm.trainHMM(corpusJSON, N, numFeatures)
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

    print corpus


def calculateF1(tp, fp, tn):
    precision = tp/(tp + fp)
    recall = tp/(tp + fn)
    F1 = 2 * precision * recall / (precision + recall)
    return F1



#filterReviews("Labeled_Reviews_All.json")
saveModel("Labeled_Reviews_200-400.json", 3, 3)
model = loadModel()
#print model.M
#print model.p
#model.B.printResults()
reviews = utils.loadLabeledReviews("Labeled_Reviews_200-400.json")

"""
r = utils.getReview("EaXxcrGtsNRHHBgBHSYuZg")
gold = reviews["EaXxcrGtsNRHHBgBHSYuZg"]
predicted = model.summarize(r, len(gold))
print predicted
print "Labeled indices", gold
tp = 0.0
fp = 0.0
fn = 0.0
for i in predicted:
    if i in gold: tp += 1
    else: fp += 1
for i in gold:
    if i not in predicted: fn += 1
print "tp: %d. fp: %d, fn: %d" % (tp, fp, fn)
print calculateF1(tp, fp, fn)
"""

count = 0
totalF1 = 0
for key, value in reviews.items():
    r = utils.getReview(key)
    "value", value
    try:
        predicted = model.summarize(r, len(value))
        print predicted
        print "Labeled indices", value
        tp = 0.0
        fp = 0.0
        fn = 0.0
        for i in predicted:
            if i in value: tp += 1
            else: fp += 1
        for i in value:
            if i not in predicted: fn += 1
        print "tp: %d. fp: %d, fn: %d" % (tp, fp, fn)
        precision = tp/(tp + fp)
        recall = tp/(tp + fn)
        F1 = 2 * precision * recall / (precision + recall)
        totalF1 += F1
        print "F1 score: ", F1, "\n"
    except ZeroDivisionError:
        print "ZeroDivisionError Encountered with review ", key
        count += 1
        continue

print count
used = len(reviews) - count
print used
print totalF1/used
#0.412077370878
