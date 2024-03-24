from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import time

# Local imports
from .constants import MAIN_URL


def refactor_phone_number(phone_number: str):
    if phone_number.startswith("+34"):
        phone_number = phone_number[3:]
    phone_number = phone_number.replace(" ", "")
    phone_number = phone_number.replace("-", "")

    return phone_number


def permission_to_scrap(url):
    headers = {'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'es'}
    request = urllib.request.Request(
        MAIN_URL + url, headers=headers)

    tiempo_espera = 1
    while True:
        try:
            f = urllib.request.urlopen(request)
            return BeautifulSoup(f, 'lxml')
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(
                    f"Error 429: Demasiadas solicitudes. Esperando {tiempo_espera} segundos.")
                time.sleep(tiempo_espera)
                tiempo_espera += 1


def process_reviews(celda, row: BeautifulSoup, site_name, number_opinions, score):
    if site_name in celda:
        if row.find('td', class_='rightText') is not None:
            review_row = row.find_next("td", class_="rightText")

            if review_row.text.strip():
                number_opinions = int(review_row.text.strip())
            else:
                number_opinions = 0

            score = float(review_row.find_next(
                "td", class_="rightText rating").text.strip().replace(",", "."))
        else:
            number_opinions = 0
            score = 0.
    return number_opinions, score
