import tweepy
import json
import sys
import ast
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

# data1 = {'user_id': user.id, 'Place': str(user.location)}


def Update_id_list(id_list, data):
    print('Updated list')
    if not any(item['user_id'] == data['user_id'] for item in id_list):
        print(data)
        id_list.append(data)
        json.dump(data, user_file)
        user_file.write('\n')
        user_file.flush()

# search old tweets of users.
id_list = []
user_file = open('lust_user.json', 'r+')
data = {}
for line in user_file:
    data = ast.literal_eval(line)
    # print(data['user_id'])
    id_list.append(data['user_id'])
print(len(id_list))
# u = api.get_user(id_list[0])
# print(u)
for id_val in id_list:
    for page in tweepy.Cursor(api.user_timeline, id=id_val, include_rts=True, tweet_mode='extended', lan='en', count=9999).pages():
        for tweet in page:
            json_str = tweet._json
            try:
                if json_str['possibly_sensitive']:
                    # print('found sensitive')
                    if json_str['in_reply_to_status_id'] is not None:
                        print('found reply')
                        user = api.get_user(json_str['in_reply_to_status_id'])
                        print("get User:", user)
                        if user.location is not None:
                            print('found location of user')
                            place = user.location
                        else:
                            print('found location of tweet')
                            place = tweet.place.fullname
                        data1 = {'user_id': user.id, 'place': place}
                        Update_id_list(id_list, data1)
                    elif (tweet.retweeted) or ('RT @' in tweet.full_text):
                        print('found retweeted')
                        og_tweet_id = tweet.retweeted_status.id
                        retweet_list = api.retweets(og_tweet_id)
                        print(retweet_list)
                        for ret_id in retweet_list:
                            if ret_id.location is not None:
                                print('found location of user')
                                place = ret_id.location
                            else:
                                print('No found location')
                                place = None
                            data1 = {'user_id': ret_id.user.id, 'place': ret_id.place.full_name}
                            Update_id_list(id_list, ret_id)
                    else:
                        print('No reply and no retweet')
                else:
                    print('Not sensitive')
            except:
                print(json_str)