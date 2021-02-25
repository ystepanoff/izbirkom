from selenium import webdriver
import time
from PIL import Image
import glob
import os
from imgcat import imgcat
from collections import defaultdict

need = 1000 # How many captcha samples do we need? 
driver = webdriver.Firefox()

while need > 0:
    try:
        driver.get('http://www.vybory.izbirkom.ru/region/izbirkom?action=show&vrn=100100020769552')
        time.sleep(0.5)
        with open('samples/' + str(need) + '.png', 'wb') as file:
            file.write(driver.find_element_by_xpath('//*[@id="captchaImg"]').screenshot_as_png)
        need -= 1
    except:
        pass
    
driver.close()

counts = defaultdict(int)
images = glob.glob('samples/*.png')
for image in images:
    img = Image.open(image)
    img = img.convert('P')
    img_bw = Image.new('P', img.size, 255)

    # works only in iTerm2 (macOS, not in tmux) or kitty
    # TODO: add an alternative preview method for other platforms 
    imgcat(img)
    value = input('> ')
    path = 'all_digits/' + image.split('.')[0].split('/')[1] + '/'

    for x in range(img.size[1]):
        for y in range(img.size[0]):
            px = img.getpixel((y, x))
            if px != 0:
                img_bw.putpixel((y, x), 0)
        
    img_bw.save(image)

    in_digit, found_digit = False, False
    start, end = 0, 0
    count = 0
    digits = []
    name_slice = 0

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
                if px != 255:
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
            try:
                os.mkdir(path)
            except:
                pass
            im1.save(path + str(name_slice) + '.png')
            name_slice += 1
            
            im1.save('digits/' + value[i] + '/' + str(counts[int(value[i])]) + '.png')
            counts[int(value[i])] += 1
