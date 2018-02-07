#Michael Esposito
#Network Defense 2
#Homework 2

import sys
import getopt
import hashlib
import random
wordlist = "wordlist.txt" #is 3870 words long
tlds = ['com', 'net', 'org', 'ru', 'cn', 'tv']
seed = 0
total_words = 0


#create three numbers, pull from wordlist

#word1 - randomly-generated word from wordlist
#word2 - word on line in wordlist equal to sum of ASCII values in MD5 hash
#word3 - word on line in wordlist equal to sum of ASCII values / 2 in MD5 hash
#tld   - ASCII val of first letter in word 1 mod 6

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
    return get_word(wordlist, rand_int)

#create md5 hash, sum ASCII, get from wordlist
def get_word_2(wordlist, seed):
    md5_hash = hashlib.md5(str(seed))
    temp = str(md5_hash.hexdigest())
    total = 0
    for char in temp:
        total = total + ord(char)
    #print total
    return get_word(wordlist, total)

def get_word_3(wordlist, word2):
    md5_hash = hashlib.md5(word2)
    temp = str(md5_hash.hexdigest())
    total = 0
    for char in temp:
        total = total + ord(char)
    return get_word(wordlist, total/2)

def get_tld(tlds, word1):
    temp = ord(word1[0]) % len(tlds)
    return tlds[temp]

def generate_domain(wordlist, seed, total_words):
    word1 = get_word_1(wordlist, seed)
    word2 = get_word_2(wordlist, seed)
    word3 = get_word_3(wordlist, word2)
    tld = get_tld(tlds, word1)
    return word1 + word2 + word3 + '.' + tld

def usage():
    print "\nEsposito_dga.py\n\tA wrapper program to run the DGA function\n\n\t-h | --help\tThis message\n\t--date\t\tThe date to generate for\n\t--count\t\tThe number of entries to generate (default: 10)\n"

def main(argv):
    global total_words
    total_words = get_wordlist_length(wordlist) 

    try:
        opts,args = getopt.getopt(argv, "h", ["help", "date=", "count="])
    except getopt.GetoptError:
        usage()
        sys.exit()
    
    date = ''
    count = 10
    
    for opt,arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("--date"):
            date = arg
        elif opt in ("--count"):
            count = int(arg)
        else:
            assert False, "unhandled option"

    if date:
        for i in range(0,count):
            seed = int(date) + i
            print generate_domain(wordlist, seed, total_words)
    else:
        usage()
        sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])


