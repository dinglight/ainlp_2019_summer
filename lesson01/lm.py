import gzip
import jieba

from collections import Counter

TOKENS_1_GRAM = []
words_count_1 = {}

TOKENS_2_GRAM = []
words_count_2 = {}

# language model
def cut(string):
    return list(jieba.cut(string))

def lm_build():
    sentences = []
    with gzip.open("train.txt.gz", 'rt', encoding='utf-8') as pf:
        for line in pf.readlines():
            sentences.append(line.split('++$++')[2].strip())
    #print(len(sentences))

    tokens = []
    tokens_2 = []
    for s in sentences:
        result = cut(s)
        tokens += result
        tokens_2 += [''.join(result[i:i+2]) for i in range(len(result[:-1]))]
    #print(len(tokens))

    with open("1gram.txt", 'wt', encoding='utf-8') as f:
        for t in tokens:
            f.write(t+'\n')

    with open("2gram.txt", 'wt', encoding='utf-8') as f:
        for t in tokens_2:
            f.write(t+'\n')

def lm_load_1gram():
    with open("1gram.txt", 'rt', encoding='utf-8') as f:
        for line in f.readlines():
            TOKENS_1_GRAM.append(line)

    words_count_1 = Counter(TOKENS_1_GRAM)

def lm_load_2gram():
    with open("2gram.txt", 'rt', encoding='utf-8') as f:
        for line in f.readlines():
            TOKENS_2_GRAM.append(line)

    words_count_2 = Counter(TOKENS_2_GRAM)

def lm_pro1(word):
    if word in words_count_1:
        return words_count_1[word] / len(TOKENS_1_GRAM)
    else:
        return 1 / len(TOKENS_1_GRAM)

def lm_pro2(word1, word2):
    if word1+word2 in words_count_2:
        return words_count_2[word1+word2] / len(TOKENS_2_GRAM)
    else:
        return 1 / len(TOKENS_2_GRAM)

def get_probability(sentence):
    words = cut(sentence)
    sentece_pro = 1
    for i, word in enumerate(words[:-1]):
        next_word = words[i+1]
        probability = lm_pro2(word, next_word)
        sentece_pro *= probability
    return sentece_pro

if __name__ == '__main__':
    lm_build()
