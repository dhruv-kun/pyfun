from bs4 import BeautifulSoup
import requests
import argparse
import logging

LOG_FILENAME = 'codescrape.log'
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.DEBUG
)


class Problem:
    def __init__(self, p_id):
        self.p_id = p_id
        self.problem_name = None
        self.submission_link = None
        self.solution_link = None
        self.problem_link = None
        self.solution_lang = None
        self.solution_code = None

    def write_to_file(self, dst, verbose=False):

        if self.solution_lang.startswith('C++'):
            ext = '.cpp'
            comment = '/*\n{}*/\n\n'
        elif self.solution_lang.startswith('PYTH'):
            ext = '.py'
            comment = '"""\n{}"""\n\n'

        comment = comment.format(repr(self))

        filename = dst + self.p_id + ext

        with open(filename, 'w') as outfile:
            outfile.write(comment)
            outfile.write(self.solution_code)
        if verbose:
            print(self.problem_name)
            print('{} write successful.\n'.format(filename))

    def __hash__(self):
        return hash(self.p_id)

    def __repr__(self):
        stng = ""
        stng += "Problem ID: {}\n".format(self.p_id)
        stng += "Name: {}\n".format(self.problem_name)
        stng += "Problem Link: {}\n".format(self.problem_link)
        stng += "Submission Link: {}\n".format(self.submission_link)
        stng += "Solution Link: {}\n".format(self.solution_link)
        stng += "Lang: {}\n".format(self.solution_lang)
        return stng

    def __str__(self):
        stng = ""
        stng += "Problem ID: {}\n".format(self.p_id)
        stng += "Name: {}\n".format(self.problem_name)
        stng += "Problem Link: {}\n".format(self.problem_link)
        stng += "Submission Link: {}\n".format(self.submission_link)
        stng += "Solution Link: {}\n".format(self.solution_link)
        stng += "Lang: {}\n".format(self.solution_lang)
        return stng


def get_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; '
        'Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    return soup


def get_probs(user_link):
    while True:
        soup = get_soup(user_link)
        prob_sections = soup.find(
            'section', attrs={'class': 'problems-solved'})
        if prob_sections is None:
            continue
        break
    fully_solved = prob_sections.div.article.find_all('a')
    solved = set()
    for prob_id in fully_solved:
        prob = Problem(prob_id.text)
        prob.submission_link = prob_id.get('href')
        solved.add(prob)
    return solved


def download_solutions(solved, dst, verbose):
    for prob in solved:
        while True:
            soup = get_soup(URL + prob.submission_link)
            submissions = soup.find_all('tr', attrs={'class': '\\"kol\\"'})
            if submissions is None:
                continue
            break

        best_soln = None

        for i in range(len(submissions)):
            submissions[i] = submissions[i].find_all('td')
            result_row = submissions[i][3]
            tick = result_row.find('img', attrs={'src': '/misc/tick-icon.gif'})
            if tick:
                if 'pts' not in result_row.text:
                    best_soln = submissions[i]
                elif '100' in result_row.text:
                    best_soln = submissions[i]

        if best_soln is not None:
            prob.solution_link = best_soln[-1].find('a').get('href')
            prob.solution_lang = best_soln[-2].text
            prob.solution_code = download_code(prob)
            prob.write_to_file(dst, verbose)


def download_code(prob):
    while True:
        soup = get_soup(URL + prob.solution_link)
        problem_meta = soup.find(
            'div', attrs={'id': 'breadcrumb'}).find_all('a')
        ol = soup.find('ol')
        if ol is None or problem_meta is None:
            continue
        prob.problem_name = problem_meta[-2].text
        prob.problem_link = problem_meta[-2].get('href')
        code = []
        for li in ol.find_all('li'):
            code.append(li.text)
        break
    return '\n'.join(code)


def parser():
    ap = argparse.ArgumentParser(
        prog='CodeChef Solution Scraper',
        description="Downloads problem information and solution code"
        " of problems solved by the user and writes them in DIR"
    )
    ap.add_argument('-u', '--user-name', required=True,
                    help='User name of the codechef account')
    ap.add_argument('-d', '--dir', required=True,
                    help='Destination to store the code')
    ap.add_argument('-v', '--verbose',
                    help='Prints status of the problem solution')
    return ap


def main(args):
    link = "/users/" + args['user_name']
    solved = get_probs(URL + link)
    if args['verbose'] is not None:
        args['verbose'] = True
    download_solutions(solved, args['dir'], args['verbose'])

    print('Total Writes {}'.format(len(solved)))


if __name__ == '__main__':
    URL = "https://www.codechef.com"
    ap = parser()
    args = vars(ap.parse_args())
    main(args)
