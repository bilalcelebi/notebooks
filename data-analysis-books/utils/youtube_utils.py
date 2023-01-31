from pyyoutube import Api

key_path = '/home/bilalcelebi/Workspace/notebooks/data/youtube-data/api_key.txt'
api_key = open(key_path).read()

api = Api(api_key = api_key)


def get_comment(com_id):

    comments = api.get_comment_by_id(comment_id = com_id)
    comments = comments.items
    
    response = []

    for comment in comments:

        snippet = comment.snippet

        data = dict()
        data['author'] = str(snippet.authorDisplayName)
        data['like_count'] = int(snippet.likeCount)
        data['text'] = str(snippet.textOriginal)

        response.append(data)

    return response

def get_comment_threads(vid_id, count):

    threads = api.get_comment_threads(video_id = vid_id, count = count)
    ids = [str(thread.id) for thread in threads.items]
    
    return ids


def get_comments(video_id, count):

    threads = get_comment_threads(vid_id = video_id, count = count)
    
    response = []

    for thread in threads:

        comments = get_comment(com_id = thread)

        for comment in comments:

            if comment not in response:

                response.append(comment)


    return response


def extract_tags(tags):

    point = len('https://en.wikipedia.org/wiki/')
    response = []

    for tag in tags:

        response.append(tag[point:])

    return response


def get_channel_info(channel_id):

    channel = api.get_channel_info(channel_id = channel_id)
    channel = channel.items[0].to_dict()
    stats = channel['statistics']

    response = dict()
    response['title'] = channel['snippet']['title']
    response['description'] = channel['snippet']['description']
    response['created_time'] = channel['snippet']['publishedAt']
    response['language'] = channel['snippet']['defaultLanguage']
    response['country'] = channel['snippet']['country']
    response['view_count'] = int(stats['viewCount'])
    response['subs_count'] = int(stats['subscriberCount'])
    response['video_count'] = int(stats['videoCount'])
    response['tags'] = extract_tags(channel['topicDetails']['topicCategories'])
    response['madeforkids'] = channel['status']['madeForKids']
    
    try:
        response['good_standing'] = channel['auditDetails']['overallGoodStanding']
    except:
        response['good_standing'] = 'None'

    try:
        response['owner'] = channel['contentOwnerDetails']['contentOwner']
    except:
        response['owner'] = 'None'



    return response


def extract_video_details(video):

    response = dict()
    response['title'] = video['snippet']['title']
    response['description'] = video['snippet']['description']
    response['created_time'] = video['snippet']['publishedAt']
    response['tags'] = video['snippet']['tags']
    response['language'] = video['snippet']['defaultAudioLanguage']
    response['duration'] = video['contentDetails']['duration']
    response['caption'] = video['contentDetails']['caption']
    response['forKids'] = video['status']['madeForKids']
    response['view_count'] = int(video['statistics']['viewCount'])
    response['like_count'] = video['statistics']['likeCount']
    response['comment_count'] = int(video['statistics']['commentCount'])
    response['topics'] = extract_tags(video['topicDetails']['topicCategories'])

    return response


def get_video_details(video_id):

    video = api.get_video_by_id(video_id = video_id)
    video = video.items[0].to_dict()
    
    response = extract_video_details(video = video)

    return response


def get_popular_videos(country_code):

    videos = api.get_videos_by_chart(chart = 'mostPopular', region_code = country_code, count = 5)
    
    response = []

    for video in videos.items:
        
        details = get_video_details(video_id = str(video.id))
        
        response.append(details)
        

    return response

    
def extract_result(result, result_type):

    result = result.to_dict()

    response = dict()

    if result_type == 'video':
        response['id'] = result['id']['videoId']
    elif result_type == 'channel':
        response['id'] = result['id']['channelId']
    elif result_type == 'playlist':
        response['id'] = result['id']['playlistId']
    else:
        response['id'] = 'None'

    response['title'] = result['snippet']['title']
    response['description'] = result['snippet']['description']
    response['created_at'] = result['snippet']['publishedAt']
    response['channel'] = result['snippet']['channelTitle']
    response['channel_id'] = result['snippet']['channelId']

    return response


