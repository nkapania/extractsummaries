import hmm
import YelpReview
import utils

YelpHMM = hmm.trainHMM("Labeled_Reviews_1000-1090.json", N = 2, numFeatures = 3)
print YelpHMM.M
print YelpHMM.p
YelpHMM.B.printResults()

TestReview = utils.getReview("htx37hVCEdIQf03QfnL77w")
YelpHMM.summarize(TestReview, 4)