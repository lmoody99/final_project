# coding = utf-8
import spacy
from collections import Counter, defaultdict
from operator import itemgetter

nlp = spacy.load('en')

def read_file(file_name):
    with open(file_name, 'r') as file:
        return file.read().decode('utf-8')

def summarize_text(textfile, lengthOfSummary):
# Process `text` with Spacy NLP Parser
    text = read_file(textfile)
    doc = nlp(text)

    #creates a keyList of top 10 keywords, parses documents into list of sentences
    keywords = Counter()
    for chunk in doc.noun_chunks:
        if nlp.vocab[chunk.lemma_].prob < - 8: # probablity value -8 is arbitrarily selected threshold
            keywords[chunk.lemma_] += 1
    keyList = keywords.most_common(10)
    sentences = [s for s in doc.sents]
    for sentence in sentences:
        print(sentence)
    sentenceList = [] #a 2D array containing the index of each sentence and its score

    #assigining points to each sentence
    for i in range(0,len(sentences)):
        actualSentence = sentences[i].lemma_ #breaks up current sentence in sentences into basic word forms
        sentPoint = 0 #always reset the points when looping through the sentences
        for k in range(0,len(actualSentence)): #this for loop loops through each word in actualSentence
            currentWord = str(actualSentence[k].encode('utf-8')) #assigning currentWord to first word in actualSentence
            for j in range(1,len(keyList)): #starting at one bc the first element in keyList is not a useful keyword, loops through list of keywords
                if currentWord in str(keyList[j][0]): #checking if basic word from sentence is a substring of the keyword
                    sentPoint+= keyList[j][1] #adds points to the sentence equal to the frequency of the keyword
        eachSent = [i, sentPoint] #array containing the index of the currentSentence and its points
        sentenceList.append(eachSent) #add eachSent to the sentenceList

    #sorting the sentences by point value and putting them in a list, sorting those by sentence index and adding it to a string
    sortedSentByPoints = sorted(sentenceList, key=itemgetter(1), reverse=True)
    justSentList = []
    for x in range(0,lengthOfSummary):
        justSentList.append(sortedSentByPoints[x])
    justSentList = sorted(justSentList, key=itemgetter(0), reverse=False)
    summary = ""
    for index in range(0,len(justSentList)):
        summary+=str(sentences[justSentList[index][0]]) + " "

    return summary

length = input("How long should the summary be in sentences?: ")
print
print(summarize_text('pride and prejudice.txt',length))
