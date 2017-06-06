from  bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.error import HTTPError
import pickle
import sqlite3
from copy import deepcopy
from time import sleep

BASE = "https://www.codechef.com/problems/school"


def get_soup(url):
    while True:
        try:
            req = urlopen(url)
        except HTTPError as e:
            print()
            print("An error has occurred.", e)
            print("Waiting 10 seconds to retry.")
            sleep(10)
            continue
        break
    print('Retry successful.')
    print()
    soup = BeautifulSoup(req.read(), 'lxml')
    return soup


def get_types(soup):
    type_soups = soup.find('div', attrs={'c4s_topmenu'})
    types = []
    type_links = []
    for ty in type_soups.findAll('li'):
        types.append(ty.a.text)
        type_links.append(ty.a.get('href').split('/')[-2])
    return types, type_links


def get_problems(soup):
    problemrows = soup.findAll('tr', attrs={'class': 'problemrow'})
    ln = len(problemrows)
    allproblems = dict()
    problem = dict(name='', code='', successfulSubmission='', accuracy='')
    for i, row in zip(range(ln), problemrows):
        tds = row.findAll('td')
        problem['name'] = tds[0].text.strip('\n')
        problem['code'] = tds[1].text.strip('\n')
        problem['successfulSubmission'] = tds[2].text.strip('\n')
        problem['accuracy'] = tds[3].text.strip('\n')
        allproblems[i] = deepcopy(problem)
    return allproblems


def database_store():
    file = open('codechef.pkl', 'rb')
    all_data = pickle.load(file)
    db = sqlite3.connect('codechef.db')
    cursor = db.cursor()
    for ty in all_data.keys():
        tableSql = """CREATE TABLE IF NOT EXISTS {}(Id INT, Name TEXT, Code TEXT PRIMARY KEY,
    Submission INT, Accuracy REAL, Solved TEXT)
    """.format(ty)
        cursor.execute(tableSql)
        for idx in all_data[ty].keys():
            problem = all_data[ty][idx]
            name = problem['name']
            code = problem['code']
            sub = problem['successfulSubmission']
            acc = problem['accuracy']
            sql = """INSERT INTO {}(Id, Name, Code, Submission, Accuracy, Solved) 
            VALUES (?, ?, ?, ?, ?, ?)
            """
            sql = sql.format(ty)
            cursor.execute(sql, (idx, name, code, sub, acc, "No"))
        db.commit()


def update_problem(prob_type, prob_code, status='Yes'):
    db = sqlite3.connect('codechef.db')
    cursor = db.cursor()
    sql = """UPDATE {}
    SET Solved = ?
    WHERE code = ?
    """.format(prob_type)
    cursor.execute(sql, (status, prob_code, ))
    db.commit()


def main():
    print('Program Started.')
    try:
        file = open('codechef.pkl', 'rb')
    except FileExistsError:
        print('Code Chef data not exists.')
        print('Do you want to get it(y/n).')
        if 'y' == input().lower():
            all_data = dict()
            total = 0

            print('Getting all the types of problems.')
            soup = get_soup(BASE)
            types, links = get_types(soup)
            print('Got, {}'.format(', '.join(types)))
            print()

            for ty, lnk in zip(types, links):
                print('Getting problems of type', ty)
                soup = get_soup(urljoin(BASE, lnk))
                allproblems = get_problems(soup)
                total += len(allproblems)
                all_data[ty] = deepcopy(allproblems)
                print('Done for type "{}"'.format(ty))
                print('Total problems got {} for {}'.format(len(allproblems), ty))
                print()

            print('Done for all Problems.')
            print('Total problems got {}'.format(total))
            print()
            file = open('codechef.pkl', 'wb')
            pickle.dump(all_data, file)
            file.close()

            print('Testing if storage is done correctly.')
            print()
            file = open('codechef.pkl', 'rb')
            test = pickle.load(file)
            if test == all_data:
                print('Storage is done correctly.')
            else:
                print('Something went wrong.')

            print('Saving all data to database.')
            print()
            database_store()
            print('Done.')
            print()
        else:
            return
    print('Code chef data exists.')
    print('Do you want to update any problem status(y/n).')
    if 'y' == input().lower():
        print('Enter type and code of problem.')
        ty, code = input().split()
        update_problem(ty, code)
    else:
        print('Out of options :(.')


if __name__ == '__main__':
    main()
