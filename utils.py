"""
#########################################################################
Created by: Sean Shi
Created date: 11/13/14
Modified data: 11/25/14
-------------------------------------------------------------------------
Some helpful functions for manipulating JSON documents.
-------------------------------------------------------------------------
#########################################################################
"""

import collections
import json
import re
import string
import YelpReview

# REPLACE WITH YOUR FILE-PATH TO yelp_academic_dataset_business.json HERE
businessJSON = r"../yelp_academic_dataset_business.json"
# REPLACE WITH YOUR FILE-PATH TO yelp_academic_dataset_review.json HERE
reviewJSON = r"../yelp_academic_dataset_review.json"


'''
Read in file of stop words. Stop words are common terms that hold little value
in the context of understanding the document when assessed alone. Many functions
utilize this list so load it only once for efficiency.
'''
handle = open("stopWords.txt", 'r')
STOPWORDS = set([line.strip() for line in handle.readlines()])
handle.close()
# Container of all punctuation to be removed from strings
REGEX = re.compile('[%s]' % re.escape(string.punctuation))


'''
Pull out the first [numIDs] number of business IDs that are categorized
as a Restaurant. There are a total of 14303 business that are categorized
as such. Since it takes < 2 seconds to pull out all business IDs, all
restaurant IDs are pulled out if no argument is provided
'''
def getRestaurantIDs(numIDs=15000):
    handle = open(businessJSON, 'r');
    count = 0
    
    restaurantIDs = []
    for line in handle:
        # Break from document parsing if input limit has reached
        if count >= numIDs: break
        business = json.loads(line)
        if "Restaurants" in business["categories"]:
            restaurantIDs.append(business["business_id"])
            count += 1
    handle.close()
    return restaurantIDs

'''
Take in a JSON file that contains user defined summaries for select reviews.
The output dictionary is composed of ReviewIDs as keys, with corresponding
lists of sentence indices as values.
@param jsonFilename - filename of the JSON document containing user labeled reviews
'''
def loadLabeledReviews(jsonFilename):
    handle = open(jsonFilename)
    reviewDict = json.loads(handle.read())
    handle.close()
    return reviewDict


# Remove punctuation and whitespace from sentences in review.
# Return the sentences in a list.
def processReviewText(text):
    return [sentence.strip() \
            for sentence in re.split("[.?!]", text) \
            if sentence.strip() != ""]


'''
Take in a sentence string and process individual words as tokens. Replace all
punctuation from token with spaces, and convert it into lowercase. Append to 
return list if the token does not belong to the set of STOPWORDS.
'''
def processSentenceText(text):
    tokens = []
    for token in REGEX.sub(' ', text).lower().split():
        if token not in STOPWORDS: tokens.append(token)
    return tokens



'''
Look through all reviews until reviewID matches input ID. Build review object
from matching review
'''
def getReview(id):
    handle = open(reviewJSON, 'r')
    # Hardcoded to a document containing most common stop words.
    
    for line in handle:
        review = json.loads(line)
        if review["review_id"] == id:
            reviewText = processReviewText(review["text"])
            r = YelpReview.Review(id)
            r.ProcessTerms(reviewText, STOPWORDS)
            r.ProcessSentences(reviewText)
            break

    handle.close()
    return r

def getAverageSummaryLength(corpus):
    reviewDict = loadLabeledReviews(corpus)
    numReviews = 0
    numSummarySentences = 0
    for key, value in reviewDict.items():
        try:
            numSummarySentences += len(value)
            numReviews += 1
        except TypeError: continue

    print numSummarySentences, numReviews, numSummarySentences/numReviews


'''
There are 1,125,458 total reviews. Of those 706,646 reviews are listed under the
category Restaurants. This function builds a corpus.json file that is a counter
of all the terms in the 706,646 reviews excluding punctuation and stop words.
'''
def createRestaurantCorpus():
    # convert to set for faster membership testing
    restaurantIDs = set(getRestaurantIDs())
    corpus = collections.Counter()
    handle = open(reviewJSON, 'r')

    count = 0
    for line in handle:
        review = json.loads(line)
        if review["business_id"] in restaurantIDs:
            count += 1
            print count
            for token in REGEX.sub(' ', review["text"]).lower().split():
                if token not in STOPWORDS: corpus[token] += 1

    handle.close()

    handle = open("corpus.json", 'w')
    json.dump(corpus, handle, indent=2)
    handle.close()

corpus = loadLabeledReviews("corpus.json")

def getOccurancesFromCorpus(termCounter):
    total = 0
    for term in termCounter: total += corpus[term]
    return total

def getFreqFromCorpus(term):
    return corpus[term]

