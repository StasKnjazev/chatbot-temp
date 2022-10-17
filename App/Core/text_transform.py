from pythainlp.tokenize import word_tokenize
from tensorflow.keras.preprocessing.sequence import pad_sequences

def text_transform(WORD2VEC_MODEL, MAX_LENG, text):
    word_token = word_tokenize(text)
    word_indices = map_word_index(WORD2VEC_MODEL, word_token)
    padded_word_indices = pad_sequences([word_indices], maxlen=MAX_LENG, value=0)
    return padded_word_indices

def map_word_index(WORD2VEC_MODEL, word_seq):
    indices = []
    for word in word_seq:
        if word in WORD2VEC_MODEL.vocab:
            indices.append(WORD2VEC_MODEL.vocab[word].index + 1)
        else:
            indices.append(1)
    return indices

# Debug
# if __name__ == '__main__':
#     from gensim.models import KeyedVectors

#     def load_word2vec_model():
#         word2vec_model = KeyedVectors.load_word2vec_format('Src\LTW2V_v0.1.bin', binary=True, unicode_errors='ignore')
#         return word2vec_model

#     WORD2VEC_MODEL = load_word2vec_model()
#     print(text_transform(WORD2VEC_MODEL, 29, "การเพิ่มมาตรฐานในขั้นตอนที่ 1"))

    