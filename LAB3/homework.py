import requests
import os
from bs4 import BeautifulSoup

os.system('clear')


def infoExtracter(url, info):
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    title = soup.find('h1').text
    user = soup.find('a', class_='adPage__aside__stats__owner__login').text
    price = soup.find(
        'span', class_='adPage__content__price-feature__prices__price__value').text + "€"
    description = soup.find(
        'div', class_='adPage__content__description grid_18').text
    regions = soup.find_all('dd', itemprop='address')
    particularities = soup.find(
        'div', class_='adPage__content__features__col grid_7 suffix_1').find_all('li', class_='m-value')
    generalThings = soup.find(
        'div', class_='adPage__content__features__col grid_9 suffix_1').find_all('li', class_='m-value')
    location = ''
    for region in regions:
        location = location + region.text.replace(" ", "")
    info.update({"titlul": title})
    info.update({"user": user})
    info.update({"pretul": price})
    info.update({"locatia": location})
    for particularity in particularities:
        contentKey = particularity.find(
            'span', class_='adPage__content__features__key').text.strip()
        contentValue = particularity.find(
            'span', class_='adPage__content__features__value').text.strip()
        info.update({contentKey: contentValue})
    for general in generalThings:
        contentKey = general.find(
            'span', class_='adPage__content__features__key').text.strip()
        contentValue = general.find(
            'span', class_='adPage__content__features__value').text.strip()
        info.update({contentKey: contentValue})
    info.update({"descrierea": description})
    for key in info:
        print(key, ":", info[key])
    # print(info)


info = {}
url = 'https://999.md/ro/84334590'
infoExtracter(url, info)
# print(urls)
