''' Contains the 3 main text analysis functions for benepar, spacy, and TED analysis. '''

import re
from lxml import etree
from collections import Counter

from math import comb
from itertools import combinations

from tools import misc_tools, spacy_tools, benepar_tools, ted_tools, const


def benepar_analysis(sent):
    '''
    Extracts features from a given sentence based on constituency analysis and other 
    related information from a parsing by the benepar library. Generally has information
    to do with clauses and syntax tree shape.

    Args:
        sent: spaCy sentence to be analyzed (i.e., a Span of a Doc)

    Returns:
        features, max_features
        features: a Counter object that contains features that are summed across sentences
        max_features: a dictionary containing features for which only the maximum is stored 
        across sentences
    '''
    features = Counter(
        {x: 0 for x in const.BENEPAR_FEATURES_LST})  # initialize to 0
    max_features = {
        'max_clause_depth': 0,
        'max_depth': 0,
    }

    paratactic_sum_local = 0
    max_clause_depth = 0

    xml = misc_tools.sexp_to_xml(sent._.parse_string)
    root = etree.fromstring(xml)
    tree = etree.ElementTree(root)

    features['root_parataxis_loose'] = benepar_tools.get_root_parataxis_loose(
        root)
    features['root_parataxis_strict'] = benepar_tools.get_root_parataxis_strict(
        root)
    features['num_sbar'] = benepar_tools.get_num_sbar(root)
    features['pronoun_sum'] = benepar_tools.get_pronoun_sum(root)
    features['num_unk'] = benepar_tools.get_num_unk(root)

    for e in root.iter():
        tag = e.tag
        if tag in const.CLAUSE_TAGS:
            features['num_clauses'] += 1
            features['clause_length_sum'] += sum(int(not (d.tag.startswith(
                'PUNCT-') and bool(d.text))) for d in e.iterdescendants())

            paratactic_sum_local += benepar_tools.get_parataxis_loose(e)
        elif e.tag == 'NP':
            is_leaf_np = True
            np_text = ""
            for c in e.iterdescendants():
                if c.text:
                    # ignore determiners and punctuation
                    if not (c.tag.startswith('PUNCT-') or c.tag == 'DT'):
                        np_text += c.text + " "
                        features['np_leaf_sum'] += 1
                else:
                    is_leaf_np = False

            if np_text:
                features['num_nps'] += 1
                features['words_before_np_root_sum'] += spacy_tools.words_before_root(
                    np_text)
                if is_leaf_np:
                    features['num_leaf_nps'] += 1

        if e.text:
            path = tree.getpath(e)

            depth = len(re.findall('/', path))
            # Number of times '/' appears, excluding first
            features['depth_sum'] += depth
            max_features['max_depth'] = max(max_features['max_depth'], depth)

            clause_depth = len(const.CLAUSE_RE.findall(path))
            # if clause_depth > 6:
            #     print(' '.join([x for x in root.itertext()]))
            features['clause_depth_sum'] += clause_depth
            max_clause_depth = max(max_clause_depth, clause_depth)

    features['paratactic_sum'] = max(1, paratactic_sum_local)
    max_features['max_clause_depth'] = max_clause_depth
    features['max_clause_depth_sum'] = max_clause_depth

    return features, max_features


def spacy_analysis(sent, uniq_words: set, aoa_mode: str):
    '''
    Extracts features from a given sentence based on spaCy dependency and POS (part of speech) tagging.
    Also collects information regarding word frequence and age of acquisition of sentence vocabulary.

    Args:
       sent: spaCy sentence to be analyzed (i.e., a Span of a Doc)
       uniq_words: a set of the entire Doc's unique words (as far as is known at the time it is passed in)
       aoa_mode: 'min', 'max', or 'avg'—how to resolve a particular case explained in depth in the method 
       spacy_tools.aoa_of

    Returns:
        features, max_features, uniq_words
        features: a Counter object that contains features that are summed across sentences
        max_features: a dictionary containing features for which only the maximum is stored 
        across sentences
        uniq_words: an updated set of uniq_words (i.e., including new words in the sentence)
    '''
    features = Counter({x: 0 for x in const.SPACY_FEATURES_LST})
    max_features = {
        'max_dep_dist': 0,
    }

    features['num_stop_words'] = sum(int(token.is_stop) for token in sent)

    for token in sent:
        if not (token.is_punct or token.is_space):
            features['num_words'] += 1
            dep_dist = abs(token.head.i - token.i)
            features['dep_dist_sum'] += dep_dist
            max_features['max_dep_dist'] = max(
                dep_dist, max_features['max_dep_dist'])

            if (wf := const.WF_DICT.get(token.lower_)) is not None:
                features['wf_sum'] += wf
                features['wf_count'] += 1
                if not token.is_stop:
                    features['wf_stopless_sum'] += wf
                    features['wf_stopless_count'] += 1

            if (aoa := spacy_tools.aoa_of(token.lower_, aoa_mode)) != -1:
                features['aoa_sum'] += aoa
                features['aoa_count'] += 1
                if not token.is_stop:
                    features['aoa_stopless_sum'] += aoa
                    features['aoa_stopless_count'] += 1

            if token.i < sent.root.i:
                features['words_before_root_sum'] += 1

            if not (token.like_num):
                if not (token.lower_ in uniq_words):
                    uniq_words.add(token.lower_)

                    if wf is not None:
                        features['wf_uniq_sum'] += wf
                        features['wf_uniq_count'] += 1
                        if not token.is_stop:
                            features['wf_stopless_uniq_sum'] += wf
                            features['wf_stopless_uniq_count'] += 1

                    if aoa != -1:
                        features['aoa_uniq_sum'] += aoa
                        features['aoa_uniq_count'] += 1
                        if not token.is_stop:
                            features['aoa_stopless_uniq_sum'] += aoa
                            features['aoa_stopless_uniq_count'] += 1

                features['num_words_no_nums'] += 1
    return features, max_features, uniq_words


def ted_analysis(ted_mode: str, sents):
    '''
    Finds the average TED (tree edit distance) of all sentences in a document. (Note:
    Should therefore be run at a Doc and not sentence level.) Chooses between calculating 
    the TED of every pair of sentences (nCr(# sents, 2) calculations) or every sentence and
    the sentence that follows it (# sents - 1 calculations).

    Args:
        ted_mode: 'adjacent' or 'combinations'—how to choose pairs of sentences
        sents: list of spaCy sentences. (Note: Must be a list)

    Returns:
        Average TED
    '''
    num_sents = len(sents)
    ted_sum = 0
    if ted_mode == 'adjacent':
        for i in range(num_sents - 1):
            ted_sum += ted_tools.ted_of(sents[i], sents[i + 1])
        ted_avg = ted_sum / (num_sents - 1)
    elif ted_mode == 'combinations':
        for sent1, sent2 in combinations(sents, 2):
            ted_sum += ted_tools.ted_of(sent1, sent2)
        ted_avg = ted_sum / comb(num_sents, 2)
    else:
        print('Invalid ted_mode:', ted_mode)
        ted_avg = -1

    return ted_avg
