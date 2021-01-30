def sentiments_to_array(sentiments, sentiments_array):
    i = 0
    for sentiment in sentiments:
        value = sentiments[i].values() 
        sentiments_array.append(list(value))
        i = i + 1
    return sentiments_array