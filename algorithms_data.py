from urllib.parse import urljoin
from bs4 import BeautifulSoup
import os
import shutil
import requests
import time

BASE = "http://introcs.cs.princeton.edu/java/data/"

BASEDIR = os.path.abspath(os.getcwd())


def get_links():
    print('Do you want to download from')
    print(BASE)
    print('Or download data from specific link')
    option = input('All or one: ')
    if option.lower() == 'all':
        print('Getting all the links.')
        print()
        while True:
            try:
                req = requests.get(BASE)
                soup = BeautifulSoup(req.text, 'lxml')
            except Exception as e:
                print("An exception as occurred")
                print(e)
                time.sleep(10)
                continue
            del req
            break
        texttr = soup.findAll('tr', attrs={'bgcolor': '#ebebeb'})
        textinfo = []

        for tr in texttr:
            link = tr.td.a.get('href')
            link = urljoin(BASE, link)
            name = tr.td.a.text.replace('/', ' ')
            textinfo.append((link, name))

    elif option.lower() == 'one':
        link = input('Link: ')
        print()
        textinfo = [(link, link.split('/')[-1])]

    return textinfo


def write_data(textinfo):
    os.chdir(BASEDIR)
    try:
        os.mkdir('data')
    except FileExistsError:
        print('Data directory already exists.')
        choice = input('Do you want to delete it(y/n). ')
        print()
        if choice.lower() == 'y':
            shutil.rmtree('data')
            os.mkdir('data')
    os.chdir('data')

    print('Getting data.')
    print()
    for link, name in textinfo:
        while True:
            try:
                print('Getting Data: {}'.format(link))
                res = requests.head(link,
                                    headers={'Accept-Encoding': 'identity'})
                req = requests.get(link, stream=True)
            except Exception as e:
                print('An exception has occurred.')
                print(e)
                print()
                time.sleep(10)
                continue
            break

        size = res.headers['Content-Length']
        data = [name, float(size) / (1024 * 1024)]
        print('Writing Data: {}, File Size: {:04.4f}MB'.format(*data))
        print()
        with open(name, 'wb') as file:
            for chunk in req.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)


def main():

    textinfo = get_links()
    write_data(textinfo)
    print('All Done.')


main()
