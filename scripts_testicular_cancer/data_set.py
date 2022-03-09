
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

from numpy.random import seed
from tensorflow.random import set_seed

seed(1)
set_seed(2)

def initialize(train_path='/content/train/',
          validation_path='/content/validation/',
          test_path='/content/test/',
          batch_size=64,
          im_size = 200):
  '''
    creates data generators + class_map
  '''

  # create data generator
  # TODO add data aug.
  datagen = ImageDataGenerator(rescale=1.0/255.0)
  
  # prepare iterators(train,val,test)
  train_it = datagen.flow_from_directory(train_path,
    class_mode='categorical', batch_size=64, target_size=(im_size, im_size))
  validation_it = datagen.flow_from_directory(validation_path,
    class_mode='categorical', batch_size=64, target_size=(im_size, im_size))
  test_it = datagen.flow_from_directory(test_path,
    class_mode='categorical', batch_size=64, target_size=(im_size, im_size))
  
  # define class map
  class_map = {v:k for (k,v) in test_it.class_indices.items()}
  return train_it,validation_it,test_it,class_map

def repr_im_hist(im_path, title=""):
  '''
   creates histogram + image subplot
  '''
  fig,ax = plt.subplots(1,2)
  plt.title(title)
  im = plt.imread(im_path)
  ax[0].hist(im.ravel())
  ax[1].imshow(im)
  plt.show()

def safe_save(model, save_path):
  '''
    save the model to disk
  '''
  try:
    model.save(save_path)
  except Exception as e:
    print(e)

def plot_history(history):
  '''
    quick plot of the loss curves (train+validation)
  '''
  assert "accuracy" in history.history.keys(), "please monitor the accuracy (training set) in the training script"
  assert "val_accuracy" in history.history.keys(), "please monitor the accuracy (validation) in the training script"

  plt.title("loss curves")
  plt.plot(history.history["accuracy"])
  plt.plot(history.history["val_accuracy"])
  plt.show()
