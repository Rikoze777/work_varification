# work_varification

Бот для оповещения проверки работ [dvmn](https://dvmn.org/)

## Как установить

Для использования необходимо:

1. Зарегестрироваться на сайте [dvmn](https://dvmn.org/)

2. Получить token на [странице](https://dvmn.org/api/docs/)

3. Создайте пустой .env файл в корне с исполнительным файлом

В .env поместите следующие переменные:
```
DVMN_TOKEN="Ваш dvmn токен"
TELEGRAM_TOKEN="Токен бота"
CHAT_ID="ваш id в телеграм"
```

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

## Запуск скрипта
```
python3 main.py
```

##  Пример успешного запуска

Итогом будет получение вами сообщения от бота 
```
У вас проверили работу 'Отправляем уведомления о проверке работ'
https://dvmn.org/modules/chat-bots/lesson/devman-bot/
К сожалению, в работе нашлись ошибки
```