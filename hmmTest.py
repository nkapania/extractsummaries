import hmm
import YelpReview

YelpHMM = hmm.trainHMM("Labeled_Reviews_1000-1090.json", N = 2, numFeatures = 3)