import easygui as gui
from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError
from urllib.parse import urljoin
import pickle
import os
import time


URL = 'https://www.xkcd.com'


def get_image(count=1):
    img_url = urljoin(URL, str(count))
    while True:
        try:
            req = requests.get(img_url)
        except ConnectionError:
            print('Error occurred. Trying again in 30s.')
            time.sleep(30)
            continue
        break
    if req.status_code == 404:
        print('No More Comics')
        return False

    soup = BeautifulSoup(req.text, 'lxml')
    comic = soup.find(attrs={'id': 'comic'})
    image = {
        'number': count,
        'title': comic.img.get('title'),
        'link': urljoin('https:', comic.img.get('src')),
        'format': comic.img.get('src').split('.')[-1]
    }
    req = requests.get(image['link'], stream=True)
    filename = 'temp.' + image['format']
    with open(filename, 'wb') as temp:
        for chunk in req.iter_content(chunk_size=1024 * 256):
            temp.write(chunk)
    return image


def show_image(image_data):
    file = 'temp.' + image_data['format']
    options = ['Favorite', 'Next', 'Close']
    title = 'www.xkcd.com/{}/'.format(image_data['number'])
    message = image_data['title']
    select = gui.buttonbox(
        title=title,
        choices=options,
        image=file,
        msg=message)
    return select


def main():
    if os.path.isfile('metadata.pkl'):
        data = pickle.load(open('metadata.pkl', 'rb'))
    else:
        data = {
            'LastComicPage': 0,
            'FavoriteComics': set(),
            'SharedComics': set(),
            'ComicLimit': 1863,
        }
    count = data['LastComicPage'] + 1
    while True:
        image = get_image(count)
        if not image:
            data['ComicLimit'] = count
            data['LastComicPage']
            msg = 'No More Comics at the moment.\n'
            msg += 'Do you want to start from first comic.'
            title = 'Sorry'
            options = ['Yes', 'No', 'Close']
            select = gui.buttonbox(
                msg=msg, title=title, choices=options, cancel_choice='Close')
            if select == 'Close':
                quit()
            elif select == 'Yes':
                data['LastComicPage'] = count = 1
                image = get_image(count)
            elif select == 'No':
                msg = 'Nothing else i can do.'
                title = 'Sorry'
                gui.msgbox(msg=msg, title=title)
                quit()

        opt = show_image(image)
        count += 1
        if opt == 'Close':
            break
        elif opt == 'Favorite':
            if count - 1 in data['FavoriteComics']:
                msg = 'This image is already in your favorites.'
                title = 'File Exists.'
                gui.msgbox(msg=msg, title=title)
            else:
                from_file = 'temp.' + image['format']
                to_file = image['title'] + '.' + image['format']
                path = os.path.expanduser('~')
                path = os.path.join(path, 'Pictures', 'xkcd')
                to_file = os.path.join(path, to_file)
                if not os.path.isdir(path):
                    os.makedirs(path)
                os.rename(from_file, to_file)
                data['FavoriteComics'].add(count - 1)
        elif opt == 'Next':
            continue
    data['LastComicPage'] = count - 1
    if os.path.isfile('metadata.pkl'):
        os.remove('metadata.pkl')
    with open('metadata.pkl', 'wb') as meta:
        pickle.dump(data, meta)


main()
