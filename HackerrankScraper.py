from urllib.request import urlopen
from urllib.parse import urljoin
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from os.path import join
import time
import os
import pickle


BASE = 'https://www.hackerrank.com/domains'


def get_domains(soup):
    doms_info = soup.findAll('a', attrs={'class': 'track-tile'})
    dom_titles = []
    dom_links = []
    for dom in doms_info:
        dom_titles.append(dom.text)
        dom_links.append(dom.get('href'))
    return dict(zip(dom_titles, dom_links))


def get_subdomains(soup):
    subs_info = soup.findAll('li', attrs={'class': 'chapter-item'})
    sub_titles = []
    sub_links = []
    for sub in subs_info:
        sub_titles.append(sub.a.get('data-slug'))
        sub_links.append(sub.a.get('href'))
    return dict(zip(sub_titles, sub_links))


def get_pages(soup):
    pages_info = soup.findAll('a', attrs={'class': 'page-link'})
    page_nos = []
    page_links = []
    for page in pages_info:
        page_nos.append(page.text)
        page_links.append(page.get('href'))
    return dict(zip(page_nos, page_links))


def get_problems(soup):
    probs_info = soup.findAll('h4', attrs={'class': 'challengecard-title'})
    prob_titles = []
    prob_links = []
    for prob in probs_info:
        prob_titles.append(prob.a.text)
        prob_links.append(prob.a.get('href'))
    return dict(zip(prob_titles, prob_links))


def test1(url, name='domains', op=0):
    req = urlopen(url)
    html = req.read()
    file = open('{}.pkl'.format(name), 'wb')
    soup = BeautifulSoup(html, 'lxml')
    if op == 0:
        data = get_domains(soup)
    elif op == 1:
        data = get_subdomains(soup)
    elif op == 2:
        data = get_pages(soup)
    elif op == 3:
        data = get_problems(soup)
    pickle.dump(data, file)
    file.close()

    htm = open('{}.html'.format(name), 'w')
    htm.write(soup.prettify())
    htm.close()


def test2(name='domains'):
    file = open('{}.pkl'.format(name), 'rb')
    data = pickle.load(file)
    print(data)

# test1(urljoin(BASE, '/domains/algorithms/implementation'), 'Implementation', 2)
test2('Implementation')

