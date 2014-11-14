"""
#########################################################################
Created by: Sean Shi
Created date: 11/12/14
Modified data: 11/13/14
-------------------------------------------------------------------------
Script that allows user to choose summary sentences from a Yelp review
and save the result in a dictionary with keys as reviewID and values
that are a list of sentence positions within the document that have been
chosen to represent the review.
-------------------------------------------------------------------------
#########################################################################
"""

import json
import sys
import utils
import YelpReview

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

    # Pulls in the first 50 restaurant IDs
    restaurantIDs = utils.getRestaurantIDs(50)

    # REPLACE WITH YOUR FILE-PATH TO yelp_academic_dataset_review.json HERE
    reviewJSON = r"../yelp_academic_dataset_review.json"
    handle = open(reviewJSON, 'r')

    count = 0
    
    reviewDict = {}
    
    # Pulls out the first [NUM_REVIEWS] reviews that match the business ID
    # in the restaurantIDs list
    word_count = CHARACTER_MINIMUM
    for line in handle:
        if count >= endInd: break
        review = json.loads(line)
        if review["business_id"] in restaurantIDs:
            if len(review["text"]) > CHARACTER_MINIMUM:
                if count < startInd:
                    count += 1
                    continue
                id = review["review_id"]
                
                # Output relevant review contents
                print "[Review %d]:" % (count+1)
                print "Stars Given: %d" % review["stars"]
                print review["text"] + "\n"
                
                # Cycle through each sentence and wait for user input
                sentenceIndex = 0
                for sentence in utils.processReviewText(review["text"]):
                    print sentence
                    user_input = raw_input("Summary sentence (y/n): ")
                    if user_input == "y":
                        if id in reviewDict: reviewDict[id].append(sentenceIndex)
                        else: reviewDict[id] = [sentenceIndex]
                    sentenceIndex += 1
            
                # Open, write, close to save intermediate progress
                output = open("Labeled_Reviews.json", 'w')
                json.dump(reviewDict, output, indent=4)
                output.close()

                count += 1

    handle.close()
