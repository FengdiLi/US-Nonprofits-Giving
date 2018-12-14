# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 13:49:02 2018

@author: lifen
"""

# Packages Config
import tweepy
from tweepy import OAuthHandler
import pandas as pd

# Twitter API
consumer_key = 'tqXNKc7lbSSZ0n6Lc6PHql9tL'
consumer_secret = 'zKhWuZ9k3K32LTGmO6raj9NWJsX6yKHMzoqSt08XU1JcMQKM1r'
access_token = '701822223875706881-g68PHPO3RwG47KPsqUpXdaV2F17F6SB'
access_secret = 'PCWA33wkdO4JgP29eoREIw3LsN63xNxknkmkKRxSqBSGS'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth, wait_on_rate_limit = True)

# National Council of Nonprofits
user = 'UnitedWay'
status = []
time = []
old_id = None
tweets = api.user_timeline(screen_name = user, count = 200, tweet_mode="extended", exclude_replies = True, include_rts = False)
for tweet in tweets:
    status.append(tweet.full_text)
    time.append(tweet.created_at)
    old_id = tweet.id

for j in range(5):
    if old_id is not None:
        tweets = api.user_timeline(screen_name = user, count = 200, max_id = old_id, tweet_mode="extended", 
                                   exclude_replies = True, include_rts = False)
        old_id = None
        for tweet in tweets[1:]: # don't count the first duplicates
            status.append(tweet.full_text)
            time.append(tweet.created_at)
            old_id = tweet.id

df = pd.DataFrame({'text': status, 'created_at': time})
df.to_csv(user+'.csv', index = False)
user = 'fdncenter'
status = []
time = []
old_id = None
tweets = api.user_timeline(screen_name = user, count = 200, tweet_mode="extended", exclude_replies = True, include_rts = False)
for tweet in tweets:
    status.append(tweet.full_text)
    time.append(tweet.created_at)
    old_id = tweet.id

for j in range(5):
    if old_id is not None:
        tweets = api.user_timeline(screen_name = user, count = 200, max_id = old_id, tweet_mode="extended", 
                                   exclude_replies = True, include_rts = False)
        old_id = None
        for tweet in tweets[1:]: # don't count the first duplicates
            status.append(tweet.full_text)
            time.append(tweet.created_at)
            old_id = tweet.id

df2 = pd.DataFrame({'text': status, 'created_at': time})
df2.to_csv(user+'.csv', index = False)
#%%
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords 
import re

def CreateCorpus(text):
    BagOfWords=[]
    BagOfHashes=[]
    for line in text:
        tweetSplitter = TweetTokenizer(strip_handles=True, reduce_len=True)
        WordList=tweetSplitter.tokenize(line)
        regex1=re.compile('^#.+') #hashtag
        regex2=re.compile('[^\W\d]') #no non-word, no numbers
        regex3=re.compile('^http.*') #url
        regex4=re.compile('.+\..+') 
        for item in WordList:
            if(len(item)>2):
                if((re.match(regex1,item))):
                    #print(item)
                    newitem=item[1:] #remove the hash
                    BagOfHashes.append(newitem)
                elif(re.match(regex2,item)):
                    if (re.match(regex3,item) or re.match(regex4,item)):
                        pass
                    else:
                        BagOfWords.append(item)
                else:
                    pass
            else:
                pass
    BigBag=BagOfWords+BagOfHashes
    rawWord = [w for w in BigBag if w.lower() not in stop_words]
    IgnoreThese = ["there's", "we're", "we'll", "here's", "we've", "who's", "let's", "year-old", "yr-old"]
    rawWord = [w for w in rawWord if w.lower() not in IgnoreThese]
    rawWord = ' '.join(rawWord)
    return rawWord


def MostFreq(text, n):
    text = text.split()
    s = set(text)
    s = sorted(s, key=text.count, reverse = True)
    result = [w for w in text if w in s[:n]]
    result = ' '.join(result)
    return result

stop_words = set(stopwords.words('english')) 
# Most recent 1000 tweets, most frequent 500 tokens
unitedway = CreateCorpus(df.head(500)['text'])
unitedway = MostFreq(unitedway, 500)
with open('unitedway.txt', 'w') as f:
    f.write(unitedway)
    
fdcenter = CreateCorpus(df2.head(500)['text'])
fdcenter = MostFreq(fdcenter, 500)
with open('fdcenter.txt', 'w') as f:
    f.write(fdcenter)
