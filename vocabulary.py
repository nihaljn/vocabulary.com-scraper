'''
    Module to get definition of single word from `www.vocabulary.com`
'''

import argparse
import requests
from bs4 import BeautifulSoup

def get_definition(word):
    '''Returns definition of `word` if found, else returns None'''
    url = f'http://www.vocabulary.com/definition/{word}'
    src = requests.get(url).content
    soup = BeautifulSoup(src, 'lxml')
    try:
        # tag and class for definition of the word
        definition = soup.find_all('p', class_='short')[0].text
        return definition
    except IndexError:
        print('Page not found.')
        return None
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--word', help='word to find the meaning of')
    args = parser.parse_args()
    print(args.word)
    definition = get_definition(args.word)
    if definition:
        print(definition)