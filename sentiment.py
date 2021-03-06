def read_file(file_name):
    with open(file_name, 'r') as file:
        return file.read().decode('utf-8')

import spacy
from collections import Counter, defaultdict

nlp = spacy.load('en')

# Process `text` with Spacy NLP Parser
text = read_file('pride and prejudice.txt')
processed_text = nlp(text)

def get_character_adjectives(doc, character_lemma):
    """
    Find all the adjectives related to `character_lemma` in `doc`

    :param doc: Spacy NLP parsed document
    :param character_lemma: string object
    :return: list of adjectives related to `character_lemma`
    """

    adjectives = []
    for ent in processed_text.ents:
        if ent.lemma_ == character_lemma:
            for token in ent.subtree:
                if token.pos_ == 'ADJ': # Replace with if token.dep_ == 'amod':
                    adjectives.append(token.lemma_)

    for ent in processed_text.ents:
        if ent.lemma_ == character_lemma:
            if ent.root.dep_ == 'nsubj':
                for child in ent.root.head.children:
                    if child.dep_ == 'acomp':
                        adjectives.append(child.lemma_)

    return adjectives

doc_2 = nlp(text)
characters = Counter()
other = Counter()

for ent in doc_2.ents:
    if ent.label_ == "PERSON":
        if nlp.vocab[ent.lemma_].prob < - 8: # probablity value -8 is arbitrarily selected threshold
            characters[ent.lemma_] += 1
    elif ent.label_ == "NORP" or ent.label_ == "ORG" or ent.label_ == "GPE":
        if nlp.vocab[ent.lemma_].prob < - 8: # probablity value -8 is arbitrarily selected threshold
            other[ent.lemma_] += 1
others = other.most_common(5)
chars = characters.most_common(3)
print("Most common people: ")
for char in chars:
    print(char[0])
print('Most common places, nationalities, organizations: ')
for entity in others:
    print(entity[0])

print

for char in chars:
    prettyList = []
    person = char[0]
    charList = get_character_adjectives(processed_text, person)
    if(charList != []):
        for x in range(len(charList)):
            if(charList[x]!="-PRON-" and charList[x] not in prettyList):
                prettyList.append(charList[x])
        print char[0] + ": ",#how to not do a println?
        for elem in prettyList:
            print(elem),
        print
