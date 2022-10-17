import tensorflow as tf
from gensim.models import KeyedVectors

def load_model(path):
    model = tf.keras.models.load_model(path)
    return model


def load_word2vec_model():
    word2vec_model = KeyedVectors.load_word2vec_format('Src\LTW2V_v0.1.bin', binary=True, unicode_errors='ignore')
    return word2vec_model