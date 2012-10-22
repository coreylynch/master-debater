import re
import tweetstream
#import redis
from spelling_corrector import correct
import string
import csv
import pandas as pd

def normalize(s):
	ret = s
	for p in string.punctuation:
		ret = ret.replace(p, '')
	return ret

with open('wordsEn.txt') as word_file:
	english_words = set(word.strip().lower() for word in word_file)

def is_english_word(word):
	return word.lower() in english_words

afinn = dict(map(lambda (k,v): (k,int(v)),[ line.split('\t') for line in open("AFINN/AFINN-111.txt") ]))

with open('debate_queries.txt') as f:
	queries = [i.strip() for i in f.readlines()]


if __name__=='__main__':
	romney_count = 0
	obama_count = 0
	with tweetstream.SampleStream('username','password') as stream:
		for tweet in stream:
			if 'text' in tweet.keys() and len(tweet['text'])>0:
				try:
					no_punct = normalize(tweet['text'])
					if no_punct!=None:
						if True: #all(is_english_word(word) for word in no_punct.split()):
							if any([i.lower() in queries for i in no_punct.split()]):
								#print no_punct
								val = sum([afinn[i] if i in afinn else 0 for i in no_punct.split()])
								if val<-2 or val>2:
									print no_punct
									print val
				except UnicodeEncodeError:
					pass	