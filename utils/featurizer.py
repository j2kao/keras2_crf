import re
from utils.loader import normalize_word
from utils.loader import E_UNKN

def casing_featurize(word):
    frac = sum([c.isdigit() for c in word]) / len(word)

    if word.isdigit():
        return 'NUM'
    elif frac > 0.5:
        return 'M_NUM'
    elif word.islower():
        return 'LOW'
    elif word.isupper():
        return 'UPP'
    elif word[0].isupper():
        return 'I_UPP'
    elif frac > 0:
        return 'H_NUM'
    else:
        return 'OTHER'       

    
def featurize(X):
    all_casing = list()
    
    for sentence in X:
        sentence_casing = list()
        for word in sentence:
            feature = casing_featurize(word)
            sentence_casing.append(feature)
        all_casing.append(sentence_casing)
        
    return all_casing


def map_words(X, word2index):
    all_maps = list()
    for sentence in X:
        sentence_map = list()
        for word in sentence:
            default = word2index[E_UNKN]
            
            # I really have to fix this...
            index = word2index.get(word, word2index.get(word.lower(), word2index.get(normalize_word(word), default)))
            sentence_map.append(index)
        
        all_maps.append(sentence_map)
        
    return all_maps