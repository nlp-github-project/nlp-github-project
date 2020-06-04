# NLP Project

For this project, you will be scraping data from GitHub repository README files. The goal will be to build a model that can predict what programming language a repository is, given the text of the README file.


## Executive Summary:

* Acquired nearly 800 README’s from Github’s most starred repos
* Broke the programming languages into 5 groups:
    * Java
    * Python
    * JavaScript
    * C++
    * Other (for the other languages)

* Found no significant patterns to help distinguish between programming languages
* Using a machine learning algorithm called `Naive Bayes Multinomial` classifier we were able to predict the programming language with 71% accuracy

## How to Reproduce:
- Have python installed through anaconda
- You may need to install:
    1. WordCloud
    2. sentence tokenizer for nltk
- First clone this repo
- env.py file
- Make a github personal access token.
     1. Go here and generate a personal access token https://github.com/settings/tokens
        You do _not_ need select any scopes, i.e. leave all the check boxes unchecked
     2. Save it in your env.py file under the variable `github_token`
     3. In another variable, called `github_username`, store your github username as a string.
-  Run `repo_acquisition.py` in command line. This will will create a csv file called `repo_names.csv`. The repo's collected will be the same as the ones in the report.
-  Run `acquire.py` module in command line. This will take the `repo_names.csv`, and create a new `data.json` file, which can be read using Pandas for analysis. This file will be needed to replicate the notebook.    
     
## Hypothesis
- $𝐻_0$ : There is no significant difference between the mean word count of each language when compared with the mean word count of the group.
- $𝐻_𝑎$ : There is a significant difference between the mean word count of each language when compared with the mean word count of the group.


## Deliverables

- A well-documented jupyter notebook that contains your analysis
- One or two google slides suitable for a general audience that summarize your findings. Include a well-labelled visualization in your slides.

The link to our presentation can be found [here](https://docs.google.com/presentation/d/1cf5VWCoOLJk2amwf6M1-HZqy-p1IJzpVA43AyRPFsf0/edit?usp=sharing)
    
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

## Technical Skills
- Python (including internal and third party libraries)
- Web Scraping/ API
- Hypothesis testing
- natural language processing
- Classification modeling

## Data Source for project:
- githubs most starred repos
