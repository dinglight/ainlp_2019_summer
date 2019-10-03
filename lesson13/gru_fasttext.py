import numpy as np
import pandas as pd
from keras.preprocessing import text, sequence
from keras.models import Model
from keras.layers import Input, Dense, GRU,Embedding, Bidirectional
from keras.layers import GlobalAveragePooling1D, GlobalMaxPooling1D, concatenate, SpatialDropout1D
from keras.initializers import Constant

import io

def load_vectors(fname):
    file = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    vocab_and_vectors = {}
    # put words as dict indexes and vectors as words values
    for line in file:
        values = line.split()
        word = values[0]
        vector = np.asarray(values[1:], dtype='float32')
        vocab_and_vectors[word] = vector
    return vocab_and_vectors


MAX_NUM_WORDS = 30000
EMBEDDING_DIM = 300
MAX_SEQUENCE_LENGTH = 100

train = pd.read_csv('./data/train.csv')
X_train_texts = train['comment_text'].fillna('').values
y_train = train[['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']].values

test = pd.read_csv('./data/test.csv')
X_test_texts = test['comment_text'].fillna('').values


token = text.Tokenizer(num_words=MAX_NUM_WORDS)
token.fit_on_texts(list(X_train_texts)+list(X_test_texts))

X_train_seqs = token.texts_to_sequences(X_train_texts)
X_test_seqs  = token.texts_to_sequences(X_test_texts)

X_train = sequence.pad_sequences(X_train_seqs, maxlen = MAX_SEQUENCE_LENGTH)
X_test  = sequence.pad_sequences(X_test_seqs, maxlen = MAX_SEQUENCE_LENGTH)

word_index = token.word_index
print('Found {} unique tokens.'.format(len(word_index)))

embeddings_index = load_vectors('../../data/crawl-300d-2M.vec')

# prepare embedding matrix
num_words = min(MAX_NUM_WORDS, len(word_index) + 1)
embedding_matrix = np.zeros((num_words, EMBEDDING_DIM))
for word, i in word_index.items():
    if i >= MAX_NUM_WORDS:
        continue
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        # words not found in embedding index will be all-zeros.
        embedding_matrix[i] = embedding_vector


# build model
inp = Input(shape=(MAX_SEQUENCE_LENGTH, ))
x = Embedding(input_dim = num_words,
                    output_dim = EMBEDDING_DIM,
                    embeddings_initializer=Constant(embedding_matrix),
                    input_length=MAX_SEQUENCE_LENGTH,
                    trainable=False)(inp)
x = SpatialDropout1D(0.2)(x)
x = Bidirectional(GRU(256, return_sequences=True, dropout=0.1, recurrent_dropout=0.1))(x)
avg_pool = GlobalAveragePooling1D()(x)
max_pool = GlobalMaxPooling1D()(x)
x = concatenate([avg_pool, max_pool])
outp = Dense(units=6, activation='sigmoid')(x)

model = Model(inp, outp)
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
train_history = model.fit(X_train, y_train, batch_size=32, epochs=4, verbose=2, validation_split=0.2)

y_pred = model.predict(X_test, batch_size=1024)

submission = pd.read_csv('./data/sample_submission.csv')
submission[["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]] = y_pred
submission.to_csv('submission.csv', index=False)
