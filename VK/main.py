# -*- coding: utf-8 -*-
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import datetime
import json
    
with open('messages.json', 'r') as json_file:
    data = json.load(json_file)
data_json = json.dumps(data)
text = json.loads(data_json)

date = str(datetime.datetime.now().year) + "." + str(datetime.datetime.now().month) + "." + str(datetime.datetime.now().day)

vk_session = vk_api.VkApi(token='vk1.a.RHNQsEEP0NWNQJtyHVVBoclBzqRW9Sr_Pquuo5-1aVhXwMgceSCQTE7zplpT76Rn83IoADxz0iH1TDIAcTtXBGKSoyKSDc_Fj9KyjpzyuUbx3xe9_AMPVhZlugBSJ1MW8NuYxy18vI5oQartR_rjV-4T8MP3ssA5Ba344VM49EN31kGNg2Nbm-q5JSJSRUnTXMBZMQl6smFxqIBKYL6F5w')

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

def main():
    """ Пример использования longpoll

        https://vk.com/dev/using_longpoll
        https://vk.com/dev/using_longpoll_2
    """

    for event in longpoll.listen():
        time = str(datetime.datetime.now().hour) + "." + str(datetime.datetime.now().minute) + "." + str(datetime.datetime.now().second) + "." + str(datetime.datetime.now().microsecond)
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')

            if event.from_me:
                print('От меня для: ', end='')
            elif event.to_me:
                print('Для меня от: ', end='')

            if event.from_user:
                print(event.user_id)
            elif event.from_chat:
                print(event.user_id, 'в беседе', event.chat_id)
            elif event.from_group:
                print('группы', event.group_id)

            print('Текст: ', event.text)
            print()
            if event.to_me:
                with open(("logs" + " " + date),"a") as f:
                    f.write("\n" + "<" + time + ">" + " --> " + event.text)
                if mess(event) == False:
                    with open(("logs" + " " + date),"a") as f:
                        f.write(" --> " + "<ignore>")
                    
def mess(event):   
    for i in range(len(text)):  
        if event.text in text[i]['read'] and event.to_me:
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                attachment=text[i]['attachment'],
                message=text[i]['message']
            )
            with open(("logs" + " " + date),"a") as f:    
                f.write(" --> " + str(text[i]['message']))
            return True
    return False


if __name__ == '__main__':
    main()