'''
Contains tools for analyzing TED (tree edit distance), using the APTED
library.
'''

import re

from apted import APTED
from apted.helpers import Tree

def apted_format(parse_str):
    '''
    Cleans a given parse string, as formatted by benepar/spaCy (i.e., S-expression)
    and reformats it to fit the APTED requirements. Assumes correct formatting from 
    benepar.

    Args:
        parse_str: String to clean and reformat

    Returns:
        Reformatted string
    '''
    parse_str = re.sub('\(([^ ]+) [^ \(\)]+?\)', '(\g<1>)', parse_str)
    parse_str = parse_str.replace(' ', '')
    parse_str = parse_str.replace('(', '{')
    parse_str = parse_str.replace(')', '}')
    return parse_str

def ted_of(sent1, sent2):
    '''
    Finds the TED (tree edit distance) between two spaCy sentences
    with the benepar "parse_string" attribute. All operations are equally
    weighted.

    Args:
        sent1: The first sentence
        sent2: The second sentence
    
    Returns:
        The numerical TED
    '''
    tree1 = Tree.from_text(apted_format(sent1._.parse_string))
    tree2 = Tree.from_text(apted_format(sent2._.parse_string))

    apted = APTED(tree1, tree2, )
    ted = apted.compute_edit_distance()
    return ted