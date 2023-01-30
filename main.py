from dotenv import load_dotenv
import requests
import os
import time
import telegram
import logging
import sys


log = logging.getLogger(__file__)


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def main():
    load_dotenv()
    dvmn_token = os.environ.get("DVMN_TOKEN")
    telegram_token = os.environ.get("TELEGRAM_TOKEN")
    tg_chat_id = os.environ.get("TG_CHAT_ID")
    bot = telegram.Bot(token=telegram_token)
    params = {
                "timestamp": None,
    }
    logging.basicConfig(
        filename='app.log',
        filemode='w',
        level=logging.INFO,
        format='%(name)s - %(levelname)s - %(asctime)s - %(message)s'
    )
    log.setLevel(logging.INFO)
    log.addHandler(logging.StreamHandler(stream=sys.stdout))
    log.addHandler(TelegramLogsHandler(bot, tg_chat_id))
    log.info('Бот запущен')
    while True:
        try:
            url = "https://dvmn.org/api/long_polling/"
            headers = {
                        "Authorization": f"Token {dvmn_token}",
            }
            response = requests.get(url, headers=headers,
                                    params=params, timeout=90)
            response.raise_for_status()
            works = response.json()
            status = works.get("status")
            if status == "timeout":
                params["timestamp"] = works.get("timestamp_to_request")
            elif status == "found":
                params["timestamp"] = works.get("last_attempt_timestamp")
                last_attempt = works["new_attempts"][0]
                if last_attempt:
                    lesson_title = last_attempt['lesson_title']
                    lesson_url = last_attempt['lesson_url']
                    is_successful = not last_attempt["is_negative"]
                    header = f"У вас проверили работу '{lesson_title}'\n{lesson_url}"
                    answer = ('''Преподавателю все понравилось, можно
                              приступать к следующему уроку.'''
                              if is_successful
                              else "К сожалению, в работе нашлись ошибки")
                    bot.send_message(text=f"{header}\n{answer}",
                                     chat_id=tg_chat_id)
        except requests.exceptions.ReadTimeout as timeout:
            log.warning(f'Время ожидания вышло: {timeout}')
        except requests.exceptions.ConnectionError as error:
            log.warning(f'Ошибка соединения: {error}')
            time.sleep(10)


if __name__ == "__main__":
    main()
