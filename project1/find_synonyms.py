from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from collections import defaultdict

def get_synonyms(seed_words, model):
    '''
    with optimize 2 : dynamic programming
    @seed_words are words that we already known
    @model is the word2vec model
    '''
    dp_table = defaultdict(list)

    unseen = seed_words;
    seen = defaultdict(int)
    max_size = 500 # when found max_size synonyms we stop
    while unseen and len(seen) < max_size:
        if len(seen) % 100 == 0:
            print('seen size: {}'.format(len(seen)))

        node = unseen.pop(0)
        if not dp_table[node]:
            dp_table[node] = [w for w,s in model.wv.most_similar(node, topn=20)]

        new_expanding = dp_table[node]
        unseen += new_expanding
        seen[node] += 1

        # optimize: 1. score function could be revised
        # optimize: 2. using dynamic programming to reduce computing time

    return seen

if __name__ == '__main__':
    synonyms = get_synonyms(['说', '表示'], Word2Vec.load('../lesson04/cbow_word2vec.model'))
    synonyms_sorted = sorted(synonyms.items(), key=lambda x: x[1], reverse=True)

    with open('saywords.txt', 'w', encoding='utf8') as f:
        for word, freq in synonyms_sorted:
            if freq > 1:
                f.write("{}\n".format(word))
