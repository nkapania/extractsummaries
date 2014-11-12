"""
#########################################################################
Created by: Sean Shi
Created date: 11/12/14
-------------------------------------------------------------------------
Script that allows user to choose summary sentences from a Yelp review
and save the result in a dictionary with keys as reviewID and values
that are a list of sentence positions within the document that have been
chosen to represent the review.
-------------------------------------------------------------------------
#########################################################################

"""

import collections
import json
import re
import sys

'''
    Breaks down the text of a Yelp review into the following constituents:
    Sentences:  List of sentences that comprise the review.
    Terms:      Dictionary of tokens in the review that are not stop words.
    Keys are the tokens, values are the frequencies of the tokens.
    '''
class Review(object):
    
    # Function: Init
    # --------------
    # Generate a list of sentences based on splitting on punctuation
    # that marks the end of a sentence. Initialize terms list
    def __init__(self, reviewID, reviewText):
        self.id = reviewID
        self.sentences = [sentence.strip() \
                          for sentence in re.split("[.?!]", reviewText) \
                          if sentence.strip() != ""]
        self.terms = collections.Counter()
    
    # Function: ProcessTerms
    # ----------------------
    # Builds a dictionary of tokens. Keys are the token strings.
    # Values are the corresponding frequencies of the token strings.
    def processTerms(self):
        for sentence in self.sentences:
            # Split sentence on whitespace to parse individual tokens
            tokens = sentence.split();
            for token in tokens:
                if token not in stopWords:
                    self.terms[token] += 1


'''
Pull out the first [numIDs] number of business IDs that are categorized
as a Restaurant. There are a total of 14303 business that are categorized
as such. Since it takes < 2 seconds to pull out all business IDs, all
restaurant IDs are pulled out if no argument is provided
'''
def getRestaurantIDs(numIDs=15000):
    # REPLACE WITH YOUR FILE-PATH TO yelp_academic_dataset_business.json HERE
    businessJSON = r"../yelp_academic_dataset_business.json"
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


CHARACTER_MINIMUM = 500

if __name__ == '__main__':
    
    # Ensure that user provides argument that specifies the number of
    # reviews to be labeled.
    if len(sys.argv) != 3:
        print "USAGE: python labeler.py [start_index] [end_index]"
        print "[start_index]: the last review that was previously labeled."
        print "[end_index]: the review that you plan to review up to."
        sys.exit(0)
    
    startInd = int(sys.argv[1])
    endInd = int(sys.argv[2])
    numReviews = endInd - startInd

    # Pulls in the first 50 restaurant IDs
    restaurantIDs = getRestaurantIDs(50)

    # REPLACE WITH YOUR FILE-PATH TO yelp_academic_dataset_review.json HERE
    reviewJSON = r"../yelp_academic_dataset_review.json"
    handle = open(reviewJSON, 'r')

    count = 0
    
    reviewDict = {}
    
    # Pulls out the first [NUM_REVIEWS] reviews that match the business ID
    # in the restaurantIDs list
    word_count = CHARACTER_MINIMUM
    for line in handle:
        if count >= numReviews: break
        review = json.loads(line)
        if review["business_id"] in restaurantIDs:
            if len(review["text"]) > CHARACTER_MINIMUM:
                # Generate a Review object for current review
                r = Review(review["review_id"], review["text"])
                
                # Output relevant review contents
                print "[Review %d]:" % (count+1)
                print "Stars Given: %d" % review["stars"]
                print review["text"] + "\n"
                
                # Cycle through each sentence and wait for user input
                sentenceIndex = 0
                for sentence in r.sentences:
                    print sentence
                    user_input = raw_input("Summary sentence (y/n): ")
                    if user_input == "y":
                        if r.id in reviewDict: reviewDict[r.id].append(sentenceIndex)
                        else: reviewDict[r.id] = [sentenceIndex]
                    sentenceIndex += 1

                count += 1

    handle.close()
    for key, value in reviewDict.items():
        print key, value
