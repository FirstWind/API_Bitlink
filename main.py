import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv, find_dotenv


def shorten_link(url_user):
    url = "https://api-ssl.bitly.com/v4/bitlinks"
    body = {"long_url": url_user, "title": "Битлинк"}
    response = requests.post(url, headers=header, json=body)
    return (response.ok, response)


def is_bitlink(url_user):
    url_parse = urlparse(url_user)
    bitlink = url_parse.netloc + url_parse.path
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}"
    response = requests.get(url, headers=header)
    return (response.ok, bitlink)


def count_clicks(bitlink):
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
    response = requests.get(url, headers=header)
    return (response.ok, response)


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    header = {"Authorization": f"Bearer {os.environ.get('TOKEN_BITLY')}"}

    url_user = input("Input long url to make it short https://")
    if urlparse(url_user).scheme:
        url_user = f"https://{url_user}"
    else:
        url_user = f"{url_user}"


    try:
        status_ok, url_response_is_bitlink = is_bitlink(url_user)
        if status_ok:
            status_ok, response_count_clicks = count_clicks(url_response_is_bitlink)
            if status_ok:
                print(f"По вашей ссылке прошли {response_count_clicks.json()['total_clicks']} раз(a)")
            else:
                print(f"Ошибка подключения. Адрес: {url_response_is_bitlink}\n {response_count_clicks.text}")

        else:
            status_ok, response_shorten_link = shorten_link(url_user)
            if status_ok:
                print(response_shorten_link.json()["title"], response_shorten_link.json()["link"])
            else:
                print(f"Ошибка подключения. Адрес: {url_user}\n {response_shorten_link.text}")

    except requests.exceptions.RequestException as e:
        print("Ошибка: {}".format(e))