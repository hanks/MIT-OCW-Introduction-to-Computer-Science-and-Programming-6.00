from string import *

def countSubStringMatch(target, key):
    count = 0
    temp = target
    index = -1
    while (temp.find(key)) != -1:
        index = temp.find(key)
        count = count + 1
        temp = temp[(index + len(key)):];
        print temp
    return count

def countSubStringMatchRecursive(target, key):
    count = 0
    if target.find(key) == -1:
        return count
    else:
        return countSubStringMatchRecursive(target[(target.find(key) + len(key)):], key) + 1

#print countSubStringMatchRecursive("abcdabcdabcdabcd", "bc")
