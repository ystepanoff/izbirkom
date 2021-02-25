from sklearn.model_selection import train_test_split
import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Activation, BatchNormalization, AveragePooling2D
from tensorflow.keras.optimizers import SGD, RMSprop, Adam
import glob
from PIL import Image
import keras


def compile_model(width, height):
    model = Sequential()
    model.add(Dense(width * height, activation='relu', input_shape=(width * height, )))
    model.add(Dense(10, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer=RMSprop(), metrics=['accuracy'])
    return model


digits = [str(i) for i in range(10)]
dx, dy = [], []

for dir in digits:
    for image in glob.glob('digits/' + dir + '/*.png'):
        img = Image.open(image)
        img = img.resize((10, 10), Image.ANTIALIAS)
        dx.append(np.array(img))
        dy.append(dir)

dx = np.array(dx, dtype=object)
dy = np.array(dy)

train_x, test_x, train_y, test_y = train_test_split(dx, dy, test_size=0.20, random_state=42)

train_ds = np.asarray(train_x.reshape(train_x.shape[0], 10 * 10)).astype(np.int)
test_ds = np.asarray(test_x.reshape(test_x.shape[0], 10 * 10)).astype(np.int)

num_classes = 10
train_labels = keras.utils.to_categorical(train_y, num_classes)
test_labels = keras.utils.to_categorical(test_y, num_classes)

model = compile_model(10, 10)
model.fit(train_ds, train_labels, epochs=20, batch_size=32, verbose=1, validation_data=(test_ds, test_labels))

model.save_weights('captcha.model')
