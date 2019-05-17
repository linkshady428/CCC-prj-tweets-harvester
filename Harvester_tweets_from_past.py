import tweepy
import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import sys
with open('SA3_2016_AUST_small.json') as f:
    data = json.load(f)

dictPoly = {}
for d in data['features']:
    if 'geometry' in d and d['geometry']!= None:
        listP = d['geometry']['coordinates'][0]
        dictPoly[d['properties']['SA3_CODE16']] = listP if len(listP)>1 else listP[0]


def getSA3(lon,lat, polygon): #149.57900670400008, -35.5
    polygon = Polygon(polygon) # create polygon
    point = Point(lon, lat) # create point
    return(point.within(polygon))

def find_sa3(lon,lat):
    try:
        for poly in dictPoly:
            if getSA3(lon, lat, dictPoly[poly]):
                return poly
    except Exception as e:
        print(lon, lat)

# key and secret.
consumer_key = 'fF3Ga382lSPnu8S35q3al9R8t'
consumer_secret = 'OocybjkiOs5l32YgJJ7UrE5dIA7IgPp29So5pIzztCpFLvLz08'
access_token = '1127799065117216768-9W8FOQD4VGP1tofGtvTjfi9GhtAP8e'
access_token_secret = 'felNrM5rfj0REI3ArkM8T5wMV5s9TEAIFL0DTpkPQ69nw'

# provide the key and secret.
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# get the info. with 'wait_on_rate_limit=True' to automatically wait for rate limits to replenish.
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
# -----------------------------------------------------------------------
# search all tweets 6-9 days ago, and only record the data from first tweet per user.
# The data includes timpestamp, user id, full_name of the place, southwest and northeast points of the bounding box.
# It will keep the id list for further use.

places = api.geo_search(query="Australia", granularity='country')
place_id = places[0].id
q="place:%s" % place_id

# 10k tweets 10mins.
id_list = []
tweets_num = 0


user_sta = api.get_user(id = '870593141245566977')

# print(user_sta._json)
#
num = 0
t_num = 0
f_num = 0
# for page in tweepy.Cursor(api.user_timeline, id= '870593141245566977', tweet_mode='extended', lan='en', count=9999).pages():
#     for tweet in page:
#         num += 1
#         json_str = tweet._json
#         # data = {'time': str(tweet.created_at), 'user_id':id_val, 'tweet_id': json_str['id'], 'text': str(tweet.full_text)}
#         # print(data)
#         try:
#             if json_str['possibly_sensitive']:
#                 t_num+=1
#             else:
#                 f_num +=1
#         except:
#             pass
# print('tweets num', num, t_num, f_num)
#             # json.dump(data, file)
#             # file.write('\n')
#             # file.flush()


outfile = open('user_AU.json', 'a')
idfile = open('sensitive.json', 'a')
print('start search users')
for page in tweepy.Cursor(api.search, q="place:%s" % place_id, count=9999, tweet_mode='extended').pages():

    for t in page:
        data1 = {}
        tweets_num += 1
        json_str = t._json
        id = json_str['user']['id']
        try:
            if json_str['possibly_sensitive']:
                data1 = {'time': str(t.created_at), 'user_id': id, 'tweet_id': json_str['id'],
                         'text': str(t.full_text), 'sensitive': str(json_str['possibly_sensitive'])}
                # print(data)
                json.dump(data1, idfile)
                idfile.write('\n')
                idfile.flush()
                t_num+=1
            else:
                # print(data)
                # json.dump(data1, idfile)
                # idfile.write('\n')
                # idfile.flush()
                f_num +=1
        except:
            pass
    print('tweets num', tweets_num, t_num, f_num)
#             coordinates = [json_str['place']['bounding_box']['coordinates'][0][0],
#                            json_str['place']['bounding_box']['coordinates'][0][2]]
#             x1 = coordinates[0][0]
#             x2 = coordinates[1][0]
#             y1 = coordinates[0][1]
#             y2 = coordinates[1][1]
#             x = (x1 + x2) / 2
#             y = (y1 + y2) / 2
#             polygon = find_sa3(float(x), float(y))
#             if id not in id_list and polygon is not None:
#                 place = json_str['place']['full_name']
#
#                 data = {'time': json_str['created_at'], 'user_id': id, 'place': place, 'coordinate': [x, y],
#                         'polygon': polygon}
#                 # print(data)
#                 id_list.append(id)
#                 # print(data)
#                 # idfile.write(str(id))
#                 # idfile.write('\n')
#                 # idfile.flush()
#                 json.dump(data, outfile)
#                 outfile.write('\n')
#                 outfile.flush()
#         print('Total processed tweets: ', tweets_num, 'Total unique id:', len(id_list))
#         if len(id_list) > 20000:
#             break
#     except tweepy.RateLimitError as e:
#         print(e)

# ----------------------------------------------------------------------------------
# search old tweets of users from above searching.
#
# file = open('all_tweets_of_users.json', 'a')
# total_tweet_num = 0
# print('start search tweets')
# for id_val in id_list:
#     tweet_num = 0
#     for page in tweepy.Cursor(api.user_timeline, id=id_val, tweet_mode='extended', lan='en', count=9999).pages():
#         for tweet in page:
#             tweet_num += 1
#             json_str = tweet._json
#             data = {'time': str(tweet.created_at), 'user_id':id_val, 'tweet_id': json_str['id'], 'text': str(tweet.full_text)}
#             # print(data)
#             json.dump(data, file)
#             file.write('\n')
#             file.flush()
#     total_tweet_num += tweet_num
#     print(id_val, ' Tweets num:', tweet_num)
# print('Total tweets:', total_tweet_num)
