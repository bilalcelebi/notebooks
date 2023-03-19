from pymongo import MongoClient
import pandas as pd
import pymongo

client = MongoClient('localhost', 27017)
database = client.my_database

data_path = '/home/bilalcelebi/Workspace/notebooks/data/youtube-data/videos.csv'
data = pd.read_csv(data_path)
data.dropna(inplace = True)

records = []

for idx,pair in data.iterrows():

    node = dict()
    node['video_id'] = str(pair['id'])
    node['title'] = str(pair['title'])
    node['views'] = int(pair['view_count'])
    node['likes'] = int(pair['like_count'])
    node['comments'] = int(pair['comment_count'])
    node['channel_id'] = str(pair['channel_id'])
    node['channel_title'] = str(pair['channel_title'])

    records.append(node)


collection = database.mytable
#rec = database.mytable.insert_many(records)

#videos = collection.find()
#videos = collection.find().sort('likes', pymongo.DESCENDING)
videos = collection.find().sort('views', pymongo.DESCENDING)

for video in videos[:5]:

    print(video)
