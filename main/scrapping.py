import time
from bs4 import BeautifulSoup
import urllib.request
import urllib.error

# Local imports
from .constants import NOT_AVAILABLE_FIELD, MAIN_URL
from .utils import refactor_phone_number


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


def get_restaurant_score(parent: BeautifulSoup):
    try:
        global_score = parent.find("section", id="ranking").find(
            "div", class_="ranking").find("div", id="globalrankingbar").span["class"].pop().replace(".", ",")
    except AttributeError:
        global_score = NOT_AVAILABLE_FIELD

    try:
        data_table = parent.find("section", class_="container nopadding reviews").find(
            "div", class_="reviewsBySite").find_all("table")
    except AttributeError:
        data_table = NOT_AVAILABLE_FIELD

    tripadvisor_number_opinions = 0
    tripadvisor_score = 0.

    google_number_opinions = 0
    google_score = 0.

    the_fork_number_opinions = 0
    the_fork_score = 0.

    for dato in data_table:
        for row in dato.find_all('tr')[1:]:
            celda = row.find('a', class_='sitename').img['title']
            # Tripadvisor
            if "Tripadvisor" in celda:
                if row.find('td', class_='rightText') is not None:
                    trivadvisor_row = row.find_next("td", class_="rightText")

                    tripadvisor_number_opinions = int(
                        trivadvisor_row.text.strip())
                    tripadvisor_score = float(trivadvisor_row.find_next(
                        "td", class_="rightText rating").text.strip().replace(",", "."))
                else:
                    tripadvisor_number_opinions = 0
                    tripadvisor_score = 0.
            # Google Reviews
            if "Google" in celda:
                if row.find('td', class_='rightText') is not None:
                    google_row = row.find_next("td", class_="rightText")

                    google_number_opinions = int(
                        google_row.text.strip())
                    google_score = float(google_row.find_next(
                        "td", class_="rightText rating").text.strip().replace(",", "."))
                else:
                    google_number_opinions = 0
                    google_score = 0.
            # TheFork
            if "TheFork" in celda:
                if row.find('td', class_='rightText') is not None:
                    the_fork_row = row.find_next("td", class_="rightText")

                    the_fork_number_opinions = int(
                        the_fork_row.text.strip())
                    the_fork_score = float(the_fork_row.find_next(
                        "td", class_="rightText rating").text.strip().replace(",", "."))
                else:
                    the_fork_number_opinions = 0
                    the_fork_score = 0.

    return global_score, tripadvisor_number_opinions, tripadvisor_score, google_number_opinions, google_score, the_fork_number_opinions, the_fork_score


def get_restaurant_info(parent: BeautifulSoup):
    try:
        data = parent.find("section", class_="row").find(
            "div", class_="hl_row")
        data_adress = data.a
    except AttributeError:
        data = NOT_AVAILABLE_FIELD
        data_adress = NOT_AVAILABLE_FIELD

    try:
        street_address = data_adress.span.text.strip()
    except AttributeError:
        street_address = NOT_AVAILABLE_FIELD

    try:
        address_locality = data_adress.find(
            "span", {"itemprop": "addressLocality"}).text.strip()
    except AttributeError:
        address_locality = NOT_AVAILABLE_FIELD

    full_address = street_address + ", " + address_locality

    try:
        phone_number = data.find(
            "a", class_="i-block").span.text.strip()
    except AttributeError:
        phone_number = NOT_AVAILABLE_FIELD

    phone_number = refactor_phone_number(phone_number)

    try:
        website = data.find("div", class_="pull-right").a["href"]
    except:
        website = NOT_AVAILABLE_FIELD

    return full_address, phone_number, website


def get_restaurant_services(name: BeautifulSoup):
    delivery = False
    take_away = False
    terrace = False

    services = name.find_parent().find_all("a", class_="btn")
    for service in services:
        label = service.i["title"]
        if "Pedidos para llevar" in label:
            take_away = True
        elif "Terraza" in label:
            terrace = True
        elif "Pedidos a domicilio" in label:
            delivery = True

    return delivery, take_away, terrace


def populateDB():
    for i in range(1, 3):
        s = permission_to_scrap("/restaurantes/?page=" + str(i))

        restaurants = s.find("section", id="content").find("div", id="main_content").find("div", class_="searchResults").find_all(
            "div", class_="resultItem")
        for restaurant in restaurants:
            name = restaurant.find("h3", class_="restaurantName")

            restaurant_name = name.a.text.strip()

            try:
                price = name.find_next_sibling(
                    "span", class_="price info").text.strip()
            except:
                price = NOT_AVAILABLE_FIELD

            try:
                image = restaurant.find(
                    "div", class_="col-md-7").a.img["data-src"]
            except AttributeError:
                image = NOT_AVAILABLE_FIELD

            delivery, take_away, terrace = get_restaurant_services(name)

            local_url = restaurant.find(
                "h3", class_="restaurantName").a["href"]
            s2 = permission_to_scrap(local_url)
            parent = s2.find("body", class_="restaurant")

            full_address, phone_number, website = get_restaurant_info(parent)

            (
                global_score,
                tripadvisor_number_opinions,
                tripadvisor_score,
                google_number_opinions,
                google_score,
                the_fork_number_opinions,
                the_fork_score
            ) = get_restaurant_score(parent)
            print(f"Restaurant: {restaurant_name}")
            print(f"Price: {price}")
            print(f"Address: {full_address}")
            print(f"Phone: {phone_number}")
            print(f"Website: {website}")
            print(f"Delivery: {delivery}")
            print(f"Take Away: {take_away}")
            print(f"Terrace: {terrace}")
            print(f"Global Score: {global_score}")
            print(f"TripAdvisor Opinions: {tripadvisor_number_opinions}")
            print(f"TripAdvisor Score: {tripadvisor_score}")
            print(f"Google Opinions: {google_number_opinions}")
            print(f"Google Score: {google_score}")
            print(f"The Fork Opinions: {the_fork_number_opinions}")
            print(f"The Fork Score: {the_fork_score}")
            print(f"Image: {image}")
            print("\n\n")
