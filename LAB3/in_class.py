import json
import requests
import os
from bs4 import BeautifulSoup

os.system('clear')


def urlExtracter(url, urls, carNames, pageNumber, lastPage="null"):
    print('page ', pageNumber)
    reqs = requests.get(url+f"?page={pageNumber}")
    soup = BeautifulSoup(reqs.text, 'html.parser')

    cars = soup.find_all('div', class_='ads-list-photo-item-title')
    if lastPage == "null":
        lastPage = soup.find('li', class_='is-last-page')
        lastPageNumber = lastPage.find('a').get(
            'href').replace("/ro/list/transport/cars?page=", "")
        lastPage = int(lastPageNumber)

    for car in cars:
        title = car.find('a').text.replace(' ', '')
        link = car.find('a').get('href')
        if ("booster" not in link) and ("recommendations" not in link):
            carNames.append(title)
            urls.append("https://999.md"+link)
            print("https://999.md"+link)

    pageNumber += 1
    if pageNumber <= lastPage:
        urlExtracter(url, urls, carNames, pageNumber, lastPage)


url = 'https://999.md/ro/list/transport/cars'
urls = []
carNames = []
fileName = "urls.json"

urlExtracter(url, urls, carNames, 1)
# print(urls)
# with open(fileName, "w") as json_file:
# json.dump(urls, json_file)

# json_file.close()
