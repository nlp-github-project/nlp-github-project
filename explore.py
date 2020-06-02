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
    
    
def plot_distro_for_value_counts_all(df):
    """
    Creates a bar graph for the value counts of the readmes for all languages
    """
    
    c="#84aae2"
    value_counts_all = pd.DataFrame(df.language.value_counts(ascending=False))
    plt.figure(figsize=(13,10))
    bar = sns.barplot(x=value_counts_all.index, y="language", data=value_counts_all, color = c)
    bar.set_xticklabels(bar.get_xticklabels(),rotation=65)
    bar.set_ylabel("counts")

    plt.title("How is the data distributed per document for all languages?")
    plt.show()
    
    
def plot_distro_for_value_counts_top(df):
    """
    Creates a bar graph for the value counts of the readmes for top languages
    """
    c="#84aae2"
    value_counts = pd.DataFrame(df.is_top_language.value_counts(ascending=False))
    plt.figure(figsize=(13,10))
    bar = sns.barplot(x=value_counts.index, y="is_top_language", data=value_counts, color = c)
    bar.set_xticklabels(bar.get_xticklabels(),rotation=65)
    bar.set_ylabel("counts")

    plt.title("How is the data distributed per document for top languages?")
    plt.show()
    
    
def scatterplot_for_readmes(df):
    """creates a scatterplot of the readmes and their lengths"""
    #look at the lengths per readme so we can compare by language
    df_length = df.assign(length = df.clean_lemmatized.apply(len))

    plt.figure(figsize=(13,10))
    ax = plt.subplot(111)

    plt.title("What are the lengths of readme files per programming language?")
    sns.scatterplot(y=df_length.length, x=df_length.index,hue=df_length.language)

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), shadow=True, ncol=2)
    plt.show()