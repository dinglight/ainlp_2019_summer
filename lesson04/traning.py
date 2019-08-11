from gensim.models import word2vec
import logging

corpus_line = word2vec.LineSentence('zhwiki_only_simple_and_cut.txt')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
cbow_model = word2vec.Word2Vec(corpus_line, size=200, window=5, min_count=5, workers=4)
cbow_model.save("cbow_word2vec.model")
skip_gram_model_10000 = word2vec.Word2Vec(corpus_line, size=200, window=10, min_count=10000, sg=1, workers=4)
skip_gram_model_10000.save("skip_gram_word2vec_10000.model")
cbow_model_10000 = word2vec.Word2Vec(corpus_line, size=200, window=5, min_count=10000, workers=4)
cbow_model_10000.save("cbow_word2vec_10000.model")
