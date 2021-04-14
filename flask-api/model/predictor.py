import random
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier

import re #import regex


good_privacy = []
with open("datasets/good_privacy.txt", "r", encoding="utf8") as f:
    for line in f:
        good_privacy.append(line.rstrip())
bad_privacy = []
with open("datasets/bad_privacy.txt", "r", encoding="utf8") as f:
    for line in f:
        bad_privacy.append(line.rstrip())

combined_data = []
for item in good_privacy:
    combined_data.append([item, 0])
for item in bad_privacy:
    combined_data.append([item, 1])
random.shuffle(combined_data)

training_data = []
training_target = []
for item in combined_data:
    training_data.append(item[0])
    training_target.append(item[1])

text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB()),
                     ])

text_clf = text_clf.fit(training_data, training_target)

parameters = {'vect__ngram_range': [(1, 1), (1, 2)],
              'tfidf__use_idf': (True, False),
              'clf__alpha': (1e-2, 1e-3),
              }
gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1)
gs_clf = gs_clf.fit(training_data, training_target)


def predict_nb(sentence):
    if gs_clf.predict([sentence]) == 1:
        return True  # it's a bad privacy sentence
    else:
        return False

text_clf_svm = Pipeline([('vect', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      ('clf-svm', SGDClassifier(loss='hinge', penalty='l2',
                                        alpha=1e-3, random_state=42))
])
text_clf_svm = text_clf_svm.fit(training_data, training_target)

def predict_svm(sentence):
    if text_clf_svm.predict([sentence]) == 1:
        return True  # it's a bad privacy sentence
    else:
        return False