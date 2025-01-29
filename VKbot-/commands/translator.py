import json
import time
import requests
import vk_api
from vk_api.utils import get_random_id

import langs

def main(event,vk):
    try:
        with open('./data.json', 'r', encoding='utf-8') as json_file:
            datatemp = json.load(json_file)
        language = datatemp[str(event.user_id)]["lang"]
    except:
        language = "en"

    try:
        eventText = str(event.text).split()
        inputText = ""
        lang = langs.languages()
        
        with open('./commands/command.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            data = data["output"]
            
        if eventText[1].lower() in lang:
            print()
            inputText = ' '.join(eventText[2:])
            outputText = translate(inputText,eventText[1])
        
            vk.messages.send(
            peer_id=event.peer_id,
            random_id=get_random_id(),
            message=outputText.lower()
            )
        else:
            vk.messages.send(
            peer_id=event.peer_id,
            random_id=get_random_id(),
            message=data[language]["lanNotSup"]
            )

        return "done"
    except Exception as e:
        return "script error :" + str(e)
    
def auto(event,vk,):
    try:
        with open('./data.json', 'r', encoding='utf-8') as json_file:
            datatemp = json.load(json_file)
        language = datatemp[str(event.user_id)]["lang"]
        lang = datatemp[str(event.user_id)]["autoLang"]
    except:
        language = "en"

    try:
        inputText = ""
        with open('./commands/command.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            data = data["output"]

        inputText = str(event.text)
        print()
        outputText = translate(inputText,lang)
        
        vk.messages.send(
        peer_id=event.peer_id,
        random_id=get_random_id(),
        message=outputText.lower()
        )

        return "done"
    except Exception as e:
        vk.messages.send(
        peer_id=event.peer_id,
        random_id=get_random_id(),
        message=data[""]
        )
        return "script error :" + str(e)
    
def translate(text, target_language):
    
    url = "https://translate.googleapis.com/translate_a/single"

    params = {
        "client": "gtx",
        "sl": "auto",
        "tl": target_language,
        "dt": "t",
        "q": text
    }

    response = requests.get(url, params=params)
    try:
        if response.status_code == 200:
            result = response.json()
            translated_text = result[0][0][0]
            return translated_text
        else:
            print("wait")
            time.sleep(5)
            translate(text, target_language)
    except:
        print("wait")
        time.sleep(5)
        translate(text, target_language)
