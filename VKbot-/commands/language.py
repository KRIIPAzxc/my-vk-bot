# -*- coding: utf-8 -*-
import json
import vk_api
from vk_api.utils import get_random_id

def main(event,vk):
    try:
        with open('./data.json', 'r', encoding='utf-8') as json_file:
            datatemp = json.load(json_file)
        language = datatemp[str(event.user_id)]["lang"]
    except:
        language = "en"

    try:
        with open('./commands/command.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            data = data["output"]
            
        eventText = str(event.text).split()
        try:
            with open(("./data.json"),"r", encoding='utf-8') as f:
                file = json.load(f)
        except:
            file = {}
        print(file)
        print(event.user_id)

        if str(eventText[1]) == "ru" or eventText[1] == "en":
            file[str(event.user_id)]["lang"] = eventText[1]
            vk.messages.send(
            peer_id=event.peer_id,
            random_id=get_random_id(),
            message=data[language]["lanSelect"]
            )

        else:
            vk.messages.send(
            peer_id=event.peer_id,
            random_id=get_random_id(),
            message=data[language]["lanNotSup"]
            )
            return "done"
        
        file = json.dumps(file, ensure_ascii=False, indent=4)
        with open(("./data.json"),"w", encoding='utf-8') as f:
            f.write(file)
        return "done"
    
    except Exception as e:
        vk.messages.send(
            peer_id=event.peer_id,
            random_id=get_random_id(),
            message=data[language]["entLang"]
            )
        return "script error :" + str(e)