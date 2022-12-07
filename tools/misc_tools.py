''' Contains miscellaneous tools, primarily relating to preparing XML trees for etree analysis. '''

import re

def clean_xml(xml):
    '''
    Certain characters cannot appear in XML tags (including certain punctuation). This method
    finds such occurrences and replaces them with a generic <UNK> token. Cleaned XML strings
    should be able to be processed by the etree generator without error, assuming they meet
    other XML requirements.

    Args:
        xml: Original XML string
    
    Returns:
        Cleaned XML string
    '''
    xml = re.sub('<(/?)[^a-zA-Z/][^>]*>', '<\g<1>UNK>', xml) # invalid tokens labeled 'UNK'
    return xml.replace(' ', '')

def sexp_to_xml(sexp):
    '''
    Changes an S-expression tree to an XML tree. Special tags found in "special_chars.txt"
    are replaced as specified in the file. 

    Args:
        sexp: S-expression as a string
    
    Returns:
        XML tree as string
    '''
    def apply_inner_re(s):
        return re.sub('\(([^ ]*) ([^\)\(]*)\)', '<\g<1>> \g<2> </\g<1>>', s)

    xml = apply_inner_re(sexp)
    while xml.startswith('('):
        xml = apply_inner_re(xml)

    with open('special_chars.txt') as f:
        special_chars = dict([line.split() for line in f])

    def key_to_re(s):
        s = re.sub('(.*)([\\\.\+\*\?\^\$\(\)\[\]\{\}\|])(.*)', '\g<1>\\\\\g<2>\g<3>', s)
        return '<(/?)' + s + '>'

    for k, v in special_chars.items():
        xml = re.sub(key_to_re(k), f'<\g<1>{v}>', xml)

    return clean_xml(xml)