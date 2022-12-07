import pandas as pd
import time
import re
import os
import json
from datetime import datetime
from collections import Counter

import spacy
import benepar

from tools import text_analysis as ta
from tools import const

benepar.download('benepar_en3')

nlp = spacy.load('en_core_web_md')
if spacy.__version__.startswith('2'):
    nlp.add_pipe(benepar.BeneparComponent("benepar_en3"))
else:
    nlp.add_pipe('benepar', config={'model': 'benepar_en3'})

results = pd.DataFrame([])

# TED Mode
#  - 'combinations': Averages the TED of every pair of sentences in a doc
#  - 'adjacent': Averages the TED of a sentence and the next sentence in a doc
ted_mode = 'adjacent'
# AoA Mode: If word is not in AoA list and multiple lemma matches exist
#  - 'max': Chooses max of lemma matches
#  - 'min': Chooses min of lemma matches
#  - 'avg': Averages lemma matches
aoa_mode = 'min'
log = ""

for i, file in enumerate(os.scandir('data/text_jsons/')):
    # if i == 2: break
    
    file_time = time.perf_counter()
    file_name = re.sub('\.json$', '', file.name)
    with open(file, encoding='utf-8') as f:
        metadata = json.load(f)
    text = metadata['text']
    text = text.replace('\n', ' ').strip()
    text = re.sub('\s{2,}', ' ', text)
    
    try:
        doc = nlp(text)
    except ValueError:
        error_text = f"ValueError in '{file_name}'. Likely exists too long sentence. Skipping."
        log += error_text + '\n'
        continue
    except:
        error_text = f"Some other error occured in '{file_name}'. Skipping."
        log += error_text + '\n'
        continue

    sents = list(doc.sents)

    num_tokens = len(doc)
    num_sents = len(sents)
    ted_sum = 0

    features = Counter({x : 0 for x in const.MAST_FEATURES_LST})
    uniq_words = set()

    for sent in sents:
        benepar_time = time.perf_counter()
        b_features, b_max_features = ta.benepar_analysis(sent)
        features.update(b_features)
        for feature in b_max_features:
            features[feature] = max(features.get(feature), b_max_features[feature])
        benepar_time = time.perf_counter() - benepar_time

        spacy_time = time.perf_counter()
        s_features, s_max_features, sent_vocab = ta.spacy_analysis(sent, uniq_words, aoa_mode)
        features.update(s_features)
        for feature in s_max_features:
            features[feature] = max(features.get(feature), s_max_features[feature])
        uniq_words.update(sent_vocab)
        spacy_time = time.perf_counter() - spacy_time

    # TREE EDIT DISTANCE
    ted_time = time.perf_counter()
    ted_avg = ta.ted_analysis(ted_mode, sents);
    ted_time = time.perf_counter() - ted_time

    summary = {
        # File-level
        'date' : metadata['date'],
        'pres_name' : metadata['pres_name'],
        'byline' : metadata['byline'],
        'title' : metadata['title'],

        # Performance time
        'benepar_analysis_time' : benepar_time,
        'spacy_analysis_time' : spacy_time,
        'tree_edit_distance_time' : ted_time,
        'total_file_analysis_time' : time.perf_counter() - file_time,

        # Doc-level
        'num_tokens' : num_tokens,
        'num_sentences' : num_sents, 
        # 'avg_ted_adj' : ted_avg_adj,
        # 'avg_ted_comb' : ted_avg_comb,
        f'avg_tree_edit_dist_{ted_mode}' : ted_avg,

        # Benepar
        'avg_node_depth' : features['depth_sum'] / num_tokens, 
        'max_node_depth' : features['max_depth'], # Equivalent to tree height
        'avg_node_clause_depth' : features['clause_depth_sum'] / num_tokens,
        'max_node_clause_depth' : features['max_clause_depth'],
        'avg_clause_length' : features['clause_length_sum'] / features['num_clauses'],
        'clauses_per_sent' : features['num_clauses'] / num_sents, 
        'sbars_per_sent' : features['num_sbar'] / num_sents,
        'pronouns_per_sent' : features['pronoun_sum'] / num_sents,
        'pronouns_per_clause' : features['pronoun_sum'] / features['num_clauses'],
        'pronoun_prop_of_leaf_nps' : features['pronoun_sum'] / features['num_leaf_nps'],
        'avg_num_np_modifiers' : features['np_leaf_sum'] / features['num_nps'],
        'loose_parataxis_per_sent' : features['paratactic_sum'] / num_sents,
        'root_parataxis_per_sent_strict' : features['root_parataxis_strict'] / num_sents,
        'root_parataxis_per_sent_loose' : features['root_parataxis_loose'] / num_sents,
        'num_unk' : features['num_unk'],

        # spaCy
        'num_words' : features['num_words'],
        'avg_dependency_distance' : features['dep_dist_sum'] / features['num_words'],
        'max_dependency_distance' : features['max_dep_dist'],
        'avg_sentence_length_by_tok' : num_tokens / num_sents, 
        'avg_sentence_length_by_word' : features['num_words'] / num_sents,
        'avg_words_before_root' : features['words_before_root_sum'] / num_sents,
        'num_uniq_words' : len(uniq_words), 
        'proportion_uniq' : len(uniq_words) / features['num_words_no_nums'],
        'stop_words_per_clause' : features['num_stop_words'] / features['num_clauses'],
        'stop_words_per_sentence' : features['num_stop_words'] / num_sents,
        f'avg_aoa_{aoa_mode}' : features['aoa_sum'] / features['aoa_count'],
        f'avg_aoa_uniq_{aoa_mode}' : features['aoa_uniq_sum'] / features['aoa_uniq_count'],
        f'avg_stopless_aoa_{aoa_mode}' : features['aoa_stopless_sum'] / features['aoa_stopless_count'],
        f'avg_stopless_aoa_uniq_{aoa_mode}' : features['aoa_stopless_uniq_sum'] / features['aoa_stopless_uniq_count'],
        'avg_word_freq' : features['wf_sum'] / features['wf_count'],
        'avg_word_freq_uniq' : features['wf_uniq_sum'] / features['wf_uniq_count'],
        'avg_word_freq_stopless' : features['wf_stopless_sum'] / features['wf_stopless_count'],
        'avg_word_freq_stopless_uniq' : features['wf_stopless_uniq_sum'] / features['wf_stopless_uniq_count'],
    }      
    
    results[file_name] = summary
    
print("Error Log:")
print(log)
pd.set_option('display.precision', 2)
print(results)
results.to_csv(f"results/{datetime.now().strftime('%m-%d-%Y_%H-%M')}.csv")