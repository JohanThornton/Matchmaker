"""
Matching algorithm
Given names with several categories of tags, we find optimal pairings that share tags. Earlier tags are weighted
higher, and the different categories are individually weighted. Categories can have different maximum tag numbers.

Written by: Johan Thornton
Modified by:
Date: 2020-10-07
Created: 2020-10-05

This algorithm takes as inputs:
 - a dict of
	 - names : list of
		- categories, a list of
		   - tags
 - a dict of
	 - names : list of
		- names (that have already been matched)
 - an array of category weightings, matching the number of categories
 - an array of the maximum number of items in each category, to calculate the item weighting table
"""

import random, json, pprint, time
#from colorama import Fore, Style


import spacy
import en_core_web_lg

cPink = '\033[95m'
cBlue = '\033[94m'
cGreen = '\033[92m'
cYellow = '\033[93m'
cOrange = '\033[91m'
#C6 = '\033[0m'
cGray = '\033[1m'
cWhite = '\033[4m'
"""
import nltk
from nltk.corpus import wordnet

def nlpCompareWords(word1, word2):
   syn1 = wordnet.synsets(word1)[0]
   syn2 = wordnet.synsets(word2)[0]
   similarity = syn1.wup_similarity(syn2)
   return similarity
"""
nlp = en_core_web_lg.load()


def nlpCompareWords(word1, word2):
	#return 0
	tokenString = word1 + " " + word2
	tokens = nlp(tokenString)
	token1, token2 = tokens[0], tokens[1]
	similarity = token1.similarity(token2)
	return similarity


compareTests = [["camera", "photography", "photographer", "photo", "photograph", "nurse", "doctor", "scuba", "diving"],

#compareTests = [["camera", "photography", "photographer", "photo", "photograph", "nurse", "doctor", "scuba", "diving", "car", "drive", "driving"],
				["manager", "management", "engineer", "engineering", "nurse", "nursing", "medicine", "doctor", "hospital", "airplane", "airplanes", "pilot"],
				["big", "enormous", "huge", "immense", "gigantic", "vast", "colossal", "gargantuan", "large", "sizable",
				 "grand", "great"],
				["oil", "gasoline", "energy", "refinery", "boat", "ship", "sailboat", "sailing", "captain", "rowboat",
				 "canoe", "kayak"]
				]


def nlpTest():

	print("hello")
	#nlp = spacy.load('en_core_web_sm')
	#  nlp = en_core_web_lg.load()
	for compareTest in compareTests:
		print(13 * " " + cGray + "{:>13}".format(compareTest[0]))

		y = 0
		for cword1 in compareTest:
			x = 0
			cstring = cBlue + "{:>13}".format(cword1)
			for cword2 in compareTest:
				if x == y:
					cstring += cOrange + "            -"
				elif x == y + 1:
					cstring += cGray + "{:>13}".format(cword2)
				elif x < y:
					sim = nlpCompareWords(cword1, cword2)
					if sim == None:
						sim = 0.0
					if sim < 0.6:
						#cstring += "{:13}".format(int(sim * 100))
						cstring += cBlue
					else:
						#bstring = "[" + str(int(sim*100)) + "]"
						#cstring += "{:13}".format(bstring)
						cstring += cYellow
					cstring += "{:13}".format(int(sim * 100))
					#cstring += 11 * " " + cword2[0] + cword1[0]

				x += 1
			print(cstring)
			y += 1

		print("$\n")
		exit()
	exit()


