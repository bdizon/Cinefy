

import json
from initial_data.titles import titles
from shared.sentiment import get_sentiment_by_scene


def average_sentiment(movie_sentiment_array):
    keys = movie_sentiment_array[0].keys()
    avg_senti = {}
    for senti in movie_sentiment_array:
        for key in keys:
            if key in avg_senti:
                avg_senti[key] += senti[key]
            else:
                avg_senti[key] = senti[key]

    for key in keys:
        avg_senti[key] /= len(movie_sentiment_array)
    return avg_senti

sentiments = []
passed = 0
total = 0
with open("initial_data/movie_list.txt", 'r') as movie_file:
    titles = movie_file.readlines()
    for ctr , title in enumerate(titles):
        try:
            m_title = title.strip()
            print(m_title)
            scene_sentiments = get_sentiment_by_scene(m_title)
            if scene_sentiments.__sizeof__() > 20:
                passed += 1
                avg_senti = average_sentiment(scene_sentiments)
                avg_senti['title'] = m_title
                print(avg_senti)
                sentiments.append(avg_senti)
                
            total += 1
        except:
            print("skipped {}".format(title))
            pass
with open("initial_data/initialdata.json", 'w') as fopen:
    fopen.write(json.dumps(sentiments, indent=4))
print(passed / total)