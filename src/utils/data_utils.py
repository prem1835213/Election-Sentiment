import re
import string
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.porter import *
from collections import defaultdict

#################################


def clean_text(text):
    '''
    Remove urls, mentions, punctuations, numbers, extra
    whitespaces, stopwords and converts tweet to lower-case.
    '''
    text = text.replace('\n', ' ')
    text = re.sub(r'http://\S+|https://\S+', '', text) # removes urls
    text = re.sub(r'(@\w+\b)', '', text) # removes mentions
    text = re.sub(r'[^\w\s]', '', text) # removes punctuation
    text = re.sub(r'\d', '', text) # removes numbers
    text = text.replace('\xa0', '') # removes non-breaking whitespace
    text = text.replace('  ', ' ') # removes double spaces
    text = text.replace('  ', ' ') # double space removal again for edge cases
    text = text.strip() # removes trailing and leading whitespaces
    text = text.lower() # converts to lower case
    
    stop_words = set(stopwords.words('english'))
    text = [word for word in text.split() if not (word in stop_words)] # removes stopwords
    
    return text


def stemmed_text(full_text):
    '''
    Stems the full_text input and returns a dataframe 
    with the count of each distinct word. This function 
    requires input to be cleaned first using clean_text.
    '''
    wordCount = defaultdict(int) # initialize wordcount dictionary
    stemmer = PorterStemmer() # initialize word stemmer
    for tweet in full_text:
        for w in tweet:
            w = stemmer.stem(w) # stem each individual word
            wordCount[w] += 1 # increment wordcount
    counts = [(wordCount[w], w) for w in wordCount]
    counts.sort(reverse = True) # sort from most frequent to least frequent
    output = pd.DataFrame(data = counts, columns = ['count', 'word'])
    return output
