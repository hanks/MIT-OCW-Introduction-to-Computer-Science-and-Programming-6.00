# Problem Set 5: Ghost
# Name: 
# Collaborators: 
# Time: 
#

import random

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print "  ", len(wordlist), "words loaded."
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq


# (end of helper code)
# -----------------------------------

# Actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program.
wordlist = load_words()
INPUT_ERROR = "error"

# TO DO: your code begins here!
def ghost():
    print "Welcome to Ghose!"
    n = 0
    player_num = n % 2 + 1
    print "Player", player_num, "goes first."
    current_word = ""
    display_current_word(current_word)

    while True:
        temp = user_input(player_num)
        if temp == INPUT_ERROR:
            print "Please input only one letter."
            continue
        else:
            current_word = current_word + temp
            display_current_word(current_word)
            res = is_lose(current_word, wordlist)
            if res == NO_PREFIX:
                print "Player %d loses because no word begins with '%s'" % (player_num, current_word)
                n = n + 1
                print "Player %d winds!" % (n % 2 + 1)
                break
            elif res == IS_A_WORD:
                print "Player %d loses because '%s' is a word!" % (player_num ,current_word)
                n = n + 1
                print "Player %d wins!" % (n % 2 + 1)
                break
            n = n + 1
            player_num = n % 2 + 1
            print "Player " + str(player_num) + "'s turn."
            
def user_input(player_number):
    input = raw_input("Player " + str(player_number) + " says letter: ")
    print ""
    if is_valid_input(input):
        return input.lower()
    else:
        return INPUT_ERROR

def display_current_word(word):
    print "Current word fragment: '" +  word + "'"

NO_PREFIX = 1
IS_A_WORD = 0
CONTINUE = 2


def is_lose(current_word, word_list):
    lose = CONTINUE
    if current_word in word_list:
       if len(current_word) <= 3:
           lose = CONTINUE
       else:
           lose = IS_A_WORD
    else:
        if not is_prefix(current_word, word_list):
            lose = NO_PREFIX
    return lose

def is_prefix(current_word, word_list):
    if bi_search_prefix(current_word, word_list) == -1:
        return False
    else:
        return True

def bi_search_prefix(prefix, word_list):
    start = 0
    length = len(prefix)
    end = len(word_list) - 1
    mid = (start + end) / 2
    while start <= end:
        if prefix < word_list[mid][:length]:
            end = mid - 1
        elif prefix > word_list[mid][:length]:
            start = mid + 1
        else:
            return mid
        mid = (start + end) / 2
    return -1
    
def is_valid_input(input_word):
    res = False
    if input_word in string.ascii_letters:
        res = True
    return res

if __name__ == "__main__":
    ghost()
