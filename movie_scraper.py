from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from termcolor import colored
from progress.bar import Bar
import csv
from texttable import Texttable

TIME = 1

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
chrome_options.add_experimental_option("detach", True)

genre = input(colored('Enter Genre: ', 'green'))
url = f'https://www.imdb.com/search/title/?genres={genre}'

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

data = driver.find_elements_by_xpath(
    '//div[@class="lister-item mode-advanced"]')
length = len(data)
total = 1

movies = []
page = url

current_page = 1
page_amount = 5

id_temp = 1

bar = Bar('Processing Pages...', max=page_amount, suffix='%(percent)d%%')
while current_page <= page_amount:
    driver.get(page)
    for i in range(1, length+1):
        id = id_temp
        movie = driver.find_element_by_xpath(
            f'//*[@id="main"]/div/div[3]/div/div[{i}]/div[3]/h3/a').text
        year = driver.find_element_by_xpath(
            f'//*[@id="main"]/div/div[3]/div/div[{i}]/div[3]/h3/span[2]').text
        try:
            genre = driver.find_element_by_xpath(
                f'//*[@id="main"]/div/div[3]/div/div[{i}]/div[3]/p[1]/span[5]').text.strip()
        except NoSuchElementException:
            genre = 'N/A'
        try:
            rating = driver.find_element_by_xpath(
                f'//*[@id="main"]/div/div[3]/div/div[{i}]/div[3]/div/div[1]/strong').text
        except NoSuchElementException:
            rating = 'N/A'
        try:
            certificate = driver.find_element_by_xpath(
                f'//*[@id="main"]/div/div[3]/div/div[{i}]/div[3]/p[1]/span[1]').text
            if len(certificate) > 8:
                certificate = 'N/A'
            if certificate[0] == '1':
                certificate = 'N/A'
        except NoSuchElementException:
            certificate = 'N/A'
        link = driver.find_element_by_xpath(
            f'//*[@id="main"]/div/div[3]/div/div[{i}]/div[3]/h3/a').get_attribute("href")

        movies.append((id, movie, year, genre, rating, certificate, link))
        id_temp += 1

    page = url + f'&start={length+total}&ref_=adv_nxt'
    total += length
    current_page += 1

    bar.next()
bar.finish()

# saving the data
with open('movies.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Title', 'Year', 'Genre',
                     'Rating', 'Certificate', 'URL'])
    writer.writerows(movies)

print(f'''
Results have been found!
csv file has been created!
''')
