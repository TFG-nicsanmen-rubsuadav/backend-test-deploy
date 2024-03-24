from bs4 import BeautifulSoup

# Local imports
from .constants import NOT_AVAILABLE_FIELD
from .utils import refactor_phone_number, permission_to_scrap, process_reviews


def get_restaurant_score(parent: BeautifulSoup):
    try:
        global_score = parent.find("section", id="ranking").find(
            "div", class_="ranking").find("div", id="globalrankingbar").span["class"].pop().replace(".", ",")
    except AttributeError:
        global_score = NOT_AVAILABLE_FIELD

    return global_score


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
        div = data.find("div", class_="pull-right")
        if div is not None and div.a is not None:
            website = div.a["href"]
        else:
            website = NOT_AVAILABLE_FIELD
    except AttributeError:
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


def get_restaurant_opinions(parent: BeautifulSoup):
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

            tripadvisor_number_opinions, tripadvisor_score = process_reviews(
                celda, row, "Tripadvisor", tripadvisor_number_opinions, tripadvisor_score)

            google_number_opinions, google_score = process_reviews(
                celda, row, "Google", google_number_opinions, google_score)

            the_fork_number_opinions, the_fork_score = process_reviews(
                celda, row, "TheFork", the_fork_number_opinions, the_fork_score)

    return tripadvisor_number_opinions, tripadvisor_score, google_number_opinions, google_score, the_fork_number_opinions, the_fork_score


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

            global_score = get_restaurant_score(parent)

            (
                tripadvisor_number_opinions,
                tripadvisor_score,
                google_number_opinions,
                google_score,
                the_fork_number_opinions,
                the_fork_score
            ) = get_restaurant_opinions(parent)
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
