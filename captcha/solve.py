from tensorflow.keras import Sequential
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Activation, BatchNormalization, AveragePooling2D
from tensorflow.keras.optimizers import SGD, RMSprop, Adam
from PIL import Image
from imgcat import imgcat
import numpy as np


def compile_model(width, height):
    model = Sequential()
    model.add(Dense(width * height, activation='relu', input_shape=(width * height, )))
    model.add(Dense(10, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer=RMSprop(), metrics=['accuracy'])
    return model


def load_model(path):
    model = compile_model(10, 10)
    model.load_weights(path)
    return model

    
def solve_captcha(model, img):
    list_labels = []
    img_bw = Image.new('P', img.size, 0)
    img = img.convert('P')

    for x in range(img.size[1]):
        for y in range(img.size[0]):
            px = img.getpixel((y, x))
            if px == 0:
                img_bw.putpixel((y, x), 255)
        
    in_digit, found_digit = False, False
    start, end = 0, 0
    count = 0
    digits = []

    for y in range(img_bw.size[0]):
        for x in range(img_bw.size[1]):
            px = img.getpixel((y, x))
            if px != 0:
                in_digit = True
        if not found_digit and in_digit:
            found_digit = True
            start = y
        if found_digit and not in_digit:
            found_digit = False
            end = y
            digits.append((start, end))
        in_digit = False

    for i, digit in enumerate(digits):
        im0 = img_bw.crop((digit[0], 0, digit[1], img_bw.size[1]))
        im0 = im0.transpose(Image.ROTATE_90)

        digits0 = []
        for y in range(im0.size[0]):
            for x in range(im0.size[1]):
                px = im0.getpixel((y, x))
                if px == 0:
                    in_digit = True
            if not found_digit and in_digit:
                found_digit = True
                start = y
            if found_digit and not in_digit:
                found_digit = False
                end = y
                digits0.append((start, end))
            in_digit = False

        for digit in digits0:
            im1 = im0.crop((digit[0], 0, digit[1], im0.size[1]))
            im1 = im1.transpose(Image.ROTATE_270)
            im1 = im1.resize((10, 10), Image.ANTIALIAS)

            iarr = np.array(im1) / 255;
            iarr = iarr.reshape((1, 10 * 10))
            list_labels.append(np.argmax(model.predict(iarr), axis=-1))
            #list_labels.append(model.predict_classes([iarr])[0])

    return ''.join([str(s[0]) for s in list_labels])
