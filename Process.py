from bs4 import BeautifulSoup

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from keras.preprocessing.sequence import pad_sequences
import re


class Process:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.stopWords = stopwords.words('english')
        tmp = self.stopWords.remove('not')
        self.lemmatizer = WordNetLemmatizer()

        self.contractionMapping = {"ll": "will", "ain't": "is not", "aren't": "are not", "can't": "can not",
                              "can't've": "can not have",
                              "'cause": "because", "could've": "could have", "couldn't": "could not",
                              "couldn't've": "could not have", "didn't": "did not", "doesn't": "does not",
                              "don't": "do not",
                              "hadn't": "had not", "hadn't've": "had not have", "hasn't": "has not",
                              "haven't": "have not",
                              "he'd": "he would", "he'd've": "he would have", "he'll": "he will",
                              "he'll've": "he will have",
                              "he's": "he is", "how'd": "how did", "how'd'y": "how do you", "how'll": "how will",
                              "how's": "how is", "I'd": "I would", "I'd've": "I would have", "I'll": "I will",
                              "I'll've": "I will have", "I'm": "I am", "I've": "I have", "i'd": "i would",
                              "i'd've": "i would have", "i'll": "i will", "i'll've": "i will have", "i'm": "i am",
                              "i've": "i have", "isn't": "is not", "it'd": "it would", "it'd've": "it would have",
                              "it'll": "it will", "it'll've": "it will have", "it's": "it is", "let's": "let us",
                              "ma'am": "madam", "mayn't": "may not", "might've": "might have", "mightn't": "might not",
                              "mightn't've": "might not have", "must've": "must have", "mustn't": "must not",
                              "mustn't've": "must not have", "needn't": "need not", "needn't've": "need not have",
                              "o'clock": "of the clock", "oughtn't": "ought not", "oughtn't've": "ought not have",
                              "shan't": "shall not", "sha'n't": "shall not", "shan't've": "shall not have",
                              "she'd": "she would", "she'd've": "she would have", "she'll": "she will",
                              "she'll've": "she will have", "she's": "she is", "should've": "should have",
                              "shouldn't": "should not", "shouldn't've": "should not have", "so've": "so have",
                              "so's": "so as", "this's": "this is", "that'd": "that would",
                              "that'd've": "that would have",
                              "that's": "that is", "there'd": "there would", "there'd've": "there would have",
                              "there's": "there is", "here's": "here is", "they'd": "they would",
                              "they'd've": "they would have", "they'll": "they will", "they'll've": "they will have",
                              "they're": "they are", "they've": "they have", "to've": "to have", "wasn't": "was not",
                              "we'd": "we would", "we'd've": "we would have", "we'll": "we will",
                              "we'll've": "we will have",
                              "we're": "we are", "we've": "we have", "weren't": "were not", "what'll": "what will",
                              "what'll've": "what will have", "what're": "what are", "what's": "what is",
                              "what've": "what have", "when's": "when is", "when've": "when have",
                              "where'd": "where did",
                              "where's": "where is", "where've": "where have", "who'll": "who will",
                              "who'll've": "who will have", "who's": "who is", "who've": "who have", "why's": "why is",
                              "why've": "why have", "will've": "will have", "won't": "will not",
                              "won't've": "will not have",
                              "would've": "would have", "wouldn't": "would not", "wouldn't've": "would not have",
                              "y'all": "you all", "y'all'd": "you all would", "y'all'd've": "you all would have",
                              "y'all're": "you all are", "y'all've": "you all have", "you'd": "you would",
                              "you'd've": "you would have", "you'll": "you will", "you'll've": "you will have",
                              "you're": "you are", "you've": "you have"}

    def predict(self, text):
        sentiment = ''
        if len(text) > 0:
            MAX_SEQUENCE_LENGTH = 300
            # Tokenize text
            print(self.tokenizer)
            x_test = pad_sequences(self.tokenizer.texts_to_sequences([text]), maxlen=MAX_SEQUENCE_LENGTH)
            # Predict
            score = self.model.predict([x_test])[0]
            if score < 0.35:
                sentiment = "Negative"
            elif 0.35 < score < 0.7:
                sentiment = "Neutral"
            else:
                sentiment = "Positive"
        else:
            sentiment = "Neutral"
        # print(score)
        # return { "text": text, "prediction" : {"score": float(score), "sentiment" : sentiment } }
        return sentiment

    def cleanText(self, ip):
        cleanedText = ''
        if len(ip) > 0:
            try:
                removeHtml = BeautifulSoup(ip, 'lxml').get_text().lower()
                removeMention = re.sub(r'@[A-Za-z0-9]+', '', removeHtml).strip().rstrip('.')
                removeUrl1 = re.sub('https?://[A-Za-z0-9./]+', '', removeMention)
                removeUrl2 = re.sub('[A-Za-z0-9./]+(com|net|org)', '', removeUrl1)
                # removeBOM = removeUrl.encode("ISO-8859-1").decode('utf-8-sig').replace(u"\ufffd", "?")
                # removeSpecialChar = re.sub("[^a-zA-Z']", " ", removeBOM).lower()
                removeSpecialChar = re.sub("[^a-zA-Z']", " ", removeUrl2)
                removeContraction = ' '.join([self.contractionMapping[t]
                                              if t in self.contractionMapping else t for t in removeSpecialChar.split(" ")])
                removeDoubleDotSpace = re.sub("[ ]+|'", ' ', re.sub('[.]+', '.', removeContraction))
                removeStopWords = ' '.join([x for x in word_tokenize(removeDoubleDotSpace) if x not in self.stopWords])
                extractNoun = self.lemmatizer.lemmatize(removeStopWords)
                cleanedText = extractNoun.strip()
            except Exception:
                cleanedText = ip
        return cleanedText

# import joblib
# prc = Process(joblib.load('./modelDump/final_model_cnn_v2.pkl'), joblib.load('./modelDump/tokenizer_X_train_v2.pkl'))
# print('----->'+prc.cleanText('I love India'))
# print('=====>>>>>>' + prc.predict(prc.cleanText('I love India')))