import re
import string
import pandas as pd
import nltk
nltk.download('stopwords') # needed for first time run 
from nltk.corpus import stopwords
from nltk.stem.porter import *
from collections import defaultdict
import numpy as np
#################################


def clean_text(text):
    '''
    Remove urls, mentions, punctuations, numbers, extra
    whitespaces, stopwords and converts tweet to lower-case.
    '''
    # contractions and hyphens
    text = text.replace('—', ' ')
    text = text.replace('-', ' ')
    text = text.replace('\'ve', ' have')
    text = text.replace('n\'t', ' not')
    text = text.replace('n’t', ' not')
    text = text.replace('\'re', ' are')
    text = text.replace('’ve', ' have')
    text = text.replace('\'s', ' is')
    text = text.replace('’s', ' is')
    text = text.replace('’re', ' are')
    text = text.replace('’m', ' am')
    text = text.replace('\’m', ' am')
    text = text.replace('’ll', ' will')
    text = text.replace('\'ll', ' will')
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
    N = len(full_text) # num documents
    wordCount = defaultdict(int) # initialize wordcount dictionary
    stemmer = PorterStemmer() # initialize word stemmer
    stemmed_tweets = []
    for tweet in full_text: 
        new_tweet = []
        for w in tweet:
            w = stemmer.stem(w) # stem each individual word
            wordCount[w] += 1 # increment wordcount
            new_tweet.append(w)
        stemmed_tweets.append(new_tweet)
    
    
    docCount = defaultdict(int) # initialize docCount dictionary
    for tweet in stemmed_tweets:
        for word in wordCount:
            if word in tweet:
                docCount[word] += 1
    counts = [(wordCount[w], docCount[w], w) for w in wordCount]
    counts.sort(reverse = True) # sort from most frequent to least frequent
    stem_counts = pd.DataFrame(data = counts, columns = ['term_count', 'doc_count', 'word'])
    stem_counts['idf'] = np.log((N + 1) / stem_counts['doc_count']) + 1
    stem_counts['tf_idf'] = stem_counts['term_count'] * stem_counts['idf']
    return stem_counts, stemmed_tweets
