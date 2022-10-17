from pythainlp.tokenize import word_tokenize
from tensorflow.keras.preprocessing.sequence import pad_sequences

def text_transform(used_model, WORD2VEC_MODEL, text, stopwords):
    word_token = clean_input(text, stopwords)
    word_indices = map_word_index(WORD2VEC_MODEL, word_token)
    length = used_model.layers[0].output_shape[0][1]
    padded_word_indices = pad_sequences([word_indices], maxlen=length, value=0)
    return padded_word_indices

def specialClass(answer, label):
    if answer in label:
        return ""
    else:
        return answer

def map_word_index(WORD2VEC_MODEL, word_seq):
    indices = []
    for word in word_seq:
        if word in WORD2VEC_MODEL.vocab:
            indices.append(WORD2VEC_MODEL.vocab[word].index + 1)
        else:
            indices.append(1)
    return indices

def clean_input(text, stopwords):
    input_text = word_tokenize(text, keep_whitespace=False)
    list_word_not_stopwords = [i for i in input_text if i not in stopwords]
    return list_word_not_stopwords

# Debug
# if __name__ == '__main__':
#     from gensim.models import KeyedVectors

#     def load_word2vec_model():
#         word2vec_model = KeyedVectors.load_word2vec_format('Src\LTW2V_v0.1.bin', binary=True, unicode_errors='ignore')
#         return word2vec_model

#     WORD2VEC_MODEL = load_word2vec_model()
#     print(text_transform(WORD2VEC_MODEL, 29, "การเพิ่มมาตรฐานในขั้นตอนที่ 1"))

    