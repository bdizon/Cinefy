'''GET CURRENT SAVED TRACKS
returns list of track names'''
def get_username(sp):
    username = sp.current_user()['id']
    return username

def user_current_saved_tracks():
    tracks_list = []
    results = sp.current_user_saved_tracks(limit=2)
    for item in results['items']:
        track = item['track']
        tracks_list.append(track['name'])
    return tracks_list

'''GET FOLLOWED ARTISTS
returns list of followed artists names'''
def user_followed_artists():
    artist_list = []
    followed_artists = sp.current_user_followed_artists(limit=2)
    artist = followed_artists['artists']
    items = artist['items']
    for i in range(len(items)):
        artist_list.append(items[i]['name'])
    return artist_list

'''GET TOP ARTISTS
returns list of top artists names'''
def user_top_artists():
    artist_list = []
    top_artists = sp.current_user_top_artists(limit=2, time_range='long_term')
    items = top_artists['items']
    for i in range(len(items)):
        artist_list.append(items[i]['name'])
    return artist_list

'''GET TOP ARTISTS URI
returns list of top artists uri'''
def user_top_artists_uri(sp, timerange_no):
    artist_list = []
    timerange = 'short_term'
    if timerange_no == 1:
        timerange = 'short_term'
    elif timerange_no == 2:
        timerange = 'medium_term'
    elif timerange_no == 3:
        timerange = 'long_term'
    top_artists = sp.current_user_top_artists(limit=1, time_range=timerange)
    # print(top_artists)
    items = top_artists['items']
    for i in range(len(items)):
        artist_list.append(items[i]['uri'])
    return artist_list

'''GET TOP TRACKS URI
returns list of top tracks uri'''
def user_top_tracks(sp, timerange_no):
    tracks_list = []
    timerange = 'short_term'
    if timerange_no == 1:
        timerange = 'short_term'
    elif timerange_no == 2:
        timerange = 'medium_term'
    elif timerange_no == 3:
        timerange = 'long_term'
    top_tracks = sp.current_user_top_tracks(limit=50, time_range=timerange)
    # print(top_tracks)
    items = top_tracks['items']
    for i in range(len(items)):
        tracks_list.append(items[i]['uri'])
    return tracks_list

def track_info(sp,tracks_list):
    info_list = sp.tracks(tracks_list)
    return info_list

def track_features(sp, tracks_list):
    features = sp.audio_features(tracks_list)
    return features

def get_features(features):
    acousticness=danceability=energy=liveness=loudness=valence=tempo= 0
    seed_values = [0] * 7
    for i in range(len(features)):
        # print(features[i]['danceability'])
        acousticness += features[i]['acousticness']
        danceability += features[i]['danceability']
        energy += features[i]['energy']
        liveness += features[i]['liveness']
        loudness += features[i]['loudness']
        valence += features[i]['valence']
        tempo += features[i]['tempo']
    seed_values[0] = acousticness
    seed_values[1] = danceability
    seed_values[2] = energy
    seed_values[3] = liveness
    seed_values[4] = loudness
    seed_values[5] = valence
    seed_values[6] = tempo              
    seed_values[:] = [x/len(features) for x in seed_values]
    # print(seed_values)   
    # print(len(features)) 
    return seed_values

def track_analysis(sp, tracks_list):
    analysis = sp.audio_analysis(tracks_list)
    return analysis

'''GET TOP GENRES
returns lists of top genres names
gets top genres from top artists; chooses the '''
def user_top_genres(sp, timerange_no):
    genre_list = []
    timerange = 'short_term'
    if timerange_no == 1:
        timerange = 'short_term'
    elif timerange_no == 2:
        timerange = 'medium_term'
    elif timerange_no == 3:
        timerange = 'long_term'
    top_artists = sp.current_user_top_artists(limit=5, time_range=timerange)
    # print(top_artists)
    items = top_artists['items']
    for i in range(len(items)):
        genre_list.append(items[i]['genres'][0])
    return genre_list

