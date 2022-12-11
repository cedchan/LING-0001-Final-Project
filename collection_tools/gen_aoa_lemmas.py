''' 
Takes raw dictionary of AoA values and lemmatizes each item, then returns a new CSV
file containing that information for later analysis.
'''

import spacy
import pandas as pd

lemmatizer = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

df = pd.read_excel('reference/aoa/aoa_raw.xlsx')
df = df.dropna()
df.insert(1, 'Lemma', df['Word'])

df['Lemma'] = df['Lemma'].map(lambda w: lemmatizer(w)[0].lemma_)
df.to_csv('reference/aoa/aoa_lemmas.csv')