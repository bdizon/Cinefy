from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import NewPlaylistForm
from django.contrib import messages
from django.urls import reverse
from shared.sentiment import analyze_text, get_sentiment_by_scene
from shared.script_scraper import webscrape
from spotipy import oauth2
import spotipy
from shared.oauth import sp_oauth
from shared.training import make_prediction
from shared.functions import *
from shared.sentiment import *


def new_playlist(request):
    if request.method == 'POST':
        form = NewPlaylistForm(request.POST)
        if form.is_valid():
            request.session['form'] = form.cleaned_data
            return HttpResponseRedirect(reverse('selections'))
    else:
        form = NewPlaylistForm()

    return render(request, "home/new_playlist.html", {"form":form})

def selections(request):
    # try:
    access_token = request.session["access_token"]
    sp = spotipy.Spotify(auth=access_token)
    # return JsonResponse({"user":sp.current_user(),"form":request.session["form"]})
    info = request.session['form']
    title = info['movie_name']
    time_range = info['listening_history']
    sentiments = []
    movie_sentiments = []
    # get sentiments for each scene
    title = str(title)
    sentiments = get_sentiment_by_scene(title)
    # get seed attribute values for movie sentiments
    # attribute_values = make_prediction(sentiments)
    
    # create playlist
    # playlist_uri = make_playlist(request, time_range, sentiments, attribute_values, sp)
            

    return HttpResponse(sentiments)
    # except:
    #     auth_url = sp_oauth.get_authorize_url()
    #     return HttpResponseRedirect(auth_url)


def home(request):
    return render(request, 'home/sign_in.html')

def logout(request):
    request.session["access_token"] = ""
    return HttpResponseRedirect(reverse("home"))

def auth(request):
    auth_url = sp_oauth.get_authorize_url()
    return HttpResponseRedirect(auth_url)

def auth_callback(request):
    token_info = sp_oauth.get_access_token(code = request.GET['code'], check_cache = False)
    access_token = token_info['access_token']
    request.session["access_token"] = access_token
    sp = spotipy.Spotify(auth=access_token)
    # import pdb; pdb.set_trace()
    return HttpResponseRedirect(reverse("new"))

def results(request, movie, genre):
    scenes_sentiments = get_sentiment_by_scene(movie)
    return HttpResponse(str(scenes_sentiments))

def seed_attributes(request, sentiments):
    attribute_values = make_prediction(sentiments)
    return HttpResponse(str(attribute_values))

def make_playlist(request, time_range, sentiments, attribute_values, sp):
    # get top artist from certain time range
    artist_list = user_top_artists_uri(sp, timerange)
    # create playlist
    createdplaylist_id = create_playlist(sp)
    # add tracks to playlist
    i = 0
    for sentiment in sentiments:
        add_tracks_playlist(sp, createdplaylist_id, sentiment, attribute_values[i], artist_list)
        i += 1
    return HttpResponse(str(createdplaylist_id))