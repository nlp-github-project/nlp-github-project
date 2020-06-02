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
from wordcloud import WordCloud


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
    
    
def bargraphs_for_min_max_median(df):
    
    """
    Creates a bargraph for readme counts per language for the following:
    min, max, and median
    """
    df_length = df.assign(length = df.clean_lemmatized.apply(len))

    median_lengths = df_length.groupby("language").median().sort_values(by="length", ascending= False)
    max_length = pd.DataFrame(df_length.groupby("language").length.max().sort_values(ascending= False))
    min_length = pd.DataFrame(df_length.groupby("language").length.min().sort_values(ascending= False))


    c="#84aae2"
    plt.figure(figsize=(13,10))
    plt.title("What is the median length of readme files per language?")
    bar = sns.barplot(y=median_lengths.length,x=median_lengths.index, color=c)

    bar.set_xticklabels(bar.get_xticklabels(),rotation=65)
    plt.show()

    plt.figure(figsize=(13,10))
    plt.title("What is the minimum length of readme files per language?")
    bar = sns.barplot(y=min_length.length,x=min_length.index, color=c)

    bar.set_xticklabels(bar.get_xticklabels(),rotation=65)
    plt.show()

    plt.figure(figsize=(13,10))
    plt.title("What is the maximum length of readme files per language?")
    bar = sns.barplot(y=max_length.length,x=max_length.index, color=c)

    bar.set_xticklabels(bar.get_xticklabels(),rotation=65)
    plt.show()

    
def word_count(word):
    """
    returns the word count of readme
    """
    word_count = len(re.findall(r'\w+', word))
    return word_count

    
def word_count_summary(df):
    "returs a summary of the top language word counts"
    df["word_count"] = df.clean_lemmatized.apply(word_count)
    
    min_word_count = pd.DataFrame(df.groupby("is_top_language").word_count.min())
    min_word_count.columns = ['Min Word Count']

    max_word_count = pd.DataFrame(df.groupby("is_top_language").word_count.max())
    max_word_count.columns = ["Max Word Count"]

    median_word_count = pd.DataFrame(df.groupby("is_top_language").word_count.median())
    median_word_count.columns = ["Median Word Count"]

    mean_word_count = pd.DataFrame(df.groupby("is_top_language").word_count.mean())
    mean_word_count.columns = ["Mean Word Count"]

    std_word_count = pd.DataFrame(df.groupby("is_top_language").word_count.std())
    std_word_count.columns = ["STD of Word Count"]
    
    summary1 = pd.merge(min_word_count, max_word_count, left_index=True, right_index=True)
    summary2 = pd.merge(median_word_count , mean_word_count , left_index=True, right_index=True)
    summary3 = pd.merge(summary1 , summary2 , left_index=True, right_index=True)
    summary = pd.merge(summary3 , std_word_count , left_index=True, right_index=True)
    
    return summary


def list_of_words_for_top_languages(dfx, language="is_top_language", cleaned="clean_lemmatized"):
    """Creates a list of words for each language in the top programming languages
    returns in this order:
    java script words, python words, java words, C++ words, other languages words, all words
    """
    # create list of words by language

    js_words = ' '.join(dfx[dfx[language] == 'JavaScript'][cleaned]).split()
    p_words = ' '.join(dfx[dfx[language] == 'Python'][cleaned]).split()
    j_words = ' '.join(dfx[dfx[language] == 'Java'][cleaned]).split()
    cpp_words = ' '.join(dfx[dfx[language] == 'C++'][cleaned]).split()
    other_words = ' '.join(dfx[dfx[language] == 'other'][cleaned]).split()
    all_words = ' '.join(dfx[cleaned]).split()
    
    return js_words, p_words, j_words, cpp_words, other_words, all_words

