# -*- coding: utf-8 -*-
import importlib
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import datetime
import json
import commands.translator as translator


with open('./commands/command.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
#data_json = json.dumps(datatemp)
#data = json.loads(data_json)

date = str(datetime.datetime.now().year) + "." + str(datetime.datetime.now().month) + "." + str(datetime.datetime.now().day)

vk_session = vk_api.VkApi(token='vk1.a.RHNQsEEP0NWNQJtyHVVBoclBzqRW9Sr_Pquuo5-1aVhXwMgceSCQTE7zplpT76Rn83IoADxz0iH1TDIAcTtXBGKSoyKSDc_Fj9KyjpzyuUbx3xe9_AMPVhZlugBSJ1MW8NuYxy18vI5oQartR_rjV-4T8MP3ssA5Ba344VM49EN31kGNg2Nbm-q5JSJSRUnTXMBZMQl6smFxqIBKYL6F5w')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

def main(): 


    for event in longpoll.listen():
        time = str(datetime.datetime.now().hour) + "." + str(datetime.datetime.now().minute) + "." + str(datetime.datetime.now().second) + "." + str(datetime.datetime.now().microsecond)
        if event.type == VkEventType.MESSAGE_NEW:
            
            
                
            print('Новое сообщение:')

            if event.from_me:
                print('От меня для: ', end='')
            elif event.to_me:
                print('Для меня от: ', end='')
                try:
                    with open(("./data.json"),"r", encoding='utf-8') as f:
                        file = json.load(f)
                        auto = file[str(event.user_id)]["auto"]
                    with open(("./data.json"),"r+", encoding='utf-8') as f:
                        if str(event.user_id) not in file:
                            file = { str(event.user_id) : {"auto": True, "lang": "en", "autoLang": "en"}}
                            data = json.dumps(file, ensure_ascii=False, indent=2)
                            f.write(data)
                except Exception as e:
                    with open(("./logs/logs" + " " + date +".log"),"a", encoding='utf-8') as f:
                        f.write("\n" + "<" + time + ">" + " --> " + "data file error:" + str(e))
                        
                        
            if event.from_user:
                print(event.user_id)
            elif event.from_chat:
                print(event.user_id, 'в беседе', event.chat_id)
            elif event.from_group:
                print('группы', event.group_id)

            print('Текст: ', event.text)
            print()
            if event.to_me and event.text[0] == "/":
                with open(("./logs/logs" + " " + date +".log"),"a", encoding='utf-8') as f:
                    f.write("\n" + "<" + time + ">" + " --> " + event.text + " " + processing(event))
            elif event.to_me and event.text[0] != "/" and auto == True:
                try:
                    with open(("./logs/logs" + " " + date +".log"),"a", encoding='utf-8') as f:
                        f.write("\n" + "<" + time + ">" + " --> " + event.text + " 'script: translator.py' --> " + translator.auto(event,vk))
                except Exception as e:
                    with open(("./logs/logs" + " " + date +".log"),"a", encoding='utf-8') as f:
                        f.write("\n" + "<" + time + ">" + " --> " + event.text + " script error: 'translator.py' --> " + str(e))
                    
                    
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
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    attachment=item['attachment'],
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
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message=data["output"][language]["commNoExx"]
                        )

            done = True
        
    if done == False:
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message=data["output"][language]["unkComm"]
        )
    return text

if __name__ == '__main__':
    main()