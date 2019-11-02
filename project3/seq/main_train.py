from data_process import init, load_data
from model import define_models

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] <%(processName)s> (%(threadName)s) %(message)s')
logger = logging.getLogger(__name__)

path = '../../../data/comment-classification/'

num_encoder_tokens = 300  # 300 维的词向量
num_decoder_tokens = 4    # 4 种情感等级
latent_dim = 128
batch_size = 32
epochs = 2

if __name__ == '__main__':
    logger.info("start load fasttext wordembedings")
    init()
    logger.info("start load train data")
    x1_train, x2_train, y_train = load_data(path+'sentiment_analysis_trainingset.csv', nrows=1000)
    print(x1_train.shape, x2_train.shape, y_train.shape)

    logger.info("start load valid data")
    x1_valid, x2_valid, y_valid = load_data(path+'sentiment_analysis_validationset.csv', nrows=200)
    print(x1_valid.shape, y_valid.shape)

    logger.info("start load model")
    train, infenc, infdec = define_models(num_encoder_tokens, num_decoder_tokens, latent_dim)
    train.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])

    logger.info("start train model")
    train.fit([x1_train, x2_train], y_train,
              batch_size=batch_size, epochs=epochs,
              validation_data=([x1_valid, x2_valid], y_valid))
    logger.info("complete train model")

    # save model
    logger.info("start save model")
    train.save('s2s_train.h5')
    logger.info("complete save model")
