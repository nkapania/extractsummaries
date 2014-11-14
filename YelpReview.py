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
import string

class Sentence(object):
    
    # Function: Init
    # --------------
    # Each sentence is associated with five features:
    # 1) Position of sentence in document.
    # 2) Position of sentence in paragraph.
    # 3) Number of terms in the sentence.
    # 4) Baseline term probability
    # 5) Document term probability
    def __init__(self, sentenceText, index):
        self.text = sentenceText
        # features defined here
        self.index = index
        self.terms = collections.Counter()
        self.baselineProb = 0
        self.docProb = 0


class Review(object):
    
    # Function: Init
    # --------------
    # Generate a list of sentences based on splitting on punctuation
    # that marks the end of a sentence. Initialize terms list
    def __init__(self, reviewID):
        self.id = reviewID
        self.sentences = []
        self.terms = collections.Counter()
    
    # Function: ProcessTerms
    # ----------------------
    # Builds a dictionary of tokens. Keys are the token strings.
    # Values are the corresponding frequencies of the token strings.
    def ProcessTerms(self, reviewText, stopWords):
        for sentence in reviewText:
            # Split sentence on whitespace to parse individual tokens.
            # Ignore tokens that are stop words.
            # Only store lowercase version of tokens without any punctuation.
            tokens = sentence.split()
            for token in tokens:
                # remove all punctuation from token
                token = ''.join([c for c in token if c not in string.punctuation])
                if token.lower() not in stopWords:
                    self.terms[token.lower()] += 1

    # Function: ProcessSentences
    # --------------------------
    # Builds a list of Sentence Objects.
    def ProcessSentences(self, reviewText):
        for i in range(len(reviewText)):
            self.sentences.append( Sentence(reviewText[i], i) )









