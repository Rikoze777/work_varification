from dotenv import load_dotenv
import requests
import os
import pprint


def fetch_work_status(token):
    url = "https://dvmn.org/api/user_reviews/"
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    json_response = response.json()
    return json_response


def main():
    load_dotenv()
    dvmn_token = os.environ.get("DVMN_TOKEN")
    pprint.pprint(fetch_work_status(dvmn_token))


if __name__ == "__main__":
    main()
