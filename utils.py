"""
#########################################################################
Created by: Sean Shi
Created date: 11/13/14
-------------------------------------------------------------------------
Some helpful functions for manipulating JSON documents.
-------------------------------------------------------------------------
#########################################################################
"""


import json
import re
import YelpReview

# REPLACE WITH YOUR FILE-PATH TO yelp_academic_dataset_business.json HERE
businessJSON = r"yelp_academic_dataset_business.json"
# REPLACE WITH YOUR FILE-PATH TO yelp_academic_dataset_review.json HERE
reviewJSON = r"yelp_academic_dataset_review.json"

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


'''
Read in file of stop words. Stop words are common terms that hold little value
in the context of understanding the document when assessed alone.
'''
def loadStopWords(stopWordFilename):
    handle = open(stopWordFilename, 'r')
    stopWords = [line.strip() for line in handle.readlines()]
    handle.close()
    return stopWords



# Remove punctuation and whitespace from sentences in review.
# Return the sentences in a list.
def processReviewText(text):
    return [sentence.strip() \
            for sentence in re.split("[.?!]", text) \
            if sentence.strip() != ""]


'''
Look through all reviews until reviewID matches input ID. Build review object
from matching review
'''
def getReview(id):
    handle = open(reviewJSON, 'r')
    # Hardcoded to a document containing most common stop words.
    stopWords = loadStopWords("stopWords.txt")
    
    for line in handle:
        review = json.loads(line)
        if review["review_id"] == id:
            reviewText = processReviewText(review["text"])
            r = YelpReview.Review(id)
            r.ProcessTerms(reviewText, stopWords)
            r.ProcessSentences(reviewText)
            break

    handle.close()
    return r









