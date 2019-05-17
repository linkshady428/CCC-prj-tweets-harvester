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
consumer_key = str(sys.argv[1])
consumer_secret = str(sys.argv[2])
access_token = str(sys.argv[3])
access_token_secret = str(sys.argv[4])
print(consumer_key, consumer_secret, access_token, access_token_secret )
# provide the key and secret.
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# get the info. with 'wait_on_rate_limit=True' to automatically wait for rate limits to replenish.
api = tweepy.API(auth)



# get the latest tweet in Au.

outfile = open('latest_tweets.json', 'a')
t_num=0
tweets_num = 0
f_num= 0
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):

        json_str = status._json
        # coordinates = [json_str['place']['bounding_box']['coordinates'][0][0],
        #                json_str['place']['bounding_box']['coordinates'][0][2]]
        # x1 = coordinates[0][0]
        # x2 = coordinates[1][0]
        # y1 = coordinates[0][1]
        # y2 = coordinates[1][1]
        # x = (x1 + x2) / 2
        # y = (y1 + y2) / 2
        #
        id_v = json_str['user']['id']
        # place = json_str['place']['full_name']
        # polygon = find_sa3(float(x), float(y))
        # data = {'time': json_str['created_at'], 'user_id': id_v, 'place': place, 'coordinate': [x, y], 'polygon': polygon}
        # print(data)
        # json.dump(data, outfile)
        # outfile.write('\n')
        # outfile.flush()
        print('latest')
        id = json_str['user']['id']
        try:
            print(json_str['possibly_sensitive'])

        except:
            pass

# coordinate_au=[112.921114, -43.740482, 159.109219, -9.142176]


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(languages =['en'], locations=[112.921114, -43.740482, 159.109219, -9.142176])
