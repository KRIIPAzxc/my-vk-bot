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

        text = ""
        eventText = str(event.text).split()
        print(eventText)
        with open('./commands/command.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        for item in data[language]:
            try:
                if eventText[1] in item['read']:
                    for i in item["read"]:
                        elem += "/" + i + ", "
                    text = "/" + elem[:-2] + " - " + item["alldescription"] + "\n"
                    vk.messages.send(
                        peer_id=event.peer_id,
                        random_id=get_random_id(),
                        message=text
                                    )
                    return "done"
                else:
                    0/0
            except:
                elem = ""
                for i in item["read"]:
                    elem += "/" + i + ", "
                text += elem[:-2] + " - " + item["description"] + "\n"

        vk.messages.send(
            peer_id=event.peer_id,
            random_id=get_random_id(),
            message=text
        )
        return "done"
    except Exception as e:
        return "script error :" + str(e)
