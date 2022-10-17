from gensim.models import KeyedVectors

def load_word2vec_model():
    word2vec_model = KeyedVectors.load_word2vec_format('Src\LTW2V_v0.1.bin', binary=True, unicode_errors='ignore')
    return word2vec_model