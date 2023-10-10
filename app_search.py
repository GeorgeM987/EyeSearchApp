import requests
from bs4 import BeautifulSoup

baseURL = 'https://www.google.com'
fullURL = ''
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}

search_querry = '/search?q='
formating = 'meaning=definition'

key_word = ''.strip().lower()
key_words = ''.strip().lower()


def search(kw, kws=key_words):
    if len(kw) > 1:
        for i in str(kw).split():
            kws += i + '+'
        fullURL = f'{baseURL}{search_querry}{kws}{formating}'
    else:
        kw = kw + '+'
        fullURL = f'{baseURL}{search_querry}{kw}{formating}'

    page = requests.get(fullURL, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')
    get_main_result = soup.find(class_='hgKElc').get_text()
    return get_main_result


if __name__ == '__main__':
    search