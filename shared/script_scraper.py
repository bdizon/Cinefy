import requests
from bs4 import BeautifulSoup
import math

def webscrape(user_input):
    user_input = handle_casing(user_input)
    print(user_input)
    url = "https://www.imsdb.com/scripts/" + user_input + ".html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.find('pre')

    allScript = script.getText
    everyBody = script.findAll("b") #possible indictors of a scene, or character's cue

    allScript = str(allScript) #cleaning up the text 
    allScript = allScript.replace('<b>', "")
    allScript = allScript.replace("</b>", "")
    allScript = allScript.replace("BACK TO:", "")
    allScript = allScript.replace("CUT TO:", "")
    allScript = allScript.replace("(CONTINUED)", "")

    index = 2
    scenes = []

    for i in range(len(everyBody)): #cleans up indicators, TODO: can be elminated by using exact HTML formatting 
        everyBody[i] = str(everyBody[i])
        everyBody[i] = everyBody[i].replace("<b>", "")
        everyBody[i] = everyBody[i].replace("</b>", "")
        everyBody[i] = everyBody[i].replace("</pre>>", "")
        everyBody[i] =  everyBody[i].strip()
        if(everyBody[i].isupper() or everyBody[i].find("(") > -1):
             allScript = allScript.replace(everyBody[i], "") #gets rid of character names before their dialog 


    allScript = allScript.replace("\n", "")
    allScript = allScript.replace("   ", "") 
    
    i = 0 #index for everyBody
    start = 0  #find where the end of the scene starts
    end = 0  
    arbit_len = math.floor((len(allScript) / 100)) #for scripts without indicators, will have 100 scenes 
    
    
    while(i < len(everyBody)): #appends lines from the same scene and stored at an index, will populate scene array if there are indicators
        indexStr = str(index) + "."
        if(everyBody[i] == indexStr):
            end = allScript.find(indexStr) 
            scenes.append(allScript[start:end])
            start = end + 2
            index = index + 1
        
        i = i + 1

    if(len(scenes) > 1):
        #need to account for the last scene
        scenes.append(allScript[start:len(allScript)])
    else:
        start = 0 
        end = arbit_len
        for i in range(100): #those scripts without indicators
            scenes.append(allScript[start:end])
            start = end
            end = end + arbit_len if end + arbit_len < len(allScript) else len(allScript) - 1
    
    return scenes

def handle_casing(user_input):
    lower_case = set(["a", "an", "the", "above", "across", "after", "at", "around", "before", "behind", "below", "beside", "between", "by", "down", "during", "for", "from", 'in', 'inside', 'onto', 'of', 'off', 'on','out', 'through', 'to', 'under', 'up', 'with', 'nor', 'but', 'or', 'yet', 'so'])
    words = user_input.split(" ")
    for i in range(len(words)):
        if((words[i].lower()) in lower_case):
            if(i == 0):
                words[i] = words[i].lower()
                words[i] = words[i].capitalize()
            else:
                words[i] = words[i].casefold()
        else:
            words[i] = words[i].lower()
            words[i] = words[i].capitalize()
    user_input = "-".join(words)

    return user_input