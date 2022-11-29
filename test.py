import nltk
nltk.download('omw-1.4')
from textblob import Word, TextBlob
import pandas as pd
# Lemmatize a word
u = Word("was")
 
# apply lemmatization.
print("rocks :", u.lemmatize())
 
# create a Word object.
v = Word("corpora")
 
# apply lemmatization.
print("corpora :", v.lemmatize())
 
# create a Word object.
w = Word("better")
  
# apply lemmatization with
# parameter "a", "a" denotes adjective.
print("better :", w.lemmatize("a"))

# df = pd.read_excel('word_frequency.xlsx')
# df = df.dropna()
# df.insert(1, 'Lemma', df['Word'])

# print(df['Lemma'].transform(lambda w: Word(w).lemmatize()))


# print(df['Lemma'])
# print(lemma('playing'))
# print(nlp("sajdioasd")[0].lemma_)