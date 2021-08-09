import matplotlib.pyplot as plt
import os
import re
import shutil
import string
import tensorflow as tf

from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras import preprocessing
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization

def
def setup_func():
	fbad = open('analysis_bad.txt', 'w')
	fneutral = open('analysis_neutral.txt', 'w')
	fgood = open('analysis_good.txt', 'w')

	fsolution = open('sentiment_analysis_solution_set.txt','r')
	ftest = open('sentiment_analysis_test_set.txt','r')

	data = []
	for line in ftest:
		if line == '-------------------------------------------------------------------------------------------------------------\n':
			data.append('')
		else:
			data[-1] += line

	for i in range(99):
		if data[i] != '\n' and data[i] != '\n\n':
			data[i] = data[i].replace('\n','')

	solution_set = []
	for line in fsolution:
		solution_set.append(line.split(':')[1][1:-1])

	if len(data) != 99 or len(solution_set) != 99:
		print("error: data_len = {}, solution_len = {}".format(str(len(data)), str(len(solution_set)) ) )

	for i in range(99):
		if solution_set[i] == '-1':
			fbad.write(data[i]+'\n')
		elif solution_set[i] == '0':
			fneutral.write(data[i]+'\n')
		else:
			fgood.write(data[i]+'\n')

	fbad.close()
	fneutral.close()
	fgood.close()
	fsolution.close()
	ftest.close()

def tf_training():
	raw_train_ds = tf.keras.preprocessing.text_dataset_from_directory(
	    'test_set', validation_split=0.1, subset='training', seed=42)
	raw_val_ds = tf.keras.preprocessing.text_dataset_from_directory(
	    'test_set', validation_split=0.1, subset='validation', seed=42)
	raw_test_ds = tf.keras.preprocessing.text_dataset_from_directory(
	    'test_set')

	max_features = 10000
	sequence_length = 250

	vectorize_layer = TextVectorization(
	    max_tokens=max_features,
	    output_mode='int',
	    output_sequence_length=sequence_length)

	def vectorize_text(text, label):
	  text = tf.expand_dims(text, -1)
	  return vectorize_layer(text), label

	train_text = raw_train_ds.map(lambda x, y: x)
	vectorize_layer.adapt(train_text)


	train_ds = raw_train_ds.map(vectorize_text)
	val_ds = raw_val_ds.map(vectorize_text)
	test_ds = raw_test_ds.map(vectorize_text)


	AUTOTUNE = tf.data.AUTOTUNE

	train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
	val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
	test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

	embedding_dim = 16
	model = tf.keras.Sequential([
	  layers.Embedding(max_features + 1, embedding_dim),
	  layers.Dropout(0.2),
	  layers.GlobalAveragePooling1D(),
	  layers.Dropout(0.2),
	  layers.Dense(1)])

	model.summary()

	model.compile(loss=losses.BinaryCrossentropy(from_logits=True),
	              optimizer='adam',
	              metrics=tf.metrics.BinaryAccuracy(threshold=0.0))

	epochs = 10
	history = model.fit(
	    train_ds,
	    validation_data=val_ds,
	    epochs=epochs)

	loss, accuracy = model.evaluate(test_ds)
	print("Loss: ", loss)
	print("Accuracy: ", accuracy)

	# exporting
	export_model = tf.keras.Sequential([
	  vectorize_layer,
	  model,
	  layers.Activation('sigmoid')
	])

	export_model.compile(
	    loss=losses.BinaryCrossentropy(from_logits=False), optimizer="adam", metrics=['accuracy']
	)

	# Test it with `raw_test_ds`, which yields raw strings
	loss, accuracy = export_model.evaluate(raw_test_ds)
	print(accuracy)

	examples = [
	  "I'm not so sure about buying up on Apple, although it has had some highs, I think it is at its peak"
	  "Apples and oranges, apples and oranges, stocks will be stocks",
	  "Apple has seen a steady drop recently, but I believe that it is about to turn a corner and rise"
	]

	print(export_model.predict(examples))

def standardize(term, text):
	# remove htmls
	import re
	text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
	text.replace('&gt', '')
	
