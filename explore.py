import pandas as pd
import numpy as np

from requests import get
from bs4 import BeautifulSoup
import os

import seaborn as sns
import matplotlib.pyplot as plt

import prepare

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import nltk
import nltk.sentiment
import re


def most_common_words(df):

    ADDITIONAL_STOPWORDS = ['r', 'u', '2', 'ltgt']

    def clean(text: str) -> list:
        'A simple function to cleanup text data'
        wnl = nltk.stem.WordNetLemmatizer()
        stopwords = nltk.corpus.stopwords.words('english') + ADDITIONAL_STOPWORDS
        text = (text.encode('ascii', 'ignore')
                .decode('utf-8', 'ignore')
                .lower())
        words = re.sub(r'[^\w\s]', '', text).split() # tokenization
        return [wnl.lemmatize(word) for word in words if word not in stopwords]

    all_words = clean(' '.join(df.clean_lemmatized))
    python_words = clean(' '.join(df[df.language == 'Python'].clean_lemmatized))
    javascript_words = clean(' '.join(df[df.language == 'JavaScript'].clean_lemmatized))
    java_words = clean(' '.join(df[df.language == 'Java'].clean_lemmatized))
    c_plus_plus_words = clean(' '.join(df[df.language == 'C++'].clean_lemmatized))

    figure, axes = plt.subplots(1, 5)

    pd.Series(all_words).value_counts().head(12).plot.barh(width=.9, ec='black', title='12 most common words in all README', figsize=(19,10), ax=axes[0])
    pd.Series(python_words).value_counts().head(12).plot.barh(width=.9, ec='black', title='12 most common words in Python', figsize=(19,10), ax=axes[1])
    pd.Series(javascript_words).value_counts().head(12).plot.barh(width=.9, ec='black', title='12 most common words in JavaScript', figsize=(19,10), ax=axes[2])
    pd.Series(java_words).value_counts().head(12).plot.barh(width=.9, ec='black', title='12 most common words Java', figsize=(19,10), ax=axes[3])
    pd.Series(c_plus_plus_words).value_counts().head(12).plot.barh(width=.9, ec='black', title='12 most common words C++', figsize=(19,10), ax=axes[4])

    plt.tight_layout()

def plot_word_count_distribution(df):
    
    def word_count(word):
        word_count = len(re.findall(r'\w+', word))
        return word_count

    word_count = df.clean_lemmatized.apply(word_count)
    df["word_count"] = word_count

    plt.figure(figsize=(12,8))
    sns.distplot(df.word_count)
    plt.title("Word Count Distribution")