'''GET SPOTIFY GENRES
returns list of all the spotify genres'''
# def get_genre():
#     seed_list = []
#     genre_list = []
#     seed_list = sp.recommendation_genre_seeds()
#     genre_list = seed_list['genres']
#     return genre_list

'''GET RECOMMENDATIONS
based on seeds: artists, genres, tracks, attribute values
1 parameter: sentiment of text/scene
returns list of recommended tracks uri's
'''
def get_recs(sp, sentiment, index, attribute_values, artist_list, genre_list, timerange_no):        
    recs_list = []
    tracks_list = []
    genre_list = ['rock', 'classical', 'metal', 'indie']
    # genre_list = []
    # print(attribute_values[0])
    # artist_list = artist_list[0]
    # artist_list = artist_list[0]
    if timerange_no == 4:
        genre_list = ['rock', 'classical', 'metal', 'pop', 'indie']
        artist_list = []
    recs = sp.recommendations(seed_genres=genre_list, seed_artists=artist_list, seed_tracks=tracks_list, limit=20, acousticness=attribute_values[index][0], danceability=attribute_values[index][1], energy=attribute_values[index][2], liveness=attribute_values[index][3], loudness=attribute_values[index][4], valence=attribute_values[index][5], tempo=attribute_values[index][6])
    # print("&&&&")
    # print(recs)
    tracks = recs['tracks']
    # print("99999999")
    # print(tracks)
    for i in range(len(tracks)):
        uris = tracks[i]['uri']
        recs_list.append(uris)
    # print("####")
    # print(recs_list)
    return recs_list
    
'''CREATE PLAYLIST FOR USER
returns playlist id''' 
def create_playlist(sp, movie_title):
    playlist_name = 'Cinefy Soundtrack for ' + str(movie_title)
    # creating playlist, info is in playlist var
    username = get_username(sp)
    print(username)
    playlist = sp.user_playlist_create(user=username, name=playlist_name, public=True, collaborative=False)
    return(playlist['id'])

'''ADD TRACKS TO PLAYLIST CREATED
three parameters: 1st param is a string variable containing the playlist_id, 2nd param is the list of track uri's to add, 3rd param is the sentiment'''
def add_tracks_playlist(sp, createdplaylist_id, sentiment, index, attribute_values, artist_list, genre_list, timerange_no):
    recs_list = get_recs(sp, sentiment, index, attribute_values, artist_list,genre_list, timerange_no)
    # print("RECS")
    # print(recs_list)
    sp.playlist_add_items(playlist_id=createdplaylist_id, items=recs_list ,position=None)
    
'''DISPLAY PLAYLIST DETAILS
display the title, artist, and album
one parameter: param is a string var containing the playlist details'''
def playlist_details(createdplaylist_id):
    details = sp.playlist_items(playlist_id=createdplaylist_id)

'''DELETE PLAYLIST(S) 
two parameters: 1st param is the spotify auth token, 2nd param is the list of spotify uri's for the playlist to be deleted'''
def delete_playlist(sp, playlists):
    for playlist in playlists:
        # print("hello")
        # print(playlist)
        # remove 'spotify:playlist:' substring from 'spotify:playlist:id', only need playlist_id
        playlist = playlist.replace('spotify:playlist:', '')
        # print(playlist)
        sp.current_user_unfollow_playlist(playlist)
    # sp.current_user_unfollow_playlist(playlist_id='4p5g3TOTPS87vtsbb4iRyc')
    return

'''GET CURRENT PLAYLIST
three parameters: spotify auth token, number of playlists, offset index'''
def get_current_playlists(sp, limit_no, offset_index):
    playlist_uris = []
    playlist_info = sp.current_user_playlists(limit=limit_no, offset=offset_index)
    # print(playlist_info['items'])
    items = (playlist_info['items'])
    for i in range(len(items)):
        # print(items[i]['uri'])
        playlist_uris.append(items[i]['uri'])
    return playlist_uris


