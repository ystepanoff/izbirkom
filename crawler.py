from selenium import webdriver
import selenium
from bs4 import BeautifulSoup
from PIL import Image
import time
import sys
import traceback
import pickle


sys.path.insert(1, './captcha')
from solve import load_model, solve_captcha


captcha_model = load_model('captcha/captcha.model')
main_soup = BeautifulSoup(open('main.html', encoding='latin1').read(), features='lxml')
driver = webdriver.Firefox()

data = []

for a in main_soup.find_all('a', attrs={'class': 'vibLink'}):
    url = a.attrs['href']
    params = url.split('?')[1]
    params = {x[0]: x[1] for x in [x.split('=') for x in params[1:].split('&')]}

    while True:
        try:
            while True:
                driver.get(url)
                time.sleep(0.5)
                
                try:
                    with open('captcha.png', 'wb') as file:
                        file.write(driver.find_element_by_xpath('//*[@id="captchaImg"]').screenshot_as_png)
                    img = Image.open('captcha.png')
                    captcha = solve_captcha(captcha_model, img)
                    driver.find_element_by_xpath('//*[@id="captcha"]').send_keys(captcha)
                    driver.find_element_by_xpath('//*[@id="send"]').click()
                except selenium.common.exceptions.NoSuchElementException:
                    break

            html = driver.page_source
            soup = BeautifulSoup(html, features='lxml')

            entry = {
                'vrn': params['vrn'],
                'title': a.text.encode('latin1').decode('cp1251'),
                'reports': [ ]
            }

            for a_link in soup.find_all('a'):
                if 'href' in a_link.attrs.keys():
                    if not '?' in a_link.attrs['href']:
                        continue
                    a_params = a_link.attrs['href'].split('?')[1]
                    a_params = {x[0]: x[1] for x in [x.split('=') for x in a_params[1:].split('&')]}
                    if 'type' in a_params.keys():
                        if a_params['type'] == '0':
                            continue
                        while True:
                            try:
                                driver.get(a_link.attrs['href'])
                                time.sleep(0.5)

                                report = {
                                    'type': a_params['type'],
                                    'title': a_link.text,
                                    'html': driver.page_source
                                }

                                entry['reports'].append(report)
                            except:
                                time.sleep(1.0)
                                traceback.print_exception(*sys.exc_info())
                                continue

                            break

            data.append(entry)
            with open('data.pickle', 'wb') as data_file:
                pickle.dump(data, data_file)
        except:
            time.sleep(1.0)
            traceback.print_exception(*sys.exc_info())
            continue

        break
