'''
Author: Corey Lynch
Date: 10/21/12

python afinn_classifier.py username pass
'''

import tweetstream
import string
import sys

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
	with tweetstream.SampleStream(sys.argv[1],sys.argv[2]) as stream:
		for tweet in stream:
			if 'text' in tweet.keys() and len(tweet['text'])>0:
				try:
					no_punct = normalize(tweet['text'])
					if no_punct!=None and any([i.lower() in queries for i in no_punct.split()]):
						#print no_punct
						val = sum([afinn[i] if i in afinn else 0 for i in no_punct.split()])
						if val<-2 or val>2:
							if any([i in ['romney','mitt'] for i in no_punct.split()]):
								romney+=1
							if any([i in ['romney','mitt'] for i in no_punct.split()]):
								obama+=1
							print no_punct
							print val
				except UnicodeEncodeError:
					pass	



