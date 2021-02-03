import tweepy
import time
import os

consumer_key=os.environ['consumer_key']
consumer_secret=os.environ['consumer_secret']
key=os.environ['key']
secret=os.environ['secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)

INTERVAL=60

def followingFollowers():
    print("Looking at followers...")
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            try:
                follower.follow()
                print("Followed!")
            except tweepy.TweepError as err:
                print(err.reason)
                time.sleep(3)

fileName='lastSeen.txt'
def readLastSeen(fileName):
    fileRead=open(fileName,'r')
    lastSeenId=int(fileRead.read().strip())
    fileRead.close()
    return lastSeenId

def storeLastSeen(fileName,lastSeenId):
    fileWrite=open(fileName,'w')
    fileWrite.write(str(lastSeenId))
    fileWrite.close()
    return 

tweets=api.mentions_timeline(readLastSeen(fileName),tweet_mode='extended')
hashtags=['cryptonewsbot3','#crypto','#bitcoin','#blockchain','#ethereum','#cryptocurrency','#btc','#eth','#binance','#forex','#money','#bitcoinmining','trading','#coinbase']

def reply():
    print("Looking at timeline...")
    for tweet in reversed(tweets):
        for tags in hashtags:
            if tags in tweet.full_text.lower():
                try:
                    print(str(tweet.id)+'-'+tweet.full_text)
                    api.update_status('@'+tweet.user.screen_name+" A Crypto News Bot at work!",tweet.id)
                    api.create_favorite(tweet.id)
                    api.retweet(tweet.id)
                    storeLastSeen(fileName,tweet.id)
                    time.sleep(10)
                except tweepy.TweepError as err:
                    print(err.reason)
                    time.sleep(3)
                except StopIteration:
                    break 

def searchBot():
    print("Searching hashtags...")
    for tweet in tweepy.Cursor(api.search,q=('#cryptonewsbot3 OR #BTC OR #Cryptocurrency OR #Bitcoin OR #Binance OR #Blockchain OR #BCH OR #ETH OR #LTC-filter:retweets'),lang="en").items(5):
        try:
            tweet.retweet()
            print("Retweeted!")
            api.create_favorite(tweet.id)
            time.sleep(10)
        except tweepy.TweepError as err:
            print(err.reason)
            time.sleep(3)
        except StopIteration:
            break

while True:
    followingFollowers()
    time.sleep(15)
    reply()
    time.sleep(15)
    searchBot()
    time.sleep(15)
    time.sleep(INTERVAL)
