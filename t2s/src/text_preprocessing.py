import spacy
from pprint import pprint
import string
import pickle

nlp = spacy.load("en_core_web_sm")

stop_words = {'a', 'am', 'are', 'the', 'am', 'to', 'for', 'of'}

with open('isl_dictionary', 'rb') as dic:
    isl_dict = pickle.load(dic)
# print(isl_dict)

def preprocess_text(text):
    # print(spacy.info())
    res = []
    doc = nlp(text)
    for token in doc:
        pprint((token.text, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop), indent=4)

    return res

text = 'we are waiting for gabriel'
# preprocess_text(text)