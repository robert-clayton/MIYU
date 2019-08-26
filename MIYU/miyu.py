#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup as bs
import pandas
import json
import os

url = 'https://old.reddit.com/r/aww.json'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}

response = requests.get(url, headers=headers)
print(response.json())


with open(os.path.join(os.getcwd(), 'Test.json'), 'w') as f:
    json.dump(response.json(), f, indent=4)


# soup = bs(page.text, 'html.parser')

# domains = soup.find_all('span', class_='domain')

# print(domains)
def main():
    # do things
    pass

if __name__ == '__main__':
    main()