''' Contains useful constants for text analysis. '''

import json
import pandas as pd
import re

CLAUSE_TAGS = ['S', 'SBARQ', 'SINV'] # Not included: 'SQ', 'SBAR'
CLAUSE_RE = re.compile('(' + '/|'.join(CLAUSE_TAGS) + ')')
PRONOUN_TAGS = ['PRP', 'PRPS']

BENEPAR_FEATURES_LST = ['num_clauses', 'num_sbar', 'num_unk', 'depth_sum', 'clause_depth_sum', 'pronoun_sum', 
        'num_leaf_nps', 'num_nps', 'np_leaf_sum', 'clause_length_sum', 'paratactic_sum', 
        'root_parataxis_strict', 'root_parataxis_loose']
SPACY_FEATURES_LST = ['dep_dist_sum', 'num_words', 'words_before_root_sum', 'uniq_words', 
        'num_words_no_nums', 'num_stop_words', 'aoa_sum', 'aoa_count', 
        'aoa_stopless_sum', 'aoa_stopless_count', 'aoa_uniq_sum', 'aoa_uniq_count',
        'aoa_stopless_uniq_sum', 'aoa_stopless_uniq_count', 'wf_sum', 'wf_count', 
        'wf_stopless_sum', 'wf_stopless_count', 'wf_uniq_sum', 'wf_uniq_count',
        'wf_stopless_uniq_sum', 'wf_stopless_uniq_count']
MAST_FEATURES_LST = ['num_clauses', 'num_sbar', 'num_unk', 'depth_sum', 'clause_depth_sum', 
        'pronoun_sum', 'num_leaf_nps', 'num_nps', 'np_leaf_sum', 'clause_length_sum', 
        'paratactic_sum', 'root_parataxis_strict', 'root_parataxis_loose', 'dep_dist_sum', 
        'num_words', 'words_before_root_sum', 'uniq_words', 'num_words_no_nums', 'num_stop_words', 
        'aoa_sum', 'aoa_count', 'aoa_stopless_sum', 'aoa_stopless_count', 'aoa_uniq_sum', 
        'aoa_uniq_count', 'aoa_stopless_uniq_sum', 'aoa_stopless_uniq_count', 'wf_sum', 
        'wf_count', 'wf_stopless_sum', 'wf_stopless_count', 'wf_uniq_sum', 'wf_uniq_count',
        'wf_stopless_uniq_sum', 'wf_stopless_uniq_count', 'max_clause_depth',
        'max_depth', 'max_dep_dist']

AOA_DF = pd.read_csv('reference/aoa/aoa_lemmas.csv')
with open('reference/word_frequency/subtlexus_lower.json', encoding='utf-8') as f:
    WF_DICT = json.load(f)