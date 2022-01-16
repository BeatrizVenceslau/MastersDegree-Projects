import sys
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import ComplementNB

import nltk
from nltk.corpus import  wordnet
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

np.set_printoptions(threshold=np.inf)

d = {"HISTORY":0, "MUSIC":1, "GEOGRAPHY":2, "LITERATURE":3, "SCIENCE":4}
remove_words = ["the", "this", "in", "a"]

questions_train = []
questions_test = []
labels_train = []
labels_test = []
lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()

    tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

def get_tag_by_priority(labels):
    tags = ["HISTORY", "LITERATURE", "MUSIC", "SCIENCE", "GEOGRAPHY"]
    for tag in tags:
        if tag in labels:
            return tag
    return tags[0]

def process_number(word):
    if (word.isnumeric() or word[:-1].isnumeric()) and len(word) >= 3: return "data_format"
    else: return word

def runModel(train_file, test_file):
    with open(train_file, encoding="utf8") as f:
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

    # print("Trained data processed!")

    with open(test_file, encoding="utf8") as f:
            for line in f.readlines():
                for c in [",", ".", "?", "!", ":", "(", ")", "\"", ";", "&"]:
                    line = line.replace(c, "")

                splitted = [x.strip() for x in line.strip().split("\t")]

                if len(splitted) == 2:  # Real test
                    labels = []
                if len(splitted) == 3:  # Dev
                    labels = [splitted[0]]
                else:
                    labels = splitted[:-2]

                question = splitted[-2].replace("\"", "")
                answer = splitted[-1]

                word_list = word_tokenize(question + " " + answer)

                questions_test.append(' '.join(process_number(lemmatizer.lemmatize(w, get_wordnet_pos(w))) for w in word_list))
                labels_test.append(d[get_tag_by_priority(labels)])

    # print("Test data processed!")

    count_vector = CountVectorizer(lowercase=True, stop_words=remove_words)
    count_matrix = count_vector.fit_transform(questions_train)
    feat_dict = sorted(list(count_vector.vocabulary_.keys()))

    X_train = count_matrix.toarray()
    y_train = np.array(labels_train)

    count_matrix = count_vector.transform(questions_test)
    X_test = count_matrix.toarray()
    y_test = np.array(labels_test)

    cnb = ComplementNB()

    y_pred = cnb.fit(X_train, y_train).predict(X_test)

    convert_back = ["HISTORY", "MUSIC", "GEOGRAPHY", "LITERATURE", "SCIENCE"]
    for pred in y_pred:
        print(convert_back[pred])

    # print("%d / %d" % (X_test.shape[0] - (y_test != y_pred).sum(), X_test.shape[0]))
    # print("%f" % ((X_test.shape[0] - (y_test != y_pred).sum()) / X_test.shape[0] * 100))


    # with open("NB_wrongs.txt", "w") as f:
    #     for i in range(len(X_test)):
    #         if y_test[i] != y_pred[i]:
    #             f.write("-------------------------------------------------------------------\n")
    #             f.write(f"Question and answer: {[feat_dict[x] for x in range(len(X_test[i])) if X_test[i][x] == 1]}\n")
    #             f.write(f"Resposta Pretendida: {convert_back[y_test[i]]}\n")
    #             f.write(f"Resposta Obtida: {convert_back[y_pred[i]]}\n")
    #             f.write("-------------------------------------------------------------------\n\n")

if __name__ == "__main__":
    test_file = sys.argv[2]
    train_file = sys.argv[4]

    runModel(train_file, test_file)