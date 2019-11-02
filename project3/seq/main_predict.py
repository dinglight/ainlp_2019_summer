from data_process import load_word_embeddings, cut, one_hot_decode, vectorize_sequence
from model import load_train_model, predict_sequence
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] <%(processName)s> (%(threadName)s) %(message)s')
logger = logging.getLogger(__name__)

path = '../../../data/comment-classification/'

max_encoder_seq_length = 100
latent_dim = 128

if __name__ == '__main__':
    logger.info("start load fasttext wordembedings")
    word_embeddings = load_word_embeddings('../../../data/fasttext/cc.zh.300.vec')

    logger.info("start load test data")
    df = pd.read_csv(path+'sentiment_analysis_testa.csv', nrows=100)
    logger.info("start tokenizer test data")
    data = df['content']
    data = data.apply(cut)

    logger.info("start vectorize test data")
    x = vectorize_sequence(data, max_encoder_seq_length, word_embeddings)
    print(x.shape)

    logger.info("start load model")
    infenc, infdec = load_train_model('s2s_train.h5', latent_dim)

    logger.info("start predict test data")
    for i, _ in enumerate(x):
        encoded_seq = predict_sequence(infenc, infdec, x[i:i+1], 20, 4)
        seq = one_hot_decode(encoded_seq)
        df.iloc[i, 2:] = seq

    df.to_csv('sentiment_analysis_testa.csv', encoding="utf_8_sig", index=False)
    logger.info("compete predict test data")
