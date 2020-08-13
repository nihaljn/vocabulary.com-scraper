'''
    Module to get an entire word list with list definition, list description and vocabulary.com defitinition
    for each word of the list.
    Word list with mentioned attributes is collected in a dictionary file and stored in json and csv files.
'''

import requests
from bs4 import BeautifulSoup
import vocabulary
import argparse
import pprint
import json
import os
import csv

def str2bool(v):
    '''Utility function to convert str CLA to bool'''
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def get_list(list_no, verbose=False):
    '''Returns a list of dict objs representing the word list defined by `list_no` on vocabulary.com'''
    url = f'https://www.vocabulary.com/lists/{list_no}'
    src = requests.get(url).content
    soup = BeautifulSoup(src, 'lxml')
    dictionary = []
    cnt = 0
    # all word definitions are stored as unordered list elements
    soups = soup.find_all('li')
    for soup in soups:
        # li element has class 'entry' for each word in the list
        if 'class' in soup.attrs and 'entry' in soup['class']:
            # attribute for the word
            word = soup['word']
            if verbose:
                print(f'Processing {word}...', end=' ', flush=True)
            # link to vocabulary.com defition
            # vocab_com_link = soup.find('a')['href']
            # div class for definition
            list_def = soup.find(class_='definition')
            # div class for description
            list_desc = soup.find(class_='description')
            # make the entry in the dictionary
            entry = {}
            entry['id'] = cnt + 1
            cnt += 1
            entry['word'] = word
            if list_def:
                entry['list_definition'] = list_def.text
            if list_desc:
                entry['list_description'] = list_desc.text
            # get vocabulary.com definition
            vocab_definition = vocabulary.get_definition(word)
            if vocab_definition:
                entry['verbose_definition'] = vocab_definition
            if verbose:
                print('Done.', flush=True)
            dictionary.append(entry)
    return dictionary
                
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--list_no', help='public list number as in url of vocabulary.com')
    parser.add_argument('--verbose', help='show detailed progess', type=str2bool)
    parser.add_argument('--name', help='export file name without extension')
    args = parser.parse_args()
    word_list = get_list(args.list_no, args.verbose)
    pp = pprint.PrettyPrinter()
    pp.pprint(word_list)
    print(f'Processed {len(word_list)} words.')
    path = os.path.join('json_files', args.name+'.json')
    json_file = None
    with open(path, 'w') as file:
        json.dump(word_list, file)
    json_file = json.load(open(path, 'r'))
    path = os.path.join('csv_files', args.name+'.csv')
    with open(path, 'w') as file:
        csv_writer = csv.writer(file)
        cnt = 0
        for row in json_file:
            if cnt == 0:
                header = row.keys()
                csv_writer.writerow(header)
                cnt += 1
            csv_writer.writerow(row.values())