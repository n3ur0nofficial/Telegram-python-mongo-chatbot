import spacy
from spacy import *


class Tokenizing:
    def tokenizing(chat_text):
        nlp = spacy.load('en')
        print('Chat text is:'.format(chat_text))
        cht_txt = nlp(chat_text)
        print(cht_txt)
        for ent in cht_txt.ents:
            result = ent.text
            print('Answer is'.format(result))
            return result

pass
