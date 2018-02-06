#Michael Esposito
#Network Defense 2
#Homework 2

import sys
import getopt
import hashlib
import random
wordlist = "wordlist.txt" #is 3870 words long
seed = 0
total_words = 0


#create three numbers, pull from wordlist

#num1 is a seeded random number generator that picks a number from 0 to 


#wordlist from https://github.com/OliverCollins/Oxford-3000-Word-List
def get_word(wordlist, num):
    global total_words
    if num == 0:
        num = 1
    elif num >  total_words:
        num = total_words

    f = open(wordlist, 'r')
    for i in range(num):
        temp = f.readline()
    f.close()
    return temp.rstrip()

def get_wordlist_length(wordlist):
    num_lines = 0
    f = open(wordlist, 'r')
    for line in f:
        num_lines = num_lines + 1
    return num_lines

#random word from wordlist from given seed
def get_word_1(wordlist, seed):
    random.seed(seed)
    rand_int = random.randint(0, total_words)
    return get_from_wordlist(wordlist, rand_int)

#create md5 hash, sum ASCII, get from wordlist
def get_word_2(wordlist, seed):
    sha_hash = hashlib.md5(str(seed))
    temp = str(sha_hash.hexdigest())
    total = 0
    for char in temp:
        total = total + ord(char)
    print total
    return get_word(wordlist, total)



def main(argv):
    global total_words
    total_words = get_wordlist_length(wordlist) 
    for x in range(0, 20):
        print get_word_2(wordlist, x)


if __name__ == "__main__":
    main(sys.argv[1:])


