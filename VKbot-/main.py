# -*- coding: utf-8 -*-
from gettext import install

Notready = True

while Notready:
    try:
        import pkg_resources
        import subprocess
        import sys
        import importlib
        import requests
        import vk_api
        from vk_api.longpoll import VkLongPoll, VkEventType
        from vk_api.utils import get_random_id
        import datetime
        import json
        import commands.translator as translator
        import pytesseract
        import cv2
        import matplotlib.pyplot as plt
        from PIL import Image
        from vk_api.exceptions import VkApiError
        Notready = False
    except ModuleNotFoundError as e:
        print(e.name)
        if e.name == "cv2":
            e.name = "opencv-python"
        try:  
            subprocess.check_call([sys.executable, "-m", "pip", "install", e.name])  
        except subprocess.CalledProcessError as er:  
            print(f"Ошибка установки пакета {e.name}: {er}") 
        


with open('./commands/command.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
#data_json = json.dumps(datatemp)
#data = json.loads(data_json)



vk_session = vk_api.VkApi(token='vk1.a.RHNQsEEP0NWNQJtyHVVBoclBzqRW9Sr_Pquuo5-1aVhXwMgceSCQTE7zplpT76Rn83IoADxz0iH1TDIAcTtXBGKSoyKSDc_Fj9KyjpzyuUbx3xe9_AMPVhZlugBSJ1MW8NuYxy18vI5oQartR_rjV-4T8MP3ssA5Ba344VM49EN31kGNg2Nbm-q5JSJSRUnTXMBZMQl6smFxqIBKYL6F5w')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

def main(): 
        print("started")
        for event in longpoll.listen():
            try:
                date = str(datetime.datetime.now().year) + "." + str(datetime.datetime.now().month) + "." + str(datetime.datetime.now().day)
                time = str(datetime.datetime.now().hour) + "." + str(datetime.datetime.now().minute) + "." + str(datetime.datetime.now().second) + "." + str(datetime.datetime.now().microsecond)
                if event.type == VkEventType.MESSAGE_NEW:
                    print(event.peer_id)

                    print('Новое сообщение:')

                    if event.from_me:
                        print('От меня для: ', end='')
                    elif event.to_me:
                        print('Для меня от: ', end='')
                        try:
                            with open(("./data.json"),"r", encoding='utf-8') as f:
                                file = json.load(f)
                                auto = file[str(event.user_id)]["auto"]
                        except Exception as e:
                            with open(("./data.json"),"r+", encoding='utf-8') as f:
                                if str(event.user_id) not in file:
                                    file = file | { str(event.user_id) : {"auto": False, "lang": "ru", "autoLang": "off"}}
                                    data = json.dumps(file, ensure_ascii=False, indent=2)
                                    f.write(data)
                                    
                            with open(("./logs/logs" + " " + date +".log"),"a", encoding='utf-8') as f:
                                f.write("\n" + "<" + time + ">" + " --> " + "data file error:" + str(e))
                    
                    print('Текст: ', event.text, "\nвложение: ", event.attachments)
                    print()
                    if event.to_me and event.attachments:
                        if event.attachments["attach1_type"] == "doc":
                            docs = vk.messages.getById(message_ids=event.message_id)['items'][0]['attachments'][0]
                            docs = json.dumps(docs, indent=2)
                            docs = json.loads(docs)
                            print(docs["type"])
                            url = docs[docs["type"]]["url"]
                            with open('pic1.'+docs[docs["type"]]["ext"], 'wb') as handle:
                                response = requests.get(url, stream=True)

                                if not response.ok:
                                    print(response)

                                for block in response.iter_content(1024):
                                    if not block:
                                        break

                                    handle.write(block)
                                    
                        elif event.attachments["attach1_type"] == "photo":
                            docs = vk.messages.getById(message_ids=event.message_id)['items'][0]['attachments'][0]
                            docs = json.dumps(docs, indent=2)
                            docs = json.loads(docs)
                            print(docs["type"])
                            url = docs[docs["type"]]["orig_photo"]["url"]
                            with open('pic1.jpg', 'wb') as handle:
                                response = requests.get(url, stream=True)

                                if not response.ok:
                                    print(response)

                                for block in response.iter_content(1024):
                                    if not block:
                                        break

                                    handle.write(block)
                                
                    elif event.to_me and event.text[0] == "/":
                        with open(("./logs/logs" + " " + date +".log"),"a", encoding='utf-8') as f:
                            f.write("\n" + "<" + time + ">" + " --> " + event.text + " " + processing(event))
                    elif event.to_me and event.text[0] != "/" and auto == True:
                        try:
                            with open(("./logs/logs" + " " + date +".log"),"a", encoding='utf-8') as f:
                                f.write("\n" + "<" + time + ">" + " --> " + event.text + " 'script: translator.py' --> " + translator.auto(event,vk))
                        except Exception as e:
                            with open(("./logs/logs" + " " + date +".log"),"a", encoding='utf-8') as f:
                                f.write("\n" + "<" + time + ">" + " --> " + event.text + " script error: 'translator.py' --> " + str(e))
            except Exception as e:
                print(e)
                    
def processing(event):  
    try:
        with open('./data.json', 'r', encoding='utf-8') as json_file:
            datatemp = json.load(json_file)
        language = datatemp[str(event.user_id)]["lang"]
    except:
        language = "en"

    text = "unknown command"
    done = False 
    for item in data[language]:  
        mes = (event.text[1:]).split()
        if mes[0].casefold() in item['read']:
            if item["message"] != None:
                vk.messages.send(
                    peer_id=event.peer_id,
                    random_id=get_random_id(),
                    message=item['message']
                )
            text = "" if item['message'] == None else item['message'] + " "

            if item["command"] != None:
                try:
                    module = importlib.import_module("commands." + item["command"])
                    text += "--> script: '" + item["command"] + ".py' --> " + module.main(event,vk)
                except Exception as e:
                    text += "--> script error : '" + str(e)+ "' "
                    if "No module named" in str(e):
                        vk.messages.send(
                            peer_id=event.peer_id,
                            random_id=get_random_id(),
                            message=data["output"][language]["commNoExx"]
                        )
            if item["attachment"] != None:
                try:
                    result = json.loads(requests.post(vk.docs.getMessagesUploadServer(type='doc', peer_id=event.user_id)['upload_url'], files={'file': open(item["attachment"], 'rb')}).text)
                    print(result)
                    jsonAnswer = vk.docs.save(file=result['file'], title=item["title"], tags=[])
                    print(jsonAnswer)
                    vk.messages.send(
                        peer_id=event.peer_id,
                        random_id=get_random_id(),
                        message=jsonAnswer[str(jsonAnswer["type"])]['url']
                    )
                except Exception as e:
                    text += "--> script error : '" + str(e)+ "' "
                    if "No module named" in str(e):
                        vk.messages.send(
                            peer_id=event.peer_id,
                            random_id=get_random_id(),
                            message=data["output"][language]["commNoExx"]
                    )

            done = True
        
    if done == False:
        vk.messages.send(
            peer_id=event.peer_id,
            random_id=get_random_id(),
            message=data["output"][language]["unkComm"]
        )
    return text

if __name__ == '__main__':
    main()