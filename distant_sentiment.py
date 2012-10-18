"""
Author: Corey Lynch
Date: 5/9/12

This builds positive, negative, and 'regular' word frequency distributions from twitter.

emoticon-counting script taken from: http://bit.ly/K2iW7l
"""

import re
import tweetstream
import redis
from spelling_corrector import correct
import string

# Emoticon
eyes = ['\:',';','=']
noses = ['',' ','-','\^','~']
smiles = ['\)','\]','}']
frowns = ['\(','\[','{']
regular = ['\|']

def emoticons(eyes,noses,mouths):
    """Creates all possible combinations of face features for emoticons"""
    
    faces = []
    
    for eye in eyes:
        for nose in noses:
            for mouth in mouths:
                faces.append(eye+nose+mouth)
                
    return faces


basic_positive = emoticons(eyes,noses,smiles)
basic_negative = emoticons(eyes,noses,frowns)
basic_regular = emoticons(eyes,noses,regular)

pos_str = '|'.join(basic_positive)
neg_str = '|'.join(basic_negative)
reg_str = '|'.join(basic_regular)

# Build english dictionary
with open('wordsEn.txt') as word_file:
	english_words = set(word.strip().lower() for word in word_file)

def is_english_word(word):
	return word.lower() in english_words

def normalize(s):
	ret = s
	for p in string.punctuation:
		ret = ret.replace(p, '')
	return ret

# Set up redis
r_server = redis.Redis("localhost")


# Get top values
def get_top(redis_db,n):
	top = sorted(zip([int(i) for i in r_server.hgetall(redis_db).values()],r_server.hgetall(redis_db).keys()),reverse=True)
	return top[0:n]

if __name__ == "__main__":

	with tweetstream.SampleStream('USERNAME','PASSWORD') as stream:
		for tweet in stream:
			if 'text' in tweet.keys() and len(tweet['text'])>0:
				try:
					tweet['text'].decode('ascii')
					m_pos = re.findall(pos_str,tweet['text'])
					m_neg = re.findall(neg_str,tweet['text'])
					m_reg = re.findall(reg_str,tweet['text'])
					if len(m_neg)>0 and len(m_pos)==0 and len(m_reg)==0:
						no_punct = normalize(tweet['text'])
						if no_punct!=None:
							for i in tweet['text'].split():
								word = i.lower()
								word = correct(word)
								if is_english_word(word):
									print 'Insert NEG: %s' % word
									r_server.hincrby('FREQ_DIST_NEG',word,1)
					elif len(m_pos)>0 and len(m_neg)==0 and len(m_reg)==0:
						no_punct = normalize(tweet['text'])
						if no_punct!=None:
							for i in tweet['text'].split():
								word = i.lower()
								word = correct(word)
								if is_english_word(word):
									print 'Insert POS: %s' % word
									r_server.hincrby('FREQ_DIST_POS',word,1)
					elif len(m_reg)>0 and len(m_pos)==0 and len(m_neg)==0:
						no_punct = normalize(tweet['text'])
						if no_punct!=None:
							for i in tweet['text'].split():
								word = i.lower()
								word = correct(word)
								if is_english_word(word):
									print 'Insert REG: %s' % word
									r_server.hincrby('FREQ_DIST_REG',word,1)
	
				except UnicodeEncodeError:
					pass
			
