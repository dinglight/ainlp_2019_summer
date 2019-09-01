import jieba
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import multiprocessing

def cut_file(in_file, out_file):
    cut_file = open(out_file, 'w', encoding='utf-8')
    for line in open(in_file, 'r', encoding='utf-8'):
        cut_file.write(' '.join(jieba.cut(line))+'\n')


def word2vec_train(in_file, out_model):
    sentences = LineSentence(in_file)
    model = Word2Vec(sentences, workers=multiprocessing.cpu_count())
    model.save(out_model)
    #model.wv.save_word2vec_format(out_vector, binary=False)

if __name__ == '__main__':
    cut_file('article_9k.txt', 'article_9k_cut.txt');
    word2vec_train('article_9k_cut.txt', 'article_9k_word2vec.model')
