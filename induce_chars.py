# coding: utf8
import os
import sys
import codecs
import numpy as np
from random import randint
from random import shuffle

OUT_PATH="./data/newsgroup/newsgroup.txt"
SOURCE_FILE="/usr/share/dict/ngerman"
OUT_ARR= []
DEBUG=False

INDUCTION_CHARS= "!%'()[]<>+,-.\/:@#$&*=?|"
PREFIX_CHARS= "'([<+-:@#$"
SUFFIX_CHARS= "!%')]>+,-.\/:&*?"
MID_CHARS= "'+,-.\/:@&*=|"
CAP_CHAR = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ'.decode("utf-8")
MIN_LEN=3

ADD_ONLY_NUM = True
ALPHANUMERIC = True
ADD_SUFFIX = True
ADD_PREFIX = True
ADD_MID_CHARS = True

#NUMBER_ONLY_FLAGS
NUM_ONLY_MAX_LEN=10
PERCENT_NUM_ENTRIES=20
PROB_DECIMAL=0.2 * 10
NUMBERS="0123456789"

#ALPHANUMERIC FLAGS
ALPHN_MAX_LEN=20
ALPHN_HYPHEN_PROB=0.1 *10
ALPHN_NUM_PROB=0.5 *10
ALPHN_ALPH_PROB=0.5 *10
ALPHN_PERCENT_NUM_ENTRIES=20

#SUFFIX,PREFIX,MID-CHAR PROB
SUFFIX_PROB = 0.1 * 10
PREFIX_PROB = 0.1 * 10
MID_CHAR_PROB = 0.1 * 10

with codecs.open(SOURCE_FILE,"r","utf-8") as f:
    words = [l.strip() for l in f]

if(DEBUG):
    words = words[:30]
print "Total Number of words:",str(len(words))
if DEBUG:
    print words
    print "------------------------------------------------------------------------"

num_sfxs = len(SUFFIX_CHARS)-1
num_prfxs = len(PREFIX_CHARS)-1
num_midch = len(MID_CHARS)-1

words_res = []

for word in words:
    wd = word
    if ADD_SUFFIX and (randint(0,9) < SUFFIX_PROB):
        wd += SUFFIX_CHARS[randint(0,num_sfxs)]

    if ADD_PREFIX and (randint(0,9) < PREFIX_PROB):
        wd = PREFIX_CHARS[randint(0,num_prfxs)] + wd

    if ADD_MID_CHARS and (randint(0,9) < MID_CHARS) and len(word) > 3:
        index = randint(1,len(word)-2)
        wd = wd[:index] + MID_CHARS[randint(0,num_midch)] + wd[index:]
    words_res.append(wd)

OUT_ARR += words_res

if ADD_ONLY_NUM:
    numeric_words = []
    num_of_entries = int(len(words)*(PERCENT_NUM_ENTRIES/100.0))
    len_nums = len(NUMBERS) -1
    for i in range(num_of_entries):
        word = ''
        word_len = randint(MIN_LEN,NUM_ONLY_MAX_LEN)
        for j in range(word_len):
            word += NUMBERS[randint(0,len_nums)]
        if(randint(0,9) < PROB_DECIMAL):
            word += "."
            for k in range(randint(1,word_len)):
                word += NUMBERS[randint(0,len_nums)]
        try:
            numeric_words.append('{:,}'.format(int(word)))
        except:
            numeric_words.append(word)
    OUT_ARR += numeric_words

if ALPHANUMERIC:
    alphn_words = []
    num_of_entries = int(len(words)*(ALPHN_PERCENT_NUM_ENTRIES/100.0))
    len_nums = len(NUMBERS)-1
    len_alpha = len(CAP_CHAR)-1
    for i in range(num_of_entries):
        word=''
        word_len = randint(MIN_LEN,ALPHN_MAX_LEN)
        for j in range(word_len):
            if(randint(0,9) < ALPHN_ALPH_PROB):
                word += CAP_CHAR[randint(0,len_alpha)]
                continue
            if(randint(0,9) < ALPHN_HYPHEN_PROB) and len(word) != 0:
                word += "-"
                continue
            if(randint(0,9) < ALPHN_NUM_PROB):
                word += NUMBERS[randint(0,len_nums)]
                continue
        if(len(word) > 2):
            #print word
            alphn_words.append(word)

    OUT_ARR += alphn_words

shuffle(OUT_ARR)

if DEBUG:
    print OUT_ARR
    print "---------------------"

if DEBUG:
    with open("alphn.txt",'w') as fp:
        for aa in OUT_ARR:
            fp.write("{}\n".format(aa.encode("utf-8")))
else:
    with open(OUT_PATH,'w') as fp:
        for aa in OUT_ARR:
            fp.write("{}\n".format(aa.encode("utf-8")))
