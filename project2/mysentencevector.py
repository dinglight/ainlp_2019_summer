import pandas as pd
import jieba
from gensim.models import FastText
from gensim.models.word2vec import LineSentence
import numpy as np

def train_wordvectors(in_file, out_file):
    df = pd.read_csv(in_file, encoding='gb18030', usecols=['content'])
    df = df.fillna('')
    df['tokens'] = df['content'].apply(lambda x: list(jieba.cut(x)))
    sentences = df['tokens'].tolist()
    model = FastText(sentences, window=5, size=35, iter=10, min_count=1)
    model.save(out_file)


word_vectors = {}
word_frequences={}
max_word_frequence = 0.0
def wordvector_init():
    model = FastText.load('newscorpus.fasttext.bin')
    for word in model.wv.vocab:
        word_vectors[word] = model[word]
        word_frequences[word] = model.wv.vocab[word].count / model.corpus_total_words

    max_word_frequence = max(word_frequences.values())

def get_word_vector(word):
    return word_vectors[word]

def get_word_frequence(word):
    return word_frequences[word]

def get_max_word_frequence():
    return max_word_frequence

def sentence_embedding(text):
    '''get the vector of the text
    Args:
        text: a string
    Return:
        vector: a vector of the text
    '''
    # weight = alpah/(alpah + p)
    # alpha is a parameter, 1e-3 ~ 1e-5
    alpha = 1e-4

    sentence_vec = np.zeros_like(word_vectors['测试'])

    words = jieba.cut(text)
    words = [w for w in words if w in word_vectors]

    for w in words:
        weight = alpha / (alpha + get_word_frequence(w))
        sentence_vec += weight * get_word_vector(w)

    if len(words) > 0:
        sentence_vec /= len(words)
    # Skip the PCA
    return sentence_vec


if __name__ == '__main__':
    train_wordvectors('../../data/sqlResult_1558435.csv', 'newscorpus.fasttext.bin')