def search_with_keyword(keyword, search_type, count = 3, limit = 3, order = 'viewCount'):

    results = api.search_by_keywords(q = keyword, search_type = search_type, count = count, limit = limit, order = order)
    results = results.items

    response = [extract_result(result, search_type) for result in results]

    return response


def search_with_time_range(keyword, search_type, before, after, count = 3, order = 'viewCount'):

    before = before + 'Z'
    after = after + 'Z'

    results = api.search(q = keyword, published_before = before, published_after = after, count = count, search_type = search_type, order = order)
    results = results.items

    response = [extract_result(result, search_type) for result in results]

    return response


def search_with_related_video(video_id, search_type, count = 3, order = 'viewCount'):

    results = api.search(related_to_video_id = video_id, count = count, order = order, search_type = search_type)
    results = results.items

    response = [extract_result(result, search_type) for result in results]

    return response


def search_with_topic(topic_id, search_type, count = 3, order = 'viewCount'):

    results = api.search(topic_id = topic_id, search_type = search_type, count = count, order = order)
    results = results.items

    response = [extract_result(result, search_type) for result in results]

    return response


def get_video_categories(region_code):

    results = api.get_video_categories(region_code = region_code)
    results = results.items

    response = []

    for result in results:
        result = result.to_dict()

        category = dict()
        category['id'] = result['id']
        category['title'] = result['snippet']['title']
        category['channel'] = result['snippet']['channelId']

        response.append(category)

    return response


def get_category_details(category_id):

    results = api.get_video_categories(category_id = category_id)
    results = results.items
    
    response = []

    for result in results:
        result = result.to_dict()
        
        category = dict()
        category['id'] = result['id']
        category['title'] = result['snippet']['title']

        response.append(category)


    return response


def get_channel_sections(channel_id):

    results = api.get_channel_sections_by_channel(channel_id = channel_id)
    results = results.items

    response = []

    for result in results:
        result = result.to_dict()

        section = dict()
        section['id'] = result['id']
        section['title'] = result['snippet']['title']
        section['type'] = result['snippet']['type']

        response.append(section)

    return response


def extract_playlist(playlist):
    
    playlist = playlist.to_dict()

    response = dict()
    response['id'] = playlist['id']
    response['title'] = playlist['snippet']['title']
    response['description'] = playlist['snippet']['description']
    response['created_time'] = playlist['snippet']['publishedAt']
    response['channel'] = playlist['snippet']['channelTitle']
    response['channel_id'] = playlist['snippet']['channelId']
    response['item_count'] = playlist['contentDetails']['itemCount']
    response['status'] = playlist['status']['privacyStatus']
    response['language'] = playlist['snippet']['defaultLanguage']


    return response



def get_playlist(playlist_id):

    results = api.get_playlist_by_id(playlist_id = playlist_id)
    results = results.items

    response = [extract_playlist(playlist) for playlist in results]

    return response


def get_channel_playlists(channel_id):

    results = api.get_playlists(channel_id = channel_id)
    results = results.items

    response = [extract_playlist(playlist) for playlist in results]

    return response




def get_playlist_items(playlist_id, count = 3):

    results = api.get_playlist_items(playlist_id = playlist_id, count = count)
    results = results.items

    response = []

    for result in results:
        result = result.to_dict()

        item = dict()

        item['id'] = result['snippet']['resourceId']['videoId']
        item['title'] = result['snippet']['title']
        item['description'] = result['snippet']['description']
        item['created_time'] = result['snippet']['publishedAt']
        item['channel'] = result['snippet']['channelTitle']
        item['channel_id'] = result['snippet']['channelId']
        item['video_owner'] = result['snippet']['videoOwnerChannelId']
        item['video_owner_name'] = result['snippet']['videoOwnerChannelTitle']
        item['position'] = result['snippet']['position']

        response.append(item)

    return response



def get_activities(channel_id, count = 3):

    results = api.get_activities_by_channel(channel_id = channel_id, count = count)
    results = results.items
        
    response = []

    for result in results:
        result = result.to_dict()

        activity = dict()
        activity['id'] = result['id']
        activity['title'] = result['snippet']['title']
        activity['description'] = result['snippet']['description']
        activity['created_time'] = result['snippet']['publishedAt']
        activity['details'] = result['contentDetails']

        response.append(activity)

    return response
