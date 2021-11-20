import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv, find_dotenv


def shorten_link(url_bitly, url, header):
    body = {"long_url": url, "title": "Битлинк"}
    response = requests.post(url_bitly, headers=header, json=body)
    response.raise_for_status()
    return response.json()['link']


def is_bitlink(url_bitly, bitlink, header):
    url = f"{url_bitly}{bitlink}"
    response = requests.get(url, headers=header)
    return response.ok


def count_clicks(url_bitly, bitlink, header):
    url = f"{url_bitly}{bitlink}/clicks/summary"
    response = requests.get(url, headers=header)
    response.raise_for_status()
    return response.json()["total_clicks"]


if __name__ == "__main__":
    url_bitly = "https://api-ssl.bitly.com/v4/bitlinks/"

    load_dotenv(find_dotenv())
    header = {"Authorization": f"Bearer {os.environ.get('TOKEN_BITLY')}"}

    input_url = input("Input url: ")
    url_parsed = urlparse(input_url)
    url_bitlink = url_parsed.netloc + url_parsed.path

    try:
        if is_bitlink(url_bitly, url_bitlink, header):
            clicks = count_clicks(url_bitly, url_bitlink, header)
            print(f"По вашей ссылке прошли {clicks} раз(a)")
        else:
            if not url_parsed.scheme:
                print("Ошибка! Ссылку ввели неправильно, без http(s)")
                exit()
            bitlink = shorten_link(url_bitly, input_url, header)
            print(f"Битлинк: {bitlink}")
    except requests.HTTPError as e:
        print("Ошибка: {}".format(e))