originalPeopleTags = {
	"p0": [["a"], ["t1", "t2"], ["i1", "i2"]],
	"p1": [["a", "c", "r"], ["t1", "t3"], ["i4", "i3"]],
	"p2": [["a", "d", "k"], ["t4", "t5"], ["i8", "i2"]],
	"p3": [["f", "d", "k"], ["t4", "t1"], ["i5", "i1"]],
	"p4": [["f", "k", "j", "a"], ["t3", "t2"], ["i1", "i6"]],
	"p5": [["g", "f", "j"], ["t5"], ["i1", "i7"]],
	"p6": [["h", "e", "j"], ["t6", "t2"], ["i2", "i7"]],
	"p7": [["h", "d", "l"], ["t8", "t3"], ["i7", "i1"]],
	"p8": [["i", "f", "l"], ["t9", "t4"], ["i3", "i5"]],
	"p9": [["a", "b", "c"], ["t1", "t3"], ["i5", "i2"]],
	"p10": [["xxx"], ["t1", "t2"], ["i1", "i2"]]
}

alreadyMet = {
	"p0": [],
	"p1": [],
	"p2": [],
	"p3": [],
	"p4": [],
	"p5": [],
	"p6": [],
	"p7": [],
	"p8": [],
	"p9": [],
	"p10": [],
}

# These are the weightings for each category
# They will be passed to this function for each individual implementation
categoryWeightings = [1.0, 0.5, 0.3, 0.3]

"""
Calculate weightings of ordered items, for each category.
Each category can have a different number of maximum entries/items/tags

   Arguments:
	  [ <category1Items>, <category2Items>, ... <categoryNItems> ]

   Example:
	  [3, 1, 5, 5]
		 Industry, title, hobbies, favourite animal
		 
   Returns:
	  Nothing
"""
itemWeightingsByCategory = []


def calculateWeightingTables(maxItemsList):
	categories = len(maxItemsList)
	for cat in range(categories):
		# Get the number of items in this category
		maxItems = maxItemsList[cat]
		weightings = []
		for index in range(maxItems):
			# This formula could change:
			weightings.append(1 / (index + 1))
		itemWeightingsByCategory.append(weightings)
	pprint.pprint(itemWeightingsByCategory)


"""
Generate a set of random people.

   Arguments:
	  <number of people>, <number of categories>

   Example:
	  30, 3
	  
   Returns:
	  Nothing
"""


def generateRandomPeople(number, categories):
	random.seed(0)
	alreadyMet.clear()
	originalPeopleTags.clear()
	for index in range(number):
		name = "P" + str(index)
		# Add empty alreadyMet to dict
		alreadyMet[name] = []
		# Add random category entries
		entryList = []
		for cat in range(categories):
			# Generate category names starting with "A"
			catName = chr(ord("A") + cat)
			# Generate a random number of items
			items = []
			for item in range(random.randrange(0, 5)):
				# add random digit
				items.append(catName + str(random.randrange(0, 9)))
			entryList.append(items)
		originalPeopleTags[name] = entryList
	pprint.pprint(originalPeopleTags)


"""
Compare two items.

   Arguments:
	  <string 1>, <string 2>

   Example:
	  "nurse", "nursing"
	  
   Returns:
	  Boolean; will be changed to float
"""


def stringCompare(string1, string2):
	# Later add comparing similar words with NLTK
	#  Replace boolean return value with float between 0 and 1
	return string1 == string2


"""
Compare a single category.

   Arguments:
	  <list of tags>, <list of tags>, <category number>

   Example:
	  ["oil", "energy", "transportation"], ["natural gas", "oil"], 0
	  
   Returns:
	  Float
"""


def compareTags(myTags, matchTags, category):
	matchFactor = 0.0
	myTagCount = 0
	# Compare all of the source tags...
	for myTag in myTags:
		matchTagCount = 0
		# ... to all of the destination tags
		for tag in matchTags:
			if stringCompare(tag, myTag):
				# Get the combined weightings for this category, and add it to the match factor
				matchFactor += itemWeightingsByCategory[category][myTagCount] * \
							   itemWeightingsByCategory[category][matchTagCount]
			matchTagCount += 1
		myTagCount += 1
	return matchFactor


"""
Compare the weighted set of multiple category items.

   Arguments:
	  [[<itemSourceA1>, .. <itemSourceAN>], ... [<itemSourceZ1>, ... <itemSourceZN>]],    
		 [[<itemDestA1>, .. <itemDestAN>], ... [<itemDestZ1>, ... <itemDestZN>]],    


   Example:
	  [["oil", "energy", "transportation"],["manager", "engineer"]] ,[["natural gas", "oil"], ["engineer"]]
	  
   Returns:
	  Float
"""


def compareMultipleTags(myTagList, matchTagList):
	totalMatchFactor = 0.0
	# For each category...
	for index in range(len(myTagList)):
		# ... add the weighted match factor, passing the category number to get the correct weighting table
		totalMatchFactor += compareTags(myTagList[index], matchTagList[index], index) * categoryWeightings[index]
	return totalMatchFactor


"""
Find a match for a single person.

   Arguments:
	  <name>
	  
   Example:
	  "john.q.engineer@somecompany.com"
	  
   Returns:
	  List [string, float]
"""


def findMatch(name):
	maxMatchFactor = 0.0
	matchName = "None"
	myTags = peopleTags[name]
	for person in peopleTags:
		# Don't try to match yourself!
		if person != name:
			# Make sure they haven't been matched before
			if person not in alreadyMet[name]:
				matchTags = peopleTags[person]
				thisMatchFactor = compareMultipleTags(myTags, matchTags)
				if thisMatchFactor > maxMatchFactor:
					# Keep best match
					maxMatchFactor = thisMatchFactor
					matchName = person
	return [matchName, maxMatchFactor]


"""
Find the best matches possible, with the remaining people. Return True if at least one match was found.

   Arguments:
	  None
	  
   Returns:
	  Boolean
"""


def getAllMatches():
	foundMatch = {}
	allDone = False
	# Do this while there are at least two people left; or exit if everyone is unmatched
	while (len(peopleTags) > 1) and not allDone:
		bestMatchFactor = 0.0
		for person in peopleTags:
			# Scan all other people
			matchPerson = findMatch(person)
			matchPersonName = matchPerson[0]
			matchPersonFactor = matchPerson[1]
			if matchPersonFactor > bestMatchFactor:
				# Best match so far
				bestMatchFactor = matchPersonFactor;
				bestPerson = person
				bestMatch = matchPersonName
		if bestMatchFactor > 0.0:
			# We have found a match, and it's not the end of a search
			print("  Match:", bestPerson, "-", bestMatch, ":", "%.2f" % bestMatchFactor)
			# Remove the two people
			peopleTags.pop(bestPerson)
			peopleTags.pop(bestMatch)
			# Add to each other's list of previously matched people
			alreadyMet[bestPerson].append(bestMatch)
			alreadyMet[bestMatch].append(bestPerson)
		else:
			# All done here
			allDone = True
	unMatched = ""
	# Print all the unmatched people
	for person in peopleTags:
		unMatched += person + " "
	print("  Unmatched:", unMatched)
	# Now return True if there was a match
	return len(peopleTags) != len(originalPeopleTags)


"""
Main(): Run a continuous set of searches until no matches are left, and time it.
   
   Arguments:
	  None
	  
   Returns:
	  Nothing
"""
if __name__ == '__main__':

	#nlpTest()

	# The arguments to this function is an array of how many entries can be made in each category
	calculateWeightingTables([5, 5, 5, 5, 5])
	# Make random people
	# generateRandomPeople(20, 4)

	startTime = time.time()
	moreMatches = True
	totalRuns = 0
	# Now loop while there are still more unmatched pairs
	while moreMatches:
		totalRuns += 1
		print("Run #", totalRuns)
		peopleTags = originalPeopleTags.copy()
		# Let's find all best matches that haven't been made before
		moreMatches = getAllMatches()  # Returns False if we're all done

	print(f"--- {(time.time() - startTime):.2f} seconds ---")
