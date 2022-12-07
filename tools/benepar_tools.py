''' 
Contains functions for use in benepar_analysis. These functions relate to constituency analysis,
meaning that they center on sentences parsed in tree structures.
'''

from tools import const

def get_root_parataxis_strict(root):
    '''
    Finds number of "strict" paratactic clauses among the children of a given etree node.
    "Strict" means that separating words (most importantly, conjunctions) are not ignored.
    
    Args:
        root: root of the etree
    
    Returns:
        The number of "strict" paratactic children
    '''
    children = [c.tag for c in root.getchildren() if not(c.tag.startswith('PUNCT-'))] # excludes punct
    sum = 0
    in_group = False
    
    for i in range(len(children) - 1):
        if children[i] in const.CLAUSE_TAGS and children[i + 1] in const.CLAUSE_TAGS:
            sum += 1
            if not(in_group):
                sum += 1
                in_group = True
        else:
            in_group = False
    return sum if sum != 0 else 1

def get_parataxis_loose(e):
    '''
    Finds number of "loose" paratactic clauses among the children of a given etree node.
    "Loose" means that separating words (most importantly, conjunctions) are ignored.
    
    Args:
        e: The node whose children to search
    
    Returns:
        The number of "loose" paratactic children
    '''
    return sum(int(bool(c.tag in const.CLAUSE_TAGS)) for c in e.getchildren())

def get_root_parataxis_loose(root):
    '''
    Finds number of "loose" paratactic clauses among the children of a the root of an etree.
    "Loose" means that separating words (most importantly, conjunctions) are ignored. This
    differs from the "get_parataxis_loose" method by applying a minimum of 1—i.e., there is at 
    least 1 clause in each sentence.
    
    Args:
        root: The tree root
    
    Returns:
        The number of "loose" paratactic children
    '''
    return max(1, get_parataxis_loose(root))

def get_num_sbar(root):
    '''
    Finds the number of subordinating clauses in a tree, measured by 
    the number of "SBAR" tags present.
    
    Args:
        root: The tree root
    
    Returns:
        The number of "SBAR" tags
    '''
    return sum(int(e.tag == 'SBAR') for e in root.iter())

def get_pronoun_sum(root):
    '''
    Finds the number of pronouns in a sentence tree
    
    Args:
        root: The tree root
    
    Returns:
        The number of pronouns
    '''
    return sum(int(e.tag in const.PRONOUN_TAGS) for e in root.iter())

def get_num_unk(root):
    '''
    Finds the number of "UNK" tokens in a sentence tree
    
    Args:
        root: The tree root
    
    Returns:
        The number of "UNK" tags
    '''
    return sum(int(e.tag == 'UNK') for e in root.iter())
