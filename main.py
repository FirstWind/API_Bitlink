import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv, find_dotenv


def shorten_link(url_bitly, url):
    body = {"long_url": url, "title": "Битлинк: "}
    r = requests.post(url_bitly, headers=header, json=body)
    r.raise_for_status()
    return r


def is_bitlink(url_bitly, bitlink):
    url = f"{url_bitly}{bitlink}"
    r = requests.get(url, headers=header)
    return r.ok


def count_clicks(url_bitly, bitlink):
    url = f"{url_bitly}{bitlink}/clicks/summary"
    r = requests.get(url, headers=header)
    r.raise_for_status()
    return r


def parts_json(json, *args):
    result = ""
    for element in args:
        result += str(json[element])
    return result


if __name__ == "__main__":
    url_bitly = "https://api-ssl.bitly.com/v4/bitlinks/"

    load_dotenv(find_dotenv())
    header = {"Authorization": f"Bearer {os.environ.get('TOKEN_BITLY')}"}

    input_url = input("Input url: ")
    url_parsed = urlparse(input_url, scheme='https')
    url_bitlink = url_parsed.netloc + url_parsed.path
    if not url_parsed.scheme:
        input_url = f"{url_parsed.scheme}://{input_url}"

    try:
        if is_bitlink(url_bitly, url_bitlink):
            response_count_clicks = count_clicks(url_bitly, url_bitlink)
            clicks = parts_json(response_count_clicks.json(), "total_clicks")
            print(f"По вашей ссылке прошли {clicks} раз(a)")
        else:
            response_shorten_link = shorten_link(url_bitly, input_url)
            clicks = parts_json(response_shorten_link.json(), "title", "link")
            print(clicks)
    except requests.HTTPError as e:
        print("Ошибка: {}".format(e))
