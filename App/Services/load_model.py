import tensorflow as tf

def load_model():
    filepath = "Model"
    model = tf.keras.models.load_model(filepath)
    return model

# Debug
# MODEL = load_model()

# def main():
#     load_model()

# if __name__ == "__main__":
#     main()