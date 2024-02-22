import re
from spacy.matcher import PhraseMatcher
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC
import nltk
from nltk.corpus import stopwords
import re, string
import unidecode

nltk.download('stopwords')


def get_words(directory, file_name):
    """
    :param directory: folder where the file is in
    :param file_name: file name in specific directory
    :return: content of file
    """
    filename = f'entities/data/{directory}/{file_name}'
    with open(filename, 'r', encoding="utf-8") as file:
        words = [line.rstrip() for line in file]
    return words

def convert_dict_values_in_one_string(value):
    """
    :param value: dict you want to convert values in str
    :return: str with all dict values
    """
    return " ".join(f'{v}' for v in value.values()).lower().replace('-', '')

def get_number_in_string(text: str):
    """
    :param text: string that wants to get the number inside
    :return: number contained in string
    """
    value = int(re.search(r"[\d]+", text).group()) if text else 0
    return value

def key_words_count(nlp, key_words, words):
    """
    :param nlp: spacy loaded words
    :param key_words: text or word to be validate
    :param words: words with key words
    :return: bring the quantity of key words that exists in text
    """
    doc = nlp(key_words)
    phrase_patterns = [nlp(text) for text in words]
    matcher = PhraseMatcher(nlp.vocab)
    matcher.add('words', None, *phrase_patterns)
    matches = matcher(doc)
    return len(matches)

def predict_title(title):
    df = pd.read_csv(f"entities/data/invalid_titles/linkedin titles valid_invalid - Titles.csv")
    df['valid_id'] = df['valid'].factorize()[0]
    X_train, X_test, y_train, y_test = train_test_split(df['titles'], df['valid'], random_state=0)

    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(X_train)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    clf = LinearSVC().fit(X_train_tfidf, y_train)
    pred = clf.predict(count_vect.transform([title]))
    output = True if pred[0] == 'valid' else False
    return output

def preprocess(text):
    text = text.lower()
    text = text.strip()
    text = unidecode.unidecode(text)
    text = re.compile('<*?:>').sub('', text)
    text = re.compile('[%s]' % re.escape(string.punctuation.replace('#', '').replace('/', ''))).sub(' ', text)
    text = re.sub('\s+', ' ', text)
    text = re.sub(r'\d', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def stopword(string):
    lst_stopwords = stopwords.words('english') + stopwords.words('portuguese')
    a = [i for i in string.split() if i not in lst_stopwords]
    return ' '.join(a)

def finalpreprocess(string):
    return preprocess(stopword(string))