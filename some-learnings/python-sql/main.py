import sqlite3
from sqlite3 import Error
import os
import pandas as pd

def create_connection(database_file):

    connection = None

    try:

        connection = sqlite3.connect(database_file)
        
        return connection

    except Error as e:

        print(e)

    
    return connection


def create_table(connection, table_sql):

    try:

        c = connection.cursor()
        c.execute(table_sql)

    except Error as e:

        print(e)


def get_videos_data():

    videos_path = '/home/bilalcelebi/Workspace/notebooks/data/youtube-data/videos.csv'
    df = pd.read_csv(videos_path)
    df.dropna(inplace = True)

    response = []

    for idx in range(df.shape[0]):

        row = df.iloc[idx]
        
        video_id = str(row['id'])
        title = str(row['title'])
        views = int(row['view_count'])
        likes = int(row['like_count'])
        comments = int(row['comment_count'])
        channel = str(row['channel_id'])

        pair = (video_id,title,views,likes,comments,channel)
        response.append(pair)
    
    return response


def get_channels_data():

    channels_path = '/home/bilalcelebi/Workspace/notebooks/data/youtube-data/channels.csv'
    df = pd.read_csv(channels_path)
   
    response = []

    for idx in range(df.shape[0]):

        row = df.iloc[idx]
        
        channel_id = str(row['id'])
        title = str(row['title'])
        country = str(row['country'])
        videos = int(row['video_count'])

        pair = (channel_id,title,country,videos)

        response.append(pair)

    return response


def create_video(connection, video):

    sql = """INSERT INTO videos(video_id,title,views,likes,comments,channel_id)
    VALUES(?,?,?,?,?,?)"""

    cursor = connection.cursor()
    cursor.execute(sql, video)
    connection.commit()

    return cursor.lastrowid


def create_channel(connection, channel):

    sql = """INSERT INTO channels(channel_id,title,country,videos) VALUES(?,?,?,?)"""
    cursor = connection.cursor()
    cursor.execute(sql, channel)
    connection.commit()

    return cursor.lastrowid


def make_request(connection, sql, one = False):

    cursor = connection.cursor()
    res = cursor.execute(sql)

    if one == True:

        return res.fetchone()

    else:

        return res.fetchall()


def main():

    db_path = os.path.join(os.getcwd(), 'learning.db')
    conn = create_connection(db_path)
    
    """
    channels_table = "CREATE TABLE IF NOT EXISTS channels (
    id integer AUTO_INCREMENT,
    channel_id text NOT NULL,
    title text,
    country text,
    videos integer,
    PRIMARY KEY (id))"

    videos_table = "CREATE TABLE IF NOT EXISTS videos (
    id integer AUTO_INCREMENT,
    video_id text NOT NULL,
    title text,
    views integer,
    likes integer,
    comments integer,
    channel_id text,
    PRIMARY KEY (id),
    FOREIGN KEY (channel_id) REFERENCES channels (channel_id)
    )"
    

    if conn is not None:

        create_table(conn, channels_table)
        create_table(conn, videos_table)

    else:

        print('Error!!!')

    """
    
    """
    videos = get_videos_data()
    channels = get_channels_data()

    for video in videos:

        create_video(conn, video)

    for channel in channels:

        create_channel(conn, channel)
    """
    

    #sql = 'SELECT title,views,likes FROM videos ORDER BY likes DESC'
    #sql = 'SELECT title,country,videos FROM channels ORDER BY videos'
    #sql = "SELECT title,country,videos FROM channels WHERE title LIKE 'a%' ORDER BY videos DESC" 
    #sql = 'SELECT COUNT(videos.video_id), COUNT(channels.channel_id) from videos INNER JOIN channels ON videos.channel_id=channels.channel_id'
    #sql = 'SELECT AVG(views), AVG(likes), AVG(comments) FROM videos'
    #sql = 'SELECT SUM(views), SUM(likes), SUM(comments) FROM videos'
    #sql = 'SELECT MIN(views), MAX(views) FROM videos'
    #sql = 'SELECT MIN(likes), MAX(likes) FROM videos'
    sql = 'SELECT MIN(comments), MAX(comments) FROM videos'

    print(make_request(conn, sql, one = True))

if __name__ == '__main__':

    main()
