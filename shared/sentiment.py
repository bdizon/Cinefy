import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from .config import apikey, url
from .script_scraper import webscrape
authenticator = IAMAuthenticator(apikey)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2020-08-01',
    authenticator=authenticator)

natural_language_understanding.set_service_url(url)
MODULUS = 50
def analyze_text(text):
    return natural_language_understanding.analyze(
        text=text,
        features=Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
            keywords=KeywordsOptions(emotion=True, sentiment=True, limit=2))).get_result()

def most_important_sentiment(sentiment_scene):
    max_significance = 0
    max_significance_sentiment = {}
    for keyword in sentiment_scene['keywords']:
        if max_significance < float(keyword['relevance']):
            max_significance = float(keyword['relevance'])
            max_significance_sentiment = keyword['emotion']
    return max_significance_sentiment

def get_sentiment_by_scene(movie_title):
    scene_texts = webscrape(movie_title)
    sentiments = []

    for i, scene_text in enumerate(scene_texts):
        if len(scene_text) > 40 and i % MODULUS == 0:
            full_sentiment_analysis = analyze_text(scene_text)
            scene_sentiment = most_important_sentiment(full_sentiment_analysis)
            sentiments.append(scene_sentiment)
    return sentiments