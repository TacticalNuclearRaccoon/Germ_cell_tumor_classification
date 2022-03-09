# load dataset with image data generator
from os import listdir
from numpy import asarray
from numpy import save
import tensorflow
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras.preprocessing.image import *
from tensorflow.keras.optimizers import SGD
import matplotlib.pyplot as plt
import numpy as np
import cv2



# define cnn model
def define_model(n_classes=3, size=200):
	'''
	definition of a simple model
	'''
	model = Sequential()
	model.add(Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same', input_shape=(size, size, 3)))
	model.add(MaxPooling2D((2, 2)))
	model.add(Flatten())
	model.add(Dense(6, activation='relu', kernel_initializer='he_uniform'))
	model.add(Dense(n_classes, activation='softmax'))
	
	return model

def compile_model(model, opt=None):
	"""
	prepare a model for categorical crossentropy
	"""

	if opt == None:
	opt = SGD(lr=0.001, momentum=0.9)
	# compile model

	model.compile(optimizer=opt, 
		  loss='categorical_crossentropy', 
		  metrics=['accuracy'])
	return model


def string_predict_single(model, im, class_map, size=200):
	"""
	predict image
	
	"""
	# in case the image has 4 channels (RGBA)
	if im.shape[-1]>3:
		im = im[:,:,:3]
	# resize image to model's input shape
	if im.shape[0:2] != model.input_shape[1:3]:
		im = cv2.resize(im,(size, size))
	
	# since it's a single image prediction - need to expand the first dimension
	predictions = model.predict(np.expand_dims(im, axis=0))
	
	# get the index of the max pred
	pred = np.argmax(predictions)
	
	#use a "mapping" dictionary to return the "human readable class"
	string_class = class_map[pred]
	
  	return string_class, predictions
