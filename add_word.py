'''
    Module to add word to dictionary
    Dictionary is a CSV file in storage
'''

import argparse
import requests
from bs4 import BeautifulSoup
import os
import csv

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
    parser.add_argument('--name', help='export file name without extension', default='dictionary', required=False)
    args = parser.parse_args()
    print(args.word)
    definition = get_definition(args.word)
    if definition:
        print(definition)
        path = os.path.join('csv_files', args.name+'.csv')
        with open(path, 'a') as file:
            csv_writer = csv.writer(file)
            row = [args.word, definition]
            csv_writer.writerow(row)
    else:
        print('Word not found.')