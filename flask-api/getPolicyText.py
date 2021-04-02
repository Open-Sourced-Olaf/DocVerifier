from bs4 import BeautifulSoup
import re
import requests
import nltk

def getPolicies(url_link):
  source = requests.get(url_link).text
  soup = BeautifulSoup(source, 'lxml')
  policies=soup.find('body')

  txt = policies.text
  words = set(nltk.corpus.words.words())
  return " ".join(w for w in nltk.wordpunct_tokenize(txt) \
          if w.lower() in words or not w.isalpha())