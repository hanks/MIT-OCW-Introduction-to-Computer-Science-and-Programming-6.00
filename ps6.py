# Problem Set 5: 6.00 Word Game
# Name: 
# Collaborators: 
# Time: 
#

import random
import string
import time
import sys

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 15
TIME_LIMIT = 0.0
SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

timeRemaining = 0.0

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

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

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    The score for a word is the sum of the points for letters
    in the word, plus 50 points if all n letters are used on
    the first go.

    Letters are scored as in Scrabble; A is worth 1, B is
    worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string (lowercase letters)
    returns: int >= 0
    """
    # TO DO ...
    score = 0
    length = len(word)
    if length == n:
        score = 50
    for letter in word:
        score += SCRABBLE_LETTER_VALUES[letter]
    return score


def get_word_score_by_time(word, n, time):
    score = 0.0
    length = len(word)
    if length == n:
        score = 50
    for letter in word:
        score += SCRABBLE_LETTER_VALUES[letter]
    if time == 0.00:
        time = 0.5
    score = score / time
    return score

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    print "Current Hand: ",
    for letter in hand.keys():
        for j in range(hand[letter]):
            print letter,              # print all on the same line
    print                              # print an empty line

#
# Make sure you understand how this function works and what it does!
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    num_vowels = n / 3
    
    for i in range(num_vowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(num_vowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not mutate hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    # TO DO ...
    res = dict(hand)
    for letter in word:
        res[letter] = res.get(letter) - 1
    return res

def pick_best_word(hand, points_dict):
    """
    Returns the word which has the highest score in the hand
    
    Returns '.' if no words can be made with the given hand

    hand: dictionary
    points_dict: dictionary
    returns: string
    """
    highest_score = 0
    word_high = "."
    for word in points_dict.keys():
        fre_temp = get_frequency_dict(word)
        if is_sub_dict(hand, fre_temp):
            if points_dict[word] > highest_score:
                word_high = word
                highest_score = points_dict[word]
    return word_high

def is_sub_dict(src, target):
    sub_dict = False
    for letter in target.keys():
        if (letter in src) and (target[letter] <= src[letter]):
            sub_dict = True
        else:
            sub_dict = False
            break
    return sub_dict


#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, points_dict):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
    
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    """
    # TO DO ...
    res = False
    tempHand = dict(hand)
    for letter in word:
        if tempHand.has_key(letter):
            tempHand[letter] = tempHand.get(letter) - 1
            if tempHand[letter] < 0:
                res = False
                return res
        else:
            res = False
            return res
    if word in points_dict:
        res = True
    return res

