import pandas as pd
import numpy as np

from requests import get
from bs4 import BeautifulSoup
import os

import time


def scrape_repo_names():
    repo_names = []

    # Loop to get repo names
    for page_number in range(1,80):
        url = f"https://github.com/search?p={page_number}&q=stars%3A%3E0&s=stars&type=Repositories"
        headers = {'User-Agent': 'Codeup Bayes Data Science'}
        response = get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        repos = soup.find_all('a', class_='v-align-middle')
        time.sleep(20)

        
        for repo_number in range(len(repos)):
            repo_name = repos[repo_number]["href"].replace("/", '', 1)
            repo_names.append(repo_name)

    return repo_names

def store_repo_names(repo_names):

    s = pd.DataFrame(repo_names, columns=["repo_name"])
    s.to_csv("repo_names.csv")

# ----------- #
# Script Code #
# ----------- #
 
repo_names = scrape_repo_names()
store_repo_names(repo_names)