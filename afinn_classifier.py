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

def is_english_word(word):
	return word.lower() in english_words

afinn = dict(map(lambda (k,v): (k,int(v)),[ line.split('\t') for line in open("AFINN/AFINN-111.txt") ]))

if __name__=='__main__':
	romney_count = 0
	obama_count = 0
	with tweetstream.SampleStream(sys.argv[1],sys.argv[2]) as stream:
		for tweet in stream:
			if 'text' in tweet.keys() and len(tweet['text'])>0:
				try:
					no_punct = normalize(tweet['text'])
					if no_punct!=None:
						val = sum([afinn[i] if i in afinn else 0 for i in no_punct.split()])
						if val<-2 or val>2:
							if any([i in ['romney','mitt'] for i in no_punct.split()]):
								romney_count+=1
								print no_punct
							if any([i in ['obama','barack'] for i in no_punct.split()]):
								obama_count+=1
								print no_punct
							print 'Obama: %s, Romney: %s' % (str(obama_count), str(romney_count))
				except UnicodeEncodeError:
					pass	



