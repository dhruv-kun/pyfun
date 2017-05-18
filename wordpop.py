from subprocess import call
import pickle
from threading import Timer
EXPTIME = 1000 * 60 * 4 # 4 mintues.
TIMERTIME = 60 * 3 

def add_word(word_list):
    Timer(TIMERTIME, add_word).start()
    """Fetch Some word"""
    word = ""
    new_words.append(word)


def show_words(word_list):
    for word in word_list:
        call(["notify-send", word["wd"], word["def"], "-t", EXPTIME])


if __name__ == "main":

    word_file = open("word_file.pkl", 'rb')
    word_list = pickle.load(word_file)
    new_words = []
    add_word()
    word_file.close()
    show_words(word_list)

    
    


