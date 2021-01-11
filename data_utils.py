import re
import string
from nltk.corpus import stopwords

#################################


def clean_text(text):
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