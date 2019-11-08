# О проекте
Telegram бот имеет следующий функционал:
  * Обработка отправленного пользователем изображения - модуль kartinka.py
  * Отправка изображений из последних постов указанной группы VK - модуль vk_part.py
  
За взаимодействие с пользователем через Telegram отвечает модуль main.py, главный модуль. Он использует функции и обьекты из других модулей

За взаимодействие с прокси-сервером отвечает модуль proxy.py

# Установка и настройка

Для работы боту требуются:
* Логин и пароль VK для запросов в группу от этого аккаунта, задается в файле vk_part.py
* Имя используемой группы  VK, задается в файле vk_part.py
* Токен бота телеграм, можно получить у @BotFather, задается в файле main.py

Требуется python 3.7 и выше

Зависимости проекта: PIL, Telebot, Requests, VK_api. Установить можно командой: 

```pip install Pillow requests pyTelegramBotApi vk_api```

Предварительно рекомендую создать окружение pipenv или подобные

Скачайте проект, задайте в файлах необходимые параметры.
Запустите командой ```python main.py```

В случае недоступности серверов Telegram, бот пытается использовать прокси-сервера из файла proxy_list.txt.
Может потребоваться добавить в него актуальные прокси в формате ```IP:PORT```
