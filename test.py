import requests
from bs4 import BeautifulSoup

baseURL = 'https://www.google.com'
fullURL = ''
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}

search_querry = '/search?q='
formating = 'meaning=definition'

key_word = input('give me a key-word: ').strip().lower()
key_words = ''.strip()

if len(key_word) > 1:
    for i in str(key_word).split():
        key_words += i + '+'
    fullURL = f'{baseURL}{search_querry}{key_words}{formating}'
else:
    key_word = key_word + '+'
    fullURL = f'{baseURL}{search_querry}{key_word}{formating}'

page = requests.get(fullURL, headers=header)
soup = BeautifulSoup(page.content, 'html.parser')
get_main_result = soup.find(class_='hgKElc').get_text()

print(f'you were searching for {key_word} with the result of \n\n{get_main_result}')