def create_bigrams(df):
    """returns a series of top 20 bigrams for each top language varible"""
    
    javascript_words, python_words, java_words, cpp_words, other_words, all_words = list_of_words_for_top_languages(df, language="is_top_language", cleaned="clean_lemmatized")

    top_20_bigrams = (pd.Series(nltk.ngrams(all_words, 2))
                      .value_counts()
                      .head(20))

    top_20_js_bigrams = (pd.Series(nltk.ngrams(javascript_words, 2))
                      .value_counts()
                      .head(20))

    top_20_p_bigrams = (pd.Series(nltk.ngrams(python_words, 2))
                      .value_counts()
                      .head(20))

    top_20_j_bigrams = (pd.Series(nltk.ngrams(java_words, 2))
                      .value_counts()
                      .head(20))

    top_20_cpp_bigrams = (pd.Series(nltk.ngrams(cpp_words, 2))
                      .value_counts()
                      .head(20))

    top_20_other_bigrams = (pd.Series(nltk.ngrams(other_words, 2))
                      .value_counts()
                      .head(20))
    return top_20_bigrams, top_20_js_bigrams, top_20_p_bigrams, top_20_j_bigrams, top_20_cpp_bigrams, top_20_other_bigrams


def plot_bigrams(df):
    """
    Plots the bigrams for the top 20 for each top language varible
    """
    
    top_20_bigrams, top_20_js_bigrams, top_20_p_bigrams, top_20_j_bigrams, top_20_cpp_bigrams, top_20_other_bigrams= create_bigrams(df)
    
    c="#84aae2"

    top_20_js_bigrams.sort_values().plot.barh(color=c, width=.9, figsize=(13, 10))
    plt.title('20 Most Frequently Occuring Java Script Bigrams')
    plt.ylabel('Bigram')
    plt.xlabel('# Occurences')
    # make the labels pretty
    ticks, _ = plt.yticks()
    labels = top_20_js_bigrams.reset_index()['index'].apply(lambda t: t[0] + ' ' + t[1])
    _ = plt.yticks(ticks, labels)
    plt.show()


    top_20_p_bigrams.sort_values().plot.barh(color=c, width=.9, figsize=(13, 10))
    plt.title('20 Most Frequently Occuring Python Bigrams')
    plt.ylabel('Bigram')
    plt.xlabel('# Occurences')
    # make the labels pretty
    ticks, _ = plt.yticks()
    labels = top_20_p_bigrams.reset_index()['index'].apply(lambda t: t[0] + ' ' + t[1])
    _ = plt.yticks(ticks, labels)
    plt.show()

    top_20_j_bigrams.sort_values().plot.barh(color=c, width=.9, figsize=(13,10))
    plt.title('20 Most Frequently Occuring Java Bigrams')
    plt.ylabel('Bigram')
    plt.xlabel('# Occurences')
    # make the labels pretty
    ticks, _ = plt.yticks()
    labels = top_20_j_bigrams.reset_index()['index'].apply(lambda t: t[0] + ' ' + t[1])
    _ = plt.yticks(ticks, labels)
    plt.show()

    top_20_cpp_bigrams.sort_values().plot.barh(color=c, width=.9, figsize=(13,10))
    plt.title('20 Most Frequently Occuring C++ Bigrams')
    plt.ylabel('Bigram')
    plt.xlabel('# Occurences')
    # make the labels pretty
    ticks, _ = plt.yticks()
    labels = top_20_cpp_bigrams.reset_index()['index'].apply(lambda t: t[0] + ' ' + t[1])
    _ = plt.yticks(ticks, labels)
    plt.show()

    top_20_bigrams.sort_values().plot.barh(color=c, width=.9, figsize=(13,10))
    plt.title('20 Most Frequently Occuring Bigrams')
    plt.ylabel('Bigram')
    plt.xlabel('# Occurences')
    # make the labels pretty
    ticks, _ = plt.yticks()
    labels = top_20_bigrams.reset_index()['index'].apply(lambda t: t[0] + ' ' + t[1])
    _ = plt.yticks(ticks, labels)
    plt.show()
    
    
def word_cloud(text):
    """Creates a word cloud for a given text"""
    plt.figure(figsize=(13, 13))

    cloud = WordCloud(background_color='white', height=1000, width=1000).generate(' '.join(text))

    plt.imshow(cloud)
    plt.axis('off')