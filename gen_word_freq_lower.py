import pandas as pd
import json

df = pd.read_excel('reference/word_frequency/SUBTLEXus_raw.xlsx')
df = df.dropna()
df['Word'] = df['Word'].str.lower()

word_freq = df[['Word', 'SUBTLWF']]
wf_dict = word_freq.to_dict(orient='split')
wf_data = dict(wf_dict.get('data'))

with open('reference/word_frequency/subtlexus_lower.json', mode='w', encoding='utf-8') as f:
    json.dump(wf_data, f, indent=4) 