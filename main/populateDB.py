from django.core.management.base import BaseCommand
from tqdm import tqdm  # Progress bar
from colorama import Fore, Style  # Colors
import concurrent.futures  # Parallel processing
from google.cloud.firestore import FieldFilter

# local imports
from conf.firebase import firestore
from .scrapping import parallel_scraping


def insert_restaurant(restaurant: dict):
    comments = restaurant.pop('comments', [])
    existing_restaurant = firestore.collection('restaurants').where(filter=FieldFilter(
        'restaurant_name', '==', restaurant['restaurant_name'])).where(filter=FieldFilter('full_address', '==', restaurant['full_address'])).get()
    if existing_restaurant:
        return
    _, restaurant_ref = firestore.collection('restaurants').add(restaurant)
    for comment in comments:
        _, _ = restaurant_ref.collection('comments').add(comment)


class PopulateDatabase(BaseCommand):
    help = 'Populate the database with the data from the scrapping'

    def populate(self, *args, **options):
        restaurants = parallel_scraping()
        with tqdm(total=len(restaurants), desc="Populating database") as pbar:
            with concurrent.futures.ProcessPoolExecutor() as executor:
                futures = []
                for i, restaurant in enumerate(restaurants):
                    futures.append(executor.submit(
                        insert_restaurant, restaurant))
                    pbar.update(1)

                    percent_complete = (i + 1) / len(restaurants) * 100

                    if 0 <= percent_complete <= 25:
                        color = Fore.RED
                    elif 25 < percent_complete <= 50:
                        color = Fore.YELLOW
                    elif 50 < percent_complete <= 75:
                        color = Fore.GREEN
                    else:
                        color = Fore.BLUE

                    pbar.set_description(
                        f'{color}Populating database{Style.RESET_ALL}')

                concurrent.futures.wait(futures)
        self.stdout.write(self.style.SUCCESS(
            f'Database populated successfully, populated {len(restaurants)} restaurants'))

        return restaurants
