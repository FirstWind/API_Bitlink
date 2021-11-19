import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv, find_dotenv


def shorten_link(url_user):
    url = "https://api-ssl.bitly.com/v4/bitlinks"
    body = {"long_url": url_user, "title": "Битлинк"}
    response = requests.post(url, headers=header, json=body)
    if response.ok:
        return response
    else:
        response.raise_for_status()


def is_bitlink(url_user):
    url_parse = urlparse(url_user)
    bitlink = url_parse.netloc + url_parse.path
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}"
    response = requests.get(url, headers=header)
    if response.ok:
        return bitlink
    else:
        response.raise_for_status()


def count_clicks(bitlink):
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
    response = requests.get(url, headers=header)
    if response.ok:
        return response
    else:
        response.raise_for_status()


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    header = {"Authorization": f"Bearer {os.environ.get('TOKEN_BITLY')}"}

    url_user = input("Input url https://")
    if not urlparse(url_user).scheme:
        url_user = f"https://{url_user}"
    else:
        url_user = f"{url_user}"

    try:
        url_response_is_bitlink = is_bitlink(url_user)
        response_count_clicks = count_clicks(url_response_is_bitlink)
        print(f"По вашей ссылке прошли {response_count_clicks.json()['total_clicks']} раз(a)")
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            try:
                response_shorten_link = shorten_link(url_user)
                print(response_shorten_link.json()["title"], response_shorten_link.json()["link"])
            except requests.HTTPError as e:
                print("Ошибка: {}".format(e))
        else:
            print("Ошибка: {}".format(e))
