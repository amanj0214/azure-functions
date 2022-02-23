import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import re
import string

from collections import Counter

import nltk
from nltk.corpus import stopwords
from nltk import PorterStemmer

from nltk.stem import WordNetLemmatizer

from transformers import pipeline

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('omw-1.4')

ct_custom_dictionary = {
    "certainteed": [" ct "],
    #"siding": ["started", "home"]
}

def replace_words(text, ct_custom_dictionary):
    """
    Replaces dictionary words with single word to replace synonyms with origin (domain specific to CertainTeed).
    
    Args:
        text(str): String to replace text
        ct_custom_dictionary(dict): Dictionary of synonyms
    Return:
        Text with replacements
    """
    for k, v in ct_custom_dictionary.items():
        for v_temp in v:
            text = text.replace(v_temp, k)
    return text

def clean_text(text):
    """
    Removes emojis, encode to ASCII, removes unwanted characters (spaces, etc.), removes stopwords, lemmatizes the word, and replaces synonyms.

    Args:
        text(str): Text to clean
    Returns:
        text_cleaned(str): Cleaned text
    """

    # remove emojis
    text = text.encode('ascii', 'ignore').decode('ascii') 
    characters_to_remove = string.punctuation + string.digits
    
    text_cleaned = text
    # remove unwanted characters
    for temp_char in characters_to_remove:
        text_cleaned = text_cleaned.replace(temp_char, " ")
    #text_cleaned = "".join([x for x in text if x not in characters_to_remove]) 

    text_cleaned = re.sub(' +', ' ', text_cleaned) # remove extra white spaces
    text_cleaned = text_cleaned.lower() # converting to lowercase
    tokens = text_cleaned.split(" ")
    tokens = [token for token in tokens if token not in stopwords.words("english")] # Taking only those words which are not stopwords

    # ps=PorterStemmer()
    # text_cleaned=" ".join([ps.stem(token) for token in tokens])
    
    wordnet_lemmatizer = WordNetLemmatizer()

    text_cleaned = " ".join([wordnet_lemmatizer.lemmatize(token) for token in tokens])

    text_cleaned = replace_words(text_cleaned, ct_custom_dictionary)

    print(text_cleaned)

    return text_cleaned


def get_text_features(text):
    '''
    Returns text features

    Args:
        text(str): Text from which the features needs to be extracted
    Returns:
        features such as sentiment
    '''
    # %%
    # https://huggingface.co/siebert/sentiment-roberta-large-english
    # sentiment_analysis = pipeline("sentiment-analysis",
    #         model="siebert/sentiment-roberta-large-english")
    sentiment_analysis = pipeline("sentiment-analysis")

    sentiment_result = sentiment_analysis(text)
    
    print(sentiment_result)

    return sentiment_result