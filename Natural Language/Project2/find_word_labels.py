import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def process_number(word):
    if (word.isnumeric() or word[:-1].isnumeric()) and len(word) >= 3: return "data_format"
    else: return word

with open("trainWithoutDev.txt", encoding="utf8") as f:
    fp = dict()
    fp["HISTORY"] = 0
    fp["MUSIC"] = 0
    fp["LITERATURE"] = 0
    fp["SCIENCE"] = 0
    fp["GEOGRAPHY"] = 0

    lemmatizer = WordNetLemmatizer()
    word = "book"
    word = process_number(lemmatizer.lemmatize(word, get_wordnet_pos(word)))

    print(word)

    for line in f.readlines():
        for c in [",", ".", "?", "!", ":", "(", ")", "\"", ";", "&"]:
                line = line.replace(c, "")

        splitted = [x.strip() for x in line.strip().split("\t")]

        if len(splitted) == 3:
                labels = [splitted[0]]
        else:
            labels = splitted[:-2]

        question_answer = (splitted[-2].replace("\"", "") + " " + splitted[-1]).lower()

        word_list = [process_number(lemmatizer.lemmatize(x, get_wordnet_pos(x))) for x in word_tokenize(question_answer)]
        # if "PBS" in line:
        #     print(word_list)

        if word in word_list:
            for l in labels:
                fp[l] = fp.get(l, 0) + 1
    
    for label in fp:
        print(f"{label}: {fp.get(label, 0)}")