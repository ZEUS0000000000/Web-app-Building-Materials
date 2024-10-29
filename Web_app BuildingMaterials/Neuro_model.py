import tensorflow as tf
import string
import re
from tensorflow import keras
from tensorflow.keras import layers
import random
import numpy as np

from tensorflow.python.types.core import runtime_checkable
import keras_nlp
import rouge
from rouge import Rouge
from nltk.translate.bleu_score import sentence_bleu


text_file = "output_changed4.txt"

with open(text_file) as f:
  lines = f.read().split("\n")[:-1]
  print(lines)

text_pairs = []
for line in lines:
    input, output = line.split("\t")
    output = "[start] " + output + " [end]"
    text_pairs.append((input, output))



random.shuffle(text_pairs)
num_val_samples = int(0.15*len(text_pairs))
num_train_samples = len(text_pairs) -2  * num_val_samples
train_pairs = text_pairs[:num_train_samples]
val_pairs = text_pairs[num_train_samples:num_train_samples + num_val_samples]
test_pairs = text_pairs[num_train_samples + num_val_samples:]



strip_chars = string.punctuation + ",.!?"
strip_chars = strip_chars.replace("[", "")
strip_chars = strip_chars.replace("]", "")

def custom_standardization(input_string):
    lowercase = tf.strings.lower(input_string)
    return tf.strings.regex_replace(
        lowercase, f"[{re.escape(strip_chars)}]", "")

vocab_size = 15000
sequence_length = 20

input_vectorization = layers.TextVectorization(
    max_tokens = vocab_size,
    output_mode = "int",
    output_sequence_length = sequence_length,
)

output_vectorization = layers.TextVectorization(
    max_tokens = vocab_size,
    output_mode = "int",
    output_sequence_length = sequence_length + 1,
    standardize = custom_standardization,
)
train_input_texts = [pair[0] for pair in train_pairs]
train_output_texts = [pair[1] for pair in train_pairs]

input_vectorization.adapt(train_input_texts)
output_vectorization.adapt(train_output_texts)



output_vocab = output_vectorization.get_vocabulary()
output_index_lookup = dict(zip(range(len(output_vocab)),output_vocab))
max_decoded_sentence_length = 20

model = keras.models.load_model("model/model.h5")  # ЗАГРУЗКА МОДЕЛИ

def decode_rnn_sequence(input_sentence):
  tokenized_input_sentence = input_vectorization([input_sentence])
  decoded_sentence = "[start]"
  for i in range(max_decoded_sentence_length):
    tokenized_output_sentence = output_vectorization([decoded_sentence])
    next_token_predictions = model.predict(
        [tokenized_input_sentence, tokenized_output_sentence],verbose = None)
    sampled_token_index = np.argmax(next_token_predictions[0, i, :])
    sampled_token = output_index_lookup[sampled_token_index]
    decoded_sentence += " " + sampled_token
    if sampled_token == "[end]":
      break
  return decoded_sentence