import pandas as pd
import numpy as np
from keras.utils.np_utils import to_categorical
import jieba
import io

# load fasttext pretrained word vectors
word_embeddings = {}

def init():
    global word_embeddings
    word_embeddings = load_word_embeddings('../../../data/fasttext/cc.zh.300.vec')

def load_word_embeddings(fname):
    vocab_and_vectors = {}
    with open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore') as file:
        # put words as dict indexes and vectors as words values
        for line in file:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], dtype='float32')
            vocab_and_vectors[word] = vector
    return vocab_and_vectors

def cut(text):
    return ' '.join(jieba.cut(text))

def vectorize_sequence(texts, max_encoder_seq_length, word_embeddings):
    embedding_size = word_embeddings['测试'].shape[0]
    results = np.zeros((len(texts), max_encoder_seq_length, embedding_size), dtype='float32')

    for i, text in enumerate(texts):
        words = text.split()
        words = [w for w in words if w in word_embeddings]
        seq_length = len(words)
        padding_size = (max_encoder_seq_length - seq_length) if (max_encoder_seq_length > seq_length) else 0
        for j in range(max_encoder_seq_length):
            if j < padding_size:
                results[i][j] = np.zeros_like(word_embeddings['测试'])
            else:
                results[i][j] = word_embeddings[words[j-padding_size]]
    return results

def one_hot_decode(encoded_seq):
    result = np.array([np.argmax(vector) for vector in encoded_seq], dtype=int)
    result = result -2
    return result


def load_data(fname, nrows):
    global word_embeddings
    max_encoder_seq_length = 100
    label_classes = 4
    # read train data
    df = pd.read_csv(fname, nrows=nrows)

    # process text
    data = df['content']
    data = data.apply(cut)

    x1 = vectorize_sequence(data, max_encoder_seq_length, word_embeddings)

    # process labels
    columns = df.columns.values.tolist()
    labels = df[columns[2:]]
    y = to_categorical(labels+2, num_classes=label_classes)

    # generate x2
    x2 = np.vstack([np.zeros((1,y.shape[1],label_classes), dtype='float32'), y[:-1]])

    return x1, x2, y
