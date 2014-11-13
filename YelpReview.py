"""
#########################################################################
Created by: Sean Shi
Created date: 11/12/14
-------------------------------------------------------------------------
Breaks down the text of a Yelp review into the following constituents:
ID:         Unique identifier for the review.
Sentences:  List of sentences that comprise the review.
Terms:      Dictionary of tokens in the review that are not stop words.
Keys are the tokens, values are the frequencies of the tokens.
-------------------------------------------------------------------------
#########################################################################

"""

import collections
import re

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