totalScore = 0.0
#
# Problem #4: Playing a hand
#
def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * When a valid word is entered, it uses up letters from the hand.

    * After every valid word: the score for that word and the total
      score so far are displayed, the remaining letters in the hand 
      are displayed, and the user is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing a single
      period (the string '.') instead of a word.

    * The final score is displayed.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
    """
    global timeRemaining
    global TIME_LIMIT
    global time_limit
#    timeRemaining = float(raw_input("Enter time limit, in seconds, for players: "));
    timeRemaining = time_limit
    TIME_LIMIT = timeRemaining
    display_hand(hand)
    n = sum(hand.values())
    global totalScore
    (userInput, total_time) = user_input(hand)
    global points_dict

    while True:
        if userInput == ".":
            print "Total score: %0.2f points." % (totalScore)
            break
        if not is_valid_word(userInput, hand, points_dict):
            print "Invalid word, please try again."
            display_hand(hand)
            (userInput, total_time) = user_input(hand)
        else:
            wordScore = get_word_score_by_time(userInput, n, total_time)
            totalScore = totalScore + wordScore
            print "%s earned %0.2f points. Total score: %0.2f points." % (userInput, wordScore, totalScore)
            hand = update_hand(hand, userInput)
            if sum(hand.values()) == 0:
                print "Total score: %0.2f points." % (totalScore)
                break
            display_hand(hand)
            (userInput, total_time) = user_input(hand)



def user_input(hand):
    start_time = time.time()
   #userInput = raw_input("Enter word, or a . to indicate that you are finished: ")
    global points_dict
   #use a robot input method 
    userInput = pick_best_word_faster(hand, points_dict)
    end_time = time.time()
    total_time = end_time - start_time
    print "It took %0.2f seconds to provide an answer." % total_time
    global timeRemaining 
    timeRemaining = timeRemaining - total_time
    global totalScore
    if timeRemaining <= 0:
        print "Total time exceeds %0.2f seconds. Your scored %0.2f score" % (TIME_LIMIT, totalScore)
        sys.exit()
    print "You have %0.2f seconds remaining." % timeRemaining
    return (userInput, total_time)
            
#
# Problem #5: Playing a game
# Make sure you understand how this code works!
# 
def play_game(word_list):
    """
    Allow the user to play an arbitrary number of hands.

    * Asks the user to input 'n' or 'r' or 'e'.

    * If the user inputs 'n', let the user play a new (random) hand.
      When done playing the hand, ask the 'n' or 'e' question again.

    * If the user inputs 'r', let the user play the last hand again.

    * If the user inputs 'e', exit the game.

    * If the user inputs anything else, ask them again.
    """
    ## uncomment the following block of code once you've completed Problem #4
    hand = deal_hand(HAND_SIZE) # random init
    global totalScore
    while True:
        cmd = raw_input('Enter n to deal a new hand, r to replay the last hand, or e to end game: ')
        if cmd == 'n':
            hand = deal_hand(HAND_SIZE)
            play_hand(hand.copy(), word_list)
            print
        elif cmd == 'r':
            totalScore = 0.0
            play_hand(hand.copy(), word_list)
            print
        elif cmd == 'e':
            break
        else:
            print "Invalid command."

points_dict = {}
time_limit = 0.0

def get_time_limit(points_dict, k):
    """
    Return the time limit for the computer player as a function of the
    multiplier k.

    point_dict should be the same dictionary that is created by 
    get_words_to_points.
    """
    start_time = time.time()
    # Do some computation. The only purpose of the computation is so we
    # can figure out how long your computer takes to perform a known task.
    for word in points_dict:
        get_frequency_dict(word)
        get_word_score(word, HAND_SIZE)
    end_time = time.time()
    return (end_time - start_time) * k

rearrange_dict = {}
def get_word_rearrangements(word_list):
    global rearrange_dict
    for word in word_list:
        temp = []
        for letter in word:
            temp.append(letter)
        temp.sort()
        rearrange_dict[string.join(temp,"")] = word

def pick_best_word_faster(hand, rearrange_dict):
    hand_string = dicToString(hand)
    word_high = "."
    score_high = 0
    for indexI in range(len(hand_string)):
        for indexJ in range(len(hand_string)):
            temp_string = hand_string[indexI : indexJ]
            if temp_string in rearrange_dict:
                if points_dict[rearrange_dict[temp_string]] > score_high:
                    word_high = rearrange_dict[temp_string]
                    score_high = points_dict[word_high] 
    return word_high

def dicToString(hand):
    hand_string = []
    for letter in hand.keys():
        for times in range(hand[letter]):
            hand_string.append(letter)
    return string.join(hand_string, "")

def get_words_to_points(word_list):
    global points_dict
    score = 0
    for word in word_list:
        for letter in word:
            score += SCRABBLE_LETTER_VALUES[letter]
        points_dict[word] = score
        score = 0
    return points_dict
    

#
# Build data structures used for entire session and play game
#

if __name__ == '__main__':
    word_list = load_words()
    points_dict = get_words_to_points(word_list)
    rearrange_dict = get_word_rearrangements(word_list)
    time_limit = get_time_limit(points_dict, 5)
    play_game(word_list)

