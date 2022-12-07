''' 
Contains tools used in spacy_analysis. Primarily involves information that is 
collected exclusively by spacy (is_stop, like_num, etc.), or dependency relationships.
'''

import spacy
from tools import const

lemmatizer = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

def lemmatize(word: str):
    '''
    Finds the lemma of a given word, taken in as a string. Input is assumed to be 
    one word. If spaCy parses the input as more than one word, the lemma of the 
    first word is returned.

    Args:
        word: Word to find lemma of

    Returns:
        Lemma of word
    '''
    return lemmatizer(word)[0].lemma_

def aoa_of(word: str, aoa_mode: str):
    '''
    Finds the AoA (age of acquisition) of a given word. The AoA dictionary used
    includes the lemmas or certain forms of different words based on frequency and other 
    factors, meaning a match is not guaranteed. If an exact match is not found, the word's 
    lemma is searched for in the dictionary. If that isn't found, the word's lemma
    is searched for in a generated dictionary of the lemmas of original dictionary entries.
    This opens up the potential for multiple matches. The AoA mode determines whether the
    maximum, minimum, or average AoA should be returned.

    Args:
        word: Word to find the AoA of
        aoa_mode: 'max', 'min', or 'avg'—method of resolving multiple AoA matches
    
    Returns:
        AoA if found, -1 if not
    '''
    aoa_df = const.AOA_DF  
    search = aoa_df[aoa_df['Word'] == word]['Rating.Mean']
    if len(search) == 1:
        return float(search)
    
    lemma_search = aoa_df[aoa_df['Word'] == lemmatize(word)]['Rating.Mean']
    if len(lemma_search) == 1:
        return float(lemma_search)
    
    lemmas = aoa_df[aoa_df['Lemma'] == lemmatize(word)]['Rating.Mean']
    if len(lemmas) == 0:
        return -1
    elif len(lemmas) == 1:
        return float(lemmas)
    elif aoa_mode == 'avg':
        return sum(lemmas) / len(lemmas)
    elif aoa_mode == 'max':
        return max(lemmas)
    elif aoa_mode == 'min':
        return min(lemmas)
    
    return -1