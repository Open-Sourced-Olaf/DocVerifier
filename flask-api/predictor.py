import random
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
import re

good_privacy = []
with open("good_privacy.txt", "r", encoding="utf8") as f:
  for line in f:
    good_privacy.append(line.rstrip())
bad_privacy = []
with open("bad_privacy.txt", "r", encoding="utf8") as f:
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

def predict(sentence):
    if gs_clf.predict([sentence]) == 1:
        return True ## it's a bad privacy sentence
    else:
        return False


def check_if_bad():
    with open("output.txt", encoding="utf8") as f:
        text = f.read()
    sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)
    bad = []
    good = []
    output = {}
    #sentences = [sentences]
    #sentence = [request.args.get('sentence')]
    for sentence in sentences:
        # print(sentence)
        # print("\n")
        if(len(sentence) > 100):
            if predict(sentence):
                good.append(sentence)
                print(sentence, 'sentence is bad')
            else:
                bad.append(sentence)
                print(sentence, 'sentence is good')
    return {'good': good, 'bad': bad}
