import re
import numpy as np

E_MASK = 'MASK_TOKEN' # this should be word vector number 0
E_DATE = 'DATE_TOKEN'
E_TIME = 'TIME_TOKEN'
E_NUMB = 'NUMB_TOKEN'
E_UNKN = 'UNKN_TOKEN'
E_TOKENS = [E_DATE, E_TIME, E_NUMB, E_UNKN]


def load_dataset(path):
    X = list()
    y = list()
    
    with open(path, 'r') as file:
        X_seq = list()
        y_seq = list()
        
        for i, line in enumerate(file):
            line = line.strip()
            if len(line) == 0:
                # Blank line = end of sentence
                
                X.append(X_seq)
                y.append(y_seq)
                
                X_seq = list()
                y_seq = list()
            else:                
                parts    = line.strip().split()
                X_seq.append(parts[1]) # 1 - each word
                y_seq.append(parts[3]) # 3 - POS tag
        
        if len(X_seq) > 0:
            X.append(X_seq)
            y.append(y_seq)
        
    return X, y


def normalize_word(word):
    # could add http:// ... for URLs
    # could improve tokenization for the case 9999aa

    word = word.lower().replace("--", "-")
    word = re.sub("\"+", '"', word)
    word = re.sub("[0-9]{4}-[0-9]{2}-[0-9]{2}", E_DATE, word)
    word = re.sub("[0-9]{2}/[0-9]{2}/[0-9]{2}([0-9]{2})?", E_DATE, word)
    word = re.sub("[0-9]{2}:[0-9]{2}:[0-9]{2}", E_TIME, word)
    word = re.sub("[0-9]{2}:[0-9]{2}", E_TIME, word)
    word = re.sub("([0-9]+[.,]?)+", E_NUMB, word)
    return word


def build_vocabulary(X):
    vocab = set()
    for sentence in X:
        for word in sentence:
            vocab.update([word, word.lower(), normalize_word(word)])
    return vocab


def load_word_embeddings(path, dimension, vocabulary=None, show_not_found=False):
    vectors = list()
    word2id = dict()
    words_found = set()
    
    # the masking word is used when trimming input sentences
    # its predictions will be ignored (skipped)
    word2id[E_MASK] = 0
    vectors.append([0] * dimension)
    
    # adding actual words to the mapping
    for i, line in enumerate(open(path, 'r')):
        entry = line.strip().split()

        word  = entry[0]
        wv    = entry[1:]
        if len(wv) != dimension:
            print('[ERR] Word {} has less than {} dimensions.'.format(word, dimension))
        
        if not vocabulary or (word in vocabulary):
            word2id[word] = len(vectors)
            vectors.append(wv)
            words_found.add(word)
            
    # creating embeddings for special tokens
    for special_embedding in E_TOKENS:
        new_wv = np.random.uniform(-0.25, 0.25, dimension)
        
        word2id[special_embedding] = len(vectors)
        vectors.append(new_wv)

    if vocabulary:
        not_found = vocabulary.difference(words_found)        
        normalized_not_found = {normalize_word(word) for word in not_found}
        
        not_found = normalized_not_found.difference(words_found)
        txt = ', '.join(map(str, not_found))
        
        if show_not_found:
            print('Words not found: [{}].'.format(txt))
            print('\n')

    vectors = np.asarray(vectors, dtype=np.float32)
    return vectors, word2id
