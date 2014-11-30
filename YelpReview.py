"""
#########################################################################
Created by: Sean Shi
Created date: 11/12/14
Modified date: 11/15/14
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
import math
import utils

class Sentence(object):
    
    # Function: Init
    # --------------
    # Each sentence is associated with five features:
    # 1) Position of sentence in document.
    # 2) Position of sentence in paragraph.
    # 3) Number of terms in the sentence.
    # 4) Baseline term probability
    # 5) Document term probability
    def __init__(self, index, numTerms, baselineProb, documentProb, text):
        # features defined here
        self.index = index
        if (index == 0): self.pos = 1
        else: self.pos = 2
        self.numTerms = math.log10(numTerms + 1)
        self.baselineProb = baselineProb
        self.documentProb = documentProb
        self.phi = [self.pos, self.numTerms, self.baselineProb, self.documentProb]
        self.text = text

class Review(object):
    
    # Function: Init
    # --------------
    # Generate a list of sentences based on splitting on punctuation
    # that marks the end of a sentence. Initialize terms list
    def __init__(self, reviewID):
        self.id = reviewID
        self.sentences = []
        self.terms = collections.Counter()
        self.documentFreq = 0
        self.baselineFreq = 0
    
    # Function: ProcessTerms
    # ----------------------
    # Builds a dictionary of tokens. Keys are the token strings.
    # Values are the corresponding frequencies of the token strings.
    # @param reviewText a list of sentences split on .?! punctuation
    def ProcessTerms(self, reviewText, stopWords):
        for sentence in reviewText:
            # Split sentence on whitespace to parse individual tokens.
            # Ignore tokens that are stop words.
            # Only store lowercase version of tokens without any punctuation.
            tokens = utils.processSentenceText( sentence )
            for token in tokens: self.terms[token] += 1
        self.documentFreq = float(len(list( self.terms.elements() )))
        self.baselineFreq = float(utils.getOccurancesFromCorpus(self.terms))

    # Function: ProcessSentences
    # --------------------------
    # Builds a list of Sentence Objects.
    def ProcessSentences(self, reviewText):
        for i in range(len(reviewText)):
            terms = utils.processSentenceText(reviewText[i])
            baselineProb = 0
            documentProb = 0
            for term in terms:
                baselineTermFreq = utils.getFreqFromCorpus(term)
                baselineProb += math.log(baselineTermFreq/self.baselineFreq)
                docTermFreq = self.terms[term]
                documentProb += math.log(docTermFreq/self.documentFreq)
            s = Sentence(i, len(terms), baselineProb, documentProb, reviewText[i])
            self.sentences.append(s)

    # Function: PrintContents
    # -----------------------
    # Prints out contents of the Review object.
    def PrintContents(self):
        print "Review ID:", self.id
        print "Number of terms", self.documentFreq
        print "Number of terms in baseline", self.baselineFreq
        for k, v in self.terms.items(): print k, v
        for sentence in self.sentences:
            print "Position", sentence.pos
            print "Term Probability", sentence.numTerms
            print "Baseline Probability", sentence.baselineProb
            print "Document Probability", sentence.documentProb









