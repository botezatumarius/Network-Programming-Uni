import json
import os
import socket
from bs4 import BeautifulSoup

os.system('clear')


def sendReq(link):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 8080
    sock.connect((host, port))
    sock.send(f'GET {link} HTTP/1.1\r\nHost:127.0.0.1\r\n\r\n'.encode())
    response = sock.recv(1024)
    sock.close()
    return BeautifulSoup(response.decode(), 'html.parser')


def parsePage():
    productList = []
    homePageContent = sendReq('/').find('p').get_text()
    aboutPageContent = sendReq('/about').find('p').get_text()
    contactPageContent = sendReq('/contacts').find('p').get_text()
    productPage = sendReq('/products')
    for product in productPage.find_all('a'):
        href = product.get('href')[21:]
        specificProductInfo = sendReq(href).find_all('p')
        productDictionary = {}
        for info in specificProductInfo:
            content = info.get_text()
            parts = content.split(":")
            if parts[0] == "Price":
                parts[1] = float(parts[1])
            if parts[0] == "Product number":
                parts[1] = int(parts[1])
            productDictionary[parts[0]] = parts[1]
        productList.append(productDictionary)
    content = {}
    content["Home"] = homePageContent
    content["About"] = aboutPageContent
    content["Contacts"] = contactPageContent
    content["Product list"] = productList

    filePath = "parsedContent.json"
    with open(filePath, 'w') as json_file:
        json.dump(content, json_file, indent=4)


parsePage()
