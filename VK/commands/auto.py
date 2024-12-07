# -*- coding: utf-8 -*-
import json
import time
import vk_api
import langs
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

        try:
            if eventText[1] != "off":
                lang = langs.languages()
                if eventText[1] in lang:
                    file[str(event.user_id)]["autoLang"] = eventText[1]

                    file[str(event.user_id)]["auto"] = True

                    vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=data[language]["ATE"] + " - " + eventText[1]
                    )
                else:
                    eventText[1]

                    vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=data[language]["lanNotSup"]
                    )
                            
            elif eventText[1] == "off":
                file[str(event.user_id)]["auto"] = False
        
                vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message=data[language]["ATD"]
                )
            else:
                vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message=data[language]["unkErr"]
                )
                return "unknown error"
                
        except:
            vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message=data[language]["entLang"]
            )


        datas = json.dumps(file, ensure_ascii=False, indent=4)
        with open(("./data.json"),"w", encoding='utf-8') as f:
            f.write(datas)
        return "done"
        
    except Exception as e:
        return "script error :" + str(e)