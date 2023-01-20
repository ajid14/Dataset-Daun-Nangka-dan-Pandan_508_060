# -*- coding: utf-8 -*-
"""sourcecode_ai.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HsJhs7r5-pbTQFkquBWe5oNLoDNYVgJl
"""

from google.colab import drive
import os

drive.mount('/content/drive')

base_dir = '/content/drive/My Drive/AI-C/'
!ls "/content/drive/My Drive/AI-C"

bahan_dir = os.path.join(base_dir, 'bahan')
train_dir = os.path.join(base_dir, 'latih')
validation_dir = os.path.join(base_dir, 'validasi')

pandan_dir = os.path.join(bahan_dir, 'Daun_Pandan/')
nangka_dir = os.path.join(bahan_dir, 'Daun_Nangka/')

print("Jumlah Dataset Setiap Daun")
print("Jumlah daun Nangka  : ", len(os.listdir(nangka_dir)))
print("Jumlah daun Pandan  : ", len(os.listdir(pandan_dir)))

train_pandan = os.path.join(train_dir, 'Daun_Pandan/')
train_nangka = os.path.join(train_dir, 'Daun_Nangka/')

validation_pandan  = os.path.join(validation_dir, 'Daun_Pandan/')
validation_nangka  = os.path.join(validation_dir, 'Daun_Nangka/')

import random
from shutil import copyfile

def train_val_split(source, train, val, train_ratio):
  total_size = len(os.listdir(source))
  train_size = int(train_ratio * total_size)
  val_size = total_size - train_size

  randomized = random.sample(os.listdir(source), total_size)
  train_files = randomized[0:train_size]
  val_files = randomized[train_size:total_size]

  for i in train_files:
    i_file = source + i
    destination = train + i
    copyfile(i_file, destination)

  for i in val_files:
    i_file = source + i
    destination = val + i
    copyfile(i_file, destination)

train_ratio = 0.9

source_00 = pandan_dir
train_00 = train_pandan
val_00 = validation_pandan
train_val_split(source_00, train_00, val_00, train_ratio)

source_01 = nangka_dir
train_01 = train_nangka
val_01 = validation_nangka
train_val_split(source_01, train_01, val_01, train_ratio)

print('jumlah seluruh pandan    : ', len(os.listdir(pandan_dir)))
print('jumlah train pandan      : ', len(os.listdir(train_pandan)))
print('jumlah validation pandan : ', len(os.listdir(validation_pandan)))

print('jumlah seluruh nangka    : ', len(os.listdir(nangka_dir)))
print('jumlah train nangka      : ', len(os.listdir(train_nangka)))
print('jumlah validation nangka : ', len(os.listdir(validation_nangka)))

import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
    rescale = 1./255,
    rotation_range = 30,
    horizontal_flip = True,
    shear_range = 0.3,
    fill_mode = 'nearest',
    width_shift_range = 0.2,
    height_shift_range = 0.2,
    zoom_range = 0.1
)

val_datagen = ImageDataGenerator(
    rescale = 1./255,
    rotation_range = 30,
    horizontal_flip = True,
    shear_range = 0.3,
    fill_mode = 'nearest',
    width_shift_range = 0.2,
    height_shift_range = 0.2,
    zoom_range = 0.1
)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size = (150, 150),
    batch_size = 10,
    class_mode = 'categorical'
)

val_generator = val_datagen.flow_from_directory(
    validation_dir,
    target_size = (150, 150),
    batch_size = 10,
    class_mode = 'categorical'
)

class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs = {}):
    if(logs.get('accuracy') > 0.99):
      print('\nAkurasi mencapai 99%')
      self.model.stop_training = True

callbacks = myCallback()

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(16, (3, 3), activation = 'relu', input_shape = (150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(32, (3, 3), activation = 'relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation = 'relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(200, activation = 'relu'),
    tf.keras.layers.Dropout(0.3,seed=112),
    tf.keras.layers.Dense(500, activation = 'relu'),
    tf.keras.layers.Dropout(0.5,seed=112),
    tf.keras.layers.Dense(2, activation = 'sigmoid')
])

model.summary()

model.compile(loss = 'categorical_crossentropy',
              optimizer = 'Adam',
              metrics = ['accuracy'])

history = model.fit(
    train_generator,
    steps_per_epoch = 6,
    epochs = 25,
    validation_data = val_generator,
    validation_steps = 1,
    verbose = 1,
    callbacks = [callbacks]
)

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

plt.plot(epochs, acc, 'r', label = 'Training Accuracy')
plt.plot(epochs, val_acc, 'b', label = 'Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.legend(loc = 'best')
plt.show()

plt.plot(epochs, loss, 'r', label = 'Training Accuracy')
plt.plot(epochs, val_loss, 'b', label = 'Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.legend(loc = 'best')
plt.show()

import numpy as np
from keras.preprocessing import image
from tensorflow.keras.utils import img_to_array
from google.colab import files
import keras
import tensorflow as tf

uploaded = files.upload()

for fn in uploaded.keys():

  #predicting images
  path = fn
  img = tf.keras.preprocessing.image.load_img(path, target_size = (150, 150))
  imgplot = plt.imshow(img)
  img_pixel = img_to_array(img)
  img_test  = np.expand_dims(image.img_to_array(img), axis = 0)

  images = np.vstack([img_test])
  classes = model.predict(images, batch_size = 100)

  print(fn)

  class_list = os.listdir(train_dir)

  for j in range(42):
    if classes[0][j] == 1. :
      print('This image belongs to class', class_list[j-1])
      break