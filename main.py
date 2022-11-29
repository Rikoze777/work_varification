from dotenv import load_dotenv
import requests
import os
import time
import telegram


def fetch_work_response(token, params):
    url = "https://dvmn.org/api/long_polling/"
    headers = {
                "Authorization": f"Token {token}",
    }
    response = requests.get(url, headers=headers, params=params, timeout=70)
    response.raise_for_status()
    json_response = response.json()
    return json_response


def main():
    load_dotenv()
    dvmn_token = os.environ.get("DVMN_TOKEN")
    telegram_token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("CHAT_ID")
    bot = telegram.Bot(token=telegram_token)
    params = {
                "timestamp": None,
    }
    while True:
        try:
            try:
                json_response = fetch_work_response(dvmn_token, params)
                status = json_response.get("status")
            except requests.exceptions.ReadTimeout:
                continue
            except requests.exceptions.ConnectionError:
                continue
            if status == "timeout":
                params["timestamp"] = json_response.get("timestamp_to_request")
            elif status == "found":
                params["timestamp"] = json_response.get("last_attempt_timestamp")
                last_attempt = json_response["new_attempts"][0]
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
                                     chat_id=chat_id)
        except requests.exceptions.ReadTimeout:
            time.sleep(10)
        except requests.exceptions.ConnectionError:
            time.sleep(10)


if __name__ == "__main__":
    main()
