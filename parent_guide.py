from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from termcolor import colored

TIME = 1

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
chrome_options.add_experimental_option("detach", True)

movie = input(colored('Enter Movie: ', 'green')).title()

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.imdb.com/')

search = driver.find_element_by_xpath(
    '//input[@id="suggestion-search"]').send_keys(movie)

driver.find_element_by_xpath('//button[@type="submit"]').click()

results = []
option = driver.find_element_by_xpath(
    '//*[@id="main"]/div/div[2]/table/tbody/tr[1]')

count = 1
while True:
    try:
        count += 1
        results.append(option.text)
        option = driver.find_element_by_xpath(
            f'//*[@id="main"]/div/div[2]/table/tbody/tr[{count}]')
    except NoSuchElementException:
        print('')
        print('All Results Found!')
        break

options_dict = {}

for i in range(1, len(results)):
    print(f'{i}. {results[i-1]}')
    options_dict[i] = results[i-1]
('')

option_choice = int(input(colored(f'Choose (1-{len(results)}): ', 'blue')))

print(f'{options_dict[option_choice]} Selected')
('')

try:
    driver.find_element_by_xpath(
        f'//*[@id="main"]/div/div[2]/table/tbody/tr[{option_choice}]/td[2]/a').click()
except NoSuchElementException:
    print('Movie Unavailable')

field = driver.find_element_by_xpath(
    '//*[@id="titleStoryLine"]/div[5]/span/a').get_attribute('href')

if "parentalguide" in field:
    driver.find_element_by_xpath(
        '//*[@id="titleStoryLine"]/div[5]/span/a').click()
else:
    driver.find_element_by_xpath(
        '//*[@id="titleStoryLine"]/div[6]/span/a').click()

print('')
try:
    nudity = driver.find_element_by_xpath('//section[@id="advisory-nudity"]')
    print(nudity.text)
    print('')
    violence = driver.find_element_by_xpath(
        '//section[@id="advisory-violence"]')
    print(violence.text)
    print('')
    profanity = driver.find_element_by_xpath(
        '//section[@id="advisory-profanity"]')
    print(profanity.text)
    print('')
    alcohol = driver.find_element_by_xpath('//section[@id="advisory-alcohol"]')
    print(alcohol.text)
    print('')
except NoSuchElementException:
    print('Parent Guide Elements cannot be located')
