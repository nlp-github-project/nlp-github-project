# NLP Project

For this project, you will be scraping data from GitHub repository README files. The goal will be to build a model that can predict what programming language a repository is, given the text of the README file.

## Executive Summary:

* We found that the majority of the repo's we acquired were written in JavaScript. The second most popular language was Python, and the third was Java.

* To help improve the accracy scores of the models, we grouped languages that were not in the top 5 as `other`. 

* We tested several models, and found that Decision Tree Classifier with a `max_depth` of 5, was the best model, with an accuracy score of ~65%. 


## Deliverables

A well-documented jupyter notebook that contains your analysis
One or two google slides suitable for a general audience that summarize your findings. Include a well-labelled visualization in your slides.

## Project Plan

**Acquisition, Prep, and Initial Exploration**
* Fetch Data from local cache
* Handle Missing Values
* Remove/repair erroneous data
* Look at shape of data
* normalize data by removing non ASCII characters
* tokenize words
* stem and lemmatize words
* remove stop words

**Exploration**
* Answer the following questions:
    * What are the most common words in READMEs?
    * What does the distribution of IDFs look like for the most common words?
    * Does the length of the README vary by programming language?
    * Do different programming languages use a different number of unique words?


**Modeling**:

* Build a model that can predict what programming language a repository is, based on the text of the README file

