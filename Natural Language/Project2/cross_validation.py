import numpy as np
from numpy.core.numeric import cross
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import ComplementNB
from sklearn.model_selection import cross_val_score

import nltk
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')
from nltk.stem import WordNetLemmatizer

remove_words = ["the", "this", "in", "a"]

questions_train = []
labels_train = []
lemmatizer = WordNetLemmatizer()
d = {"HISTORY":0, "MUSIC":1, "GEOGRAPHY":2, "LITERATURE":3, "SCIENCE":4}

def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()

    tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

def get_tag_by_priority(labels):
    tags = ["HISTORY", "LITERATURE", "MUSIC", "SCIENCE", "GEOGRAPHY"]
    for tag in tags:
        if tag in labels:
            return tag

def process_number(word):
    if (word.isnumeric() or word[:-1].isnumeric()) and len(word) >= 3: return "data_format"
    else: return word

with open("trainWithoutDev.txt", encoding="utf8") as f:
        for line in f.readlines():
            for c in [",", ".", "?", "!", ":", "(", ")", "\"", ";", "&"]:
                line = line.replace(c, "")

            splitted = [x.strip() for x in line.strip().split("\t")]

            if len(splitted) == 3:
                labels = [splitted[0]]
            else:
                labels = splitted[:-2]

            question = splitted[-2].replace("\"", "")
            answer = splitted[-1]

            word_list = word_tokenize(question + " " + answer)
            
            questions_train.append(' '.join(process_number(lemmatizer.lemmatize(w, get_wordnet_pos(w))) for w in word_list))
            labels_train.append(d[get_tag_by_priority(labels)])

print("Trained data processed!")

count_vector = CountVectorizer(lowercase=True, stop_words=remove_words)
count_matrix = count_vector.fit_transform(questions_train)
feat_dict = sorted(list(count_vector.vocabulary_.keys()))

X_train = count_matrix.toarray()
y_train = np.array(labels_train)
cnb = ComplementNB()

scores = cross_val_score(cnb, X_train, y_train, cv=5, scoring="accuracy")
print(scores)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))