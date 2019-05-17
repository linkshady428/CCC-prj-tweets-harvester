import tweepy
import json
import sys

# key and secret.
consumer_key = str(sys.argv[1])
consumer_secret = str(sys.argv[2])
access_token = str(sys.argv[3])
access_token_secret = str(sys.argv[4])

# provide the key and secret.
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# get the info. with 'wait_on_rate_limit=True' to automatically wait for rate limits to replenish.
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
# ----------------------------------------------------------------------------------
# search old tweets of a users.

id_val = sys.argv[5]
filename ='all_tweets_of_'+id_val+'.json'
file = open(filename, 'a')
total_tweet_num = 0
print('start search tweets')

for page in tweepy.Cursor(api.user_timeline, id=id_val, tweet_mode='extended', lan='en', count=9999).pages():
    tweet_num = 0
    for tweet in page:
        tweet_num += 1
        json_str = tweet._json
        data = {'time': str(tweet.created_at), 'user_id':id_val, 'tweet_id': json_str['id'], 'text': str(tweet.full_text)}
        # print(data)
        json.dump(data, file)
        file.write('\n')
        file.flush()
    total_tweet_num += tweet_num
    print(id_val, ' Tweets num:', tweet_num)
print('Total tweets:', total_tweet_num)

