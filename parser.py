import sys
import json
import re
import collections

# List of stop words
stopWords = [ "a", "an", "and", "are", "as", "at",
              "be", "by", "for", "from", "has", "he",
              "in", "is", "it", "its", "of", "on",
              "that", "the", "to", "was", "were",
              "will", "with" ]


class Sentence(object):

    # Function: Init
    # --------------
    # Each sentence is associated with five features:
    # 1) Position of sentence in document.
    # 2) Position of sentence in paragraph.
    # 3) Number of terms in the sentence.
    # 4) Baseline term probability
    # 5) Document term probability
    def __init__(self, sentenceText, docPos, paraPos):
        self.text = sentenceText
        # features defined here
        self.pos = docPos
        self.paraPos = paraPos
        self.numTerms = 0
        self.baselineProb = 0
        self.docProb = 0


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
    def __init__(self, reviewText):
        self.sentences = re.split("[.?!]", reviewText)
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

NUM_BUSINESS_IDS = 15
CHARACTER_MINIMUM = 500
NUM_REVIEWS = 5

if __name__ == '__main__':
    
    # REPLACE WITH YOUR FILE-PATH TO yelp_academic_dataset_business.json HERE
    businessJSON = r"yelp_academic_dataset_business.json"
    handle = open(businessJSON, 'r');
    count = 0
    
    # Pulls in the first NUM_BUSINESS_IDS business IDs that are restaurants.
    businessIDs = []
    for line in handle:
        if count > NUM_BUSINESS_IDS: break
        business = json.loads(line)
        if "Restaurants" in business["categories"]:
            businessIDs.append(business["business_id"])
            count += 1
    handle.close()


    # REPLACE WITH YOUR FILE-PATH TO yelp_academic_dataset_review.json HERE
    reviewJSON = r"yelp_academic_dataset_review.json"
    handle = open(reviewJSON, 'r')

    # Creates a file called reviews.txt in same location as parser.py
    outFile = open("reviews.txt", 'w')
    count = 0

    # List of review objects
    reviews = []

    # Pulls out the first reviews that match the business ID in the businessIDs list
    word_count = CHARACTER_MINIMUM
    for line in handle:
        if count > NUM_REVIEWS: break
        review = json.loads(line)
        if review["business_id"] in businessIDs[4:]:
            if len(review["text"]) > word_count:
                # Generate a Review object here
                reviews.append( Review(review["text"]) )
                
                outFile.write("[Review %d]:\n" % (count+1))
                outFile.write("Stars Given: %d\n" % review["stars"])
                outFile.write(review["text"])
                outFile.write("\n\n")
                count += 1

    handle.close()
    outFile.close()

    r = reviews[0]
    r.processTerms()
    for key, value in r.terms.items():
        print key, value


