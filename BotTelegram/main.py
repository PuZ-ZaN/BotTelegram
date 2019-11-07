from telebot import apihelper
from telebot.types import InputMediaPhoto
import telebot
import vk_part
import kartinka
import telegram
import proxy
import time
import sys

TOKEN ='ВАШ ТОКЕН'
bot = telebot.TeleBot(TOKEN)
#присланные сообщения отправлять в консоль
def log(message):
    print("\n------")
    from datetime import datetime
    print(datetime.now())
    print(f"Сообщение от {message.from_user.first_name} {message.from_user.last_name}. (id = {str(message.from_user.id)}) \nТекст = {message.text}")

#функция отправки приветствия
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    log(message)
    bot.send_message(message.chat.id,'Дарова')

#функция отправки замен
@bot.message_handler(regexp="замены")
def send_zameny(message):
    log(message)
    bot.send_chat_action(message.chat.id,telegram.ChatAction.UPLOAD_PHOTO)
    list_jpg,description=vk_part.vk_recognize()
    if description!='':
        bot.send_message(message.chat.id,text=description)
    list_InputMediaPhoto=[]
    for i in list_jpg:
        list_InputMediaPhoto.append(InputMediaPhoto(i))# InputMediaPhoto(i) открывает ссылки в i, возвращает картинки

    #телега не принимает >10 фото в сообщении, если их больше - разбиваем
    ln = len(list_InputMediaPhoto)
    if ln >10:
        i = 1
        ten_photos=[]#пачка
        while i <= ln:
            ten_photos.append(list_InputMediaPhoto[i-1])
            if i%10==0:
                bot.send_media_group(chat_id=message.chat.id, media=ten_photos)#отправляем пачками по 10
                ten_photos.clear()#очищаем массив
            i+=1
        bot.send_media_group(chat_id=message.chat.id,media=ten_photos)#отправляем последнюю, возможно неполную пачку(<10 фото)
    else:
        bot.send_media_group(chat_id=message.chat.id, media=list_InputMediaPhoto)



factor=50 #"количество" шума
#функция вывода переменной factor
@bot.message_handler(commands=["factor"])
def answer(message):
    global factor
    log(message)
    try:
        factor = int(message.text.split(maxsplit=1)[1]) # В переменной будет всё,что идёт после /command
    except Exception as e:
        bot.send_message(message.chat.id,"Введите число")
    bot.send_message(message.chat.id,"factor = "+str(factor))

#функция обработки изображений
@bot.message_handler(content_types=['photo'])
def jpeg_modify_n_send(message):
    log(message)
    #bot.send_chat_action(message.chat.id, telegram.ChatAction.UPLOAD_PHOTO)
    fileID = message.photo[len(message.photo)-1].file_id
    file = bot.get_file(fileID)
    kr = kartinka.kartinka(bot.download_file(file.file_path))
    kr.negative()
    kr.shum(factor)
    bot.send_photo(message.chat.id,photo=kr.image_to_bytes())

#проверка аргументов
if len(sys.argv)==1:
    try:
        #запуск бота
        bot.polling() #none_stop=True, interval=0
    except Exception as e:
        #перебор прокси-серверов в файле
        while True:
            proxyAddress=proxy.get_prox()
            if proxyAddress:
                apihelper.proxy = {'https': f'https://{proxyAddress}','http': f'http://{proxyAddress}'}
            print("Бот запущен...")
            try:
                bot.polling()
            except:
                print("Ожидайте 7 сек.")
                time.sleep(7)
else:
    if sys.argv[1]!='noproxy':
        proxyAddress=sys.argv[1]
        apihelper.proxy = {'https': f'https://{proxyAddress}','http': f'http://{proxyAddress}'}
        print("Прокси "+ str(proxyAddress))
        print("Бот запущен...")
        bot.polling()
    else:
        print("Бот запущен...")
        bot.polling()
