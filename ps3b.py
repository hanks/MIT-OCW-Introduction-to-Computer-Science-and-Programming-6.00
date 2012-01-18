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

def subStringMatchExact(target, key):
    result = []
    index = 0
    while target.find(key, index) != -1:
        pos = target.find(key, index)
        result.append(pos)
        index = pos + len(key)
    return tuple(result)

#print subStringMatchExact("atgacatgcacaagtatgcat","a")        


    
