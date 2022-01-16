import nltk, json, math
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

english_stopwords = stopwords.words("english")
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

d = {"HISTORY":{"count_docs":0},
    "SCIENCE":{"count_docs": 0},
    "LITERATURE":{"count_docs": 0},
    "MUSIC":{"count_docs": 0},
    "GEOGRAPHY":{"count_docs": 0}}

with open("trainWithoutDev.txt", encoding="utf8") as f:
    for line in f.readlines():
        splitted = [x.strip() for x in line.strip().split("\t")]

        if len(splitted) == 3:
                labels = [splitted[0]]
        else:
            labels = splitted[:-2]

        question_answer = (splitted[-2].replace("\"", "") + " " + splitted[-1]).lower()

        word_list = [lemmatizer.lemmatize(x, get_wordnet_pos(x)) for x in word_tokenize(question_answer) if x.isalpha() and x not in english_stopwords]

        counts = dict()
        for word in word_list:
            counts[word] = counts.get(word, 0) + 1
        
        for label in labels:
            doc = d[label]
            doc["count_docs"] += 1
            for word in counts:
                if word in doc:
                    l = doc[word]
                    l[0] += counts.get(word)
                    l[1] += 1
                else:
                    l = [counts.get(word), 1]
                doc[word] = l


y_pred = []
y_test = []

tokens_test = []
idf_tokens = []

with open("dev_clean.txt", encoding="utf8") as f:
    correct = 0
    total = 0
    for line in f.readlines():
        splitted = [x.strip() for x in line.strip().split("\t")]

        if len(splitted) == 3:
                labels = [splitted[0]]
        else:
            labels = splitted[:-2]

        y_test.append(get_tag_by_priority(labels))

        question_answer = (splitted[-2].replace("\"", "") + " " + splitted[-1]).lower()

        word_list = [lemmatizer.lemmatize(x, get_wordnet_pos(x)) for x in word_tokenize(question_answer) if x.isalpha() and x not in english_stopwords]

        counts = dict()
        for word in word_list:
            counts[word] = counts.get(word, 0) + 1

        tokens_test.append(list(counts.keys()))

        maxScore = 0
        bestLabel = ""
        best_idf = []
        for doc_type in d:
            category = d[doc_type]
            currentScore = 0

            idf = []

            for word in counts:
                value = 0
                if word in category:
                    value = category[word][0] * math.log10(category["count_docs"] / category[word][1])
                idf.append(value)
                currentScore += value

            if currentScore > maxScore:
                maxScore = currentScore
                bestLabel = doc_type
                best_idf = idf

        idf_tokens.append(best_idf)
        y_pred.append(bestLabel)

        if bestLabel in labels:
            correct += 1
        total += 1

    print(f"{correct}/{total}")
    print(f"{correct/total * 100}")
                

with open("TF_wrongs.txt", "w") as f:
    for i in range(500):
        if y_test[i] != y_pred[i]:
            f.write("-------------------------------------------------------------------\n")
            f.write(f"Tokens: {tokens_test[i]}\n")
            f.write(f"Idf Score: {idf_tokens[i]}\n")
            f.write(f"Resposta Pretendida: {y_test[i]}\n")
            f.write(f"Resposta Obtida: {y_pred[i]}\n")
            f.write("-------------------------------------------------------------------\n\n")