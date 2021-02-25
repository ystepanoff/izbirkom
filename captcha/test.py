from solve import load_model, solve_captcha
from PIL import Image
from selenium import webdriver
import time
from imgcat import imgcat

tests = 10
driver = webdriver.Firefox()
model = load_model('captcha.model')

while tests > 0:
    try:
        driver.get('http://www.vybory.izbirkom.ru/region/izbirkom?action=show&vrn=100100020769552')
        time.sleep(0.5)
        with open('test.png', 'wb') as file:
            file.write(driver.find_element_by_xpath('//*[@id="captchaImg"]').screenshot_as_png)
        img = Image.open('test.png')
        imgcat(img)
        
        print(solve_captcha(model, img))
        
        tests -= 1
    except:
        pass

driver.close() 
