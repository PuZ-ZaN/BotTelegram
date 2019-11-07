import time
import vk_api
import datetime

def vk_recognize(day_nazad=1,skolko_postov=2):#'''Получаем картинки из группы вк за опред колво суток'''
    vk_session = vk_api.VkApi('ЛОГИН', 'ПАРОЛЬ')# ЛОГИН ПАРОЛЬ , юзаются куки,но номер нужен
    vk_session.auth()
    vk = vk_session.get_api()
    arr=vk.wall.get(domain='YOUR_PARSE_GROUP',count=skolko_postov,)
    nowUnixTime=int(time.time())+18000 #Исправление часовых поясов для Екб
    daysBackUT=nowUnixTime-86400*day_nazad #Задает сколько суток назад выложили пост, т.е нижний предел
    dataList=[]#будем возвращать массив ССЫЛОК на картинки
    thisPost=0
    textPost=''
    while thisPost<len(arr['items']):
        #перейти на следующий пост,если этот помечен как реклама, и старше чем указано
        if arr['items'][thisPost]['marked_as_ads']!='' and arr['items'][thisPost]['post_type']!='post' and not (arr['items'][thisPost]['date'] in range(daysBackUT,nowUnixTime)):
            thisPost += 1
            continue
        if arr['items'][thisPost]['text'] !='':
            date = datetime.datetime.fromtimestamp(int(arr['items'][thisPost]['date'])).strftime('%Y-%m-%d %H:%M:%S')
            textPost+= f"Пост №: {thisPost} Дата и время: {date} Текст: {arr['items'][thisPost]['text']}\n"

        thisPhoto=0
        try:
            while thisPhoto < len(arr['items'][thisPost]['attachments']):#перебор элементов в посте
                #если элемент - картинка
                if arr['items'][thisPost]['attachments'][thisPhoto]['type']=='photo':
                    #нас интересует самая лучшая (по разрешению) картинка (lenSizes-1)
                    lenSizes=len(arr['items'][thisPost]['attachments'][thisPhoto]['photo']['sizes'])
                    dataList.append(arr['items'][thisPost]['attachments'][thisPhoto]['photo']['sizes'][lenSizes-1]['url'])
                thisPhoto+=1
        except KeyError:
            thisPost += 1
            continue
        thisPost += 1
    return dataList,textPost

