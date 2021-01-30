from learning.models import SongSentiment, Regression, ReverseRegression
from djqscsv import render_to_csv_response, write_csv
import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle


def train_model():
    """ 
    Performs linear regression on the SongSentiment samples in the database
  
    Pickles the linear regression model in the database for later use
  
    Parameters: 

    Returns: 
    """
    #do the training here
    INPUT_FIELDS = ['sadness_score',
        'joy_score',
        'fear_score',
        'disgust_score',
        'anger_score']

    OUTPUT_FIELDS = ['acousticness',
        'danceability',
        'energy',
        'liveness',
        'loudness',
        'valence',
        'tempo']
    samples = list(SongSentiment.objects.all())
    x = SongSentiment.objects.values(*INPUT_FIELDS)
    y = SongSentiment.objects.values(*OUTPUT_FIELDS)

    x_dataframe = pd.DataFrame(x)
    y_dataframe = pd.DataFrame(y)

    model = LinearRegression()
    model.fit(x_dataframe, y_dataframe)
    model_pickle = pickle.dumps(model)
    new_model = Regression(pickle=model_pickle)
    new_model.save()

    reverse_model = LinearRegression()
    reverse_model.fit(y_dataframe, x_dataframe)
    model_pickle = pickle.dumps(reverse_model)
    new_model = ReverseRegression(pickle=model_pickle)
    new_model.save()

def load_model():
    """
    Load the latest linear regression from the database

    Returns: 
    LinearRegression: Latest linear regression
    """
    latest_pickle_entry = Regression.objects.order_by('-id').first()
    latest_pickle = latest_pickle_entry.__dict__['pickle']
    return pickle.loads(latest_pickle)

def load_reverse():
    """
    Load the latest reverse model from the database

    Returns
    LinearRegression: Latest reverse linear regression
    """
    latest_pickle_entry = ReverseRegression.objects.order_by('-id').first()
    latest_pickle = latest_pickle_entry.__dict__['pickle']
    return pickle.loads(latest_pickle)

def make_prediction(movie_sentiment):
    """
    Make a prediction from the latest LinearRegression

    Paramaters:
    movie_sentiment (2D Array): a movie sentiment array

    Returns:
    2D Array: a song sentiment array
    """
    model = load_model()
    return model.predict(movie_sentiment)


def make_reverse(song_sentiment):
    """
    Make a prediction from the latest LinearRegression of the song sentiment

    Paramaters:
    song_sentiment (2D Array): a song sentiment array

    Returns:
    2D Array: a movie sentiment array
    """
    model = load_reverse()
    return model.predict(song_sentiment)
