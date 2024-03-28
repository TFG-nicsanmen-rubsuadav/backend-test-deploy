from bs4 import BeautifulSoup
import time
import concurrent.futures

# Local imports
from .constants import NOT_AVAILABLE_FIELD, GOOGLE, TRIPADVISOR, THEFORK
from .utils import refactor_phone_number, permission_to_scrap, ReviewSite


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


def get_restaurant_ranking(parent: BeautifulSoup):
    try:
        data_table = parent.find("section", class_="container nopadding reviews").find(
            "div", class_="reviewsBySite").find_all("table")
    except AttributeError:
        data_table = NOT_AVAILABLE_FIELD

    tripadvisor = ReviewSite(TRIPADVISOR)
    google = ReviewSite(GOOGLE)
    the_fork = ReviewSite(THEFORK)

    for dato in data_table:
        for row in dato.find_all('tr')[1:]:
            celda = row.find('a', class_='sitename').img['title']

            tripadvisor.process_reviews(celda, row)
            google.process_reviews(celda, row)
            the_fork.process_reviews(celda, row)

    return tripadvisor.number_opinions, tripadvisor.score, google.number_opinions, google.score, the_fork.number_opinions, the_fork.score


# METHOD FOR GETTING THE OPINIONS OF THE RESTAURANT (FK TO RESTAURANT)
def get_restaurant_opinions(parent: BeautifulSoup):
    comments_data = parent.find("section", class_="container nopadding reviews").find(
        "div", id="reviews").find_all("div", {"itemprop": "review"})
    comments_list = []
    for data in comments_data:
        comment = {}
        comment['review'] = data.find("div", class_="text").text.strip()

        users_data = data.find(
            "div", class_="userSite pull-left")

        comment['date'] = users_data.find(
            "div", class_="ratingDate").text.strip()
        comment['user'] = users_data.span.text.strip()
        comment["rating"] = float(users_data.find(
            "span", class_="stars").text.strip().replace(",", "."))
        site = data.find("div", class_="pull-right site").span.a.text.strip()
        if site not in [TRIPADVISOR, GOOGLE, THEFORK]:
            site = NOT_AVAILABLE_FIELD
        comments_list.append(comment)
    return comments_list


def get_restaurants(page: int):
    results = []
    s = permission_to_scrap("/restaurantes/?page=" + str(page))

    restaurants = s.find("section", id="content").find("div", id="main_content").find("div", class_="searchResults").find_all(
        "div", class_="resultItem")
    for restaurant in restaurants:
        name = restaurant.find("h3", class_="restaurantName")

        restaurant_name = name.a.text.strip()

        try:
            price = name.find_next_sibling(
                "span", class_="price info").text.strip()
        except AttributeError:
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
        ) = get_restaurant_ranking(parent)

        comments_restaurant_list = get_restaurant_opinions(parent)

        # List of comments to be added to the restaurant (FK)
        # TODO: Refactor this to a function
        comments = []

        for comment in comments_restaurant_list:
            comments.append(comment)

        results.append({
            "restaurant_name": restaurant_name,
            "price": price,
            "image": image,
            "delivery": delivery,
            "take_away": take_away,
            "terrace": terrace,
            "full_address": full_address,
            "phone_number": phone_number,
            "website": website,
            "global_score": global_score,
            "tripadvisor_number_opinions": tripadvisor_number_opinions,
            "tripadvisor_score": tripadvisor_score,
            "google_number_opinions": google_number_opinions,
            "google_score": google_score,
            "the_fork_number_opinions": the_fork_number_opinions,
            "the_fork_score": the_fork_score,
            "comments": comments
        })

    return results


def parallel_scraping():
    start_time = time.time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = []
        for result in executor.map(get_restaurants, range(1, 3)):
            results.extend(result)

    end_time = time.time()
    print(f"Time elapsed: {end_time - start_time}")
    return results
