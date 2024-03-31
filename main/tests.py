from rest_framework.test import APITestCase
from rest_framework import status

from conf.firebase import firestore
from google.cloud.firestore import FieldFilter

# local imports
from .scrapping import get_restaurants


class Test(APITestCase):
    def test_scrap_and_store_in_DB(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 45)

        restaurant = response.json()[0]

        restaurant_db = firestore.collection('restaurants').where(filter=FieldFilter(
            'restaurant_name', '==', restaurant['restaurant_name']))

        self.assertTrue(restaurant_db)

    def test_get_restaurants(self):
        restaurants = get_restaurants(1)
        self.assertTrue(len(restaurants) > 0)

        for restaurant in restaurants:
            self.assertIn('restaurant_name', restaurant)
            self.assertIn('price', restaurant)
            self.assertIn('image', restaurant)
