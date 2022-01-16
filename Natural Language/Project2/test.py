import nltk
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

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

word = "cats,"
print(lemmatizer.lemmatize(word, get_wordnet_pos(word)))