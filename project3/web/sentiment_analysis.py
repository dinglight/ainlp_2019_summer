import pandas as pd
import numpy as np
from keras.utils.np_utils import to_categorical
import jieba
import io
from model import load_train_model, predict_sequence


word_embeddings = {}
#inf_encoder_model = None
#inf_decoder_model = None
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

def initialize():
    global word_embeddings
    word_embeddings = load_word_embeddings('../../../data/fasttext/cc.zh.300.vec')
    #global inf_encoder_model
    #global inf_decoder_model
    #inf_encoder_model, inf_decoder_model = load_train_model('../seq/s2s_train.h5', 128)

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

def parse_comment(text):
    global word_embeddings
    #global inf_encoder_model
    #global inf_decoder_model
    max_encoder_seq_length = 100

    df = pd.DataFrame([{'id':0,
                       'content': text,
                       'location_traffic_convenience': -2,
                        'location_distance_from_business_district': -2,
                        'location_easy_to_find': -2,
                        'service_wait_time': -2,
                        'service_waiters_attitude': -2,
                        'service_parking_convenience': -2,
                        'service_serving_speed': -2,
                        'price_level': -2,
                        'price_cost_effective': -2,
                        'price_discount': -2,
                        'environment_decoration': -2,
                        'environment_noise': -2,
                        'environment_space': -2,
                        'environment_cleaness': -2,
                        'dish_portion': -2,
                        'dish_taste': -2,
                        'dish_look': -2,
                        'dish_recommendation': -2,
                        'others_overall_experience': -2,
                        'others_willing_to_consume_again':-2}])
    data = df['content'].apply(cut)

    x = vectorize_sequence(data, max_encoder_seq_length, word_embeddings)
    inf_encoder_model, inf_decoder_model = load_train_model('../seq/s2s_train.h5', 128)
    for i, _ in enumerate(x):
        encoded_seq = predict_sequence(inf_encoder_model, inf_decoder_model, x[i:i+1], 20, 4)
        seq = one_hot_decode(encoded_seq)
        df.iloc[i, 2:] = seq

    columns = df.columns.values.tolist()
    result_df = df[columns[2:]]
    df2 = pd.DataFrame(result_df.values.T, index=result_df.columns, columns=result_df.index)
    return df2
