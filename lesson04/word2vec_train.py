import sys
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import multiprocessing

def word2vec_train(in_file, out_model, out_vector):
    sentences = LineSentence(in_file)
    model = Word2Vec(sentences, workers=multiprocessing.cpu_count())
    model.save(out_model)
    model.wv.save_word2vec_format(out_vector, binary=False)

if __name__ == '__main__':
    word2vec_train(sys.argv[1], sys.argv[2],sys.argv[3])
