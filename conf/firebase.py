import pyrebase
import firebase_admin
from google.cloud.firestore_v1 import Client as FirestoreClient
import base64
from firebase_admin import credentials
import os
from dotenv import load_dotenv

load_dotenv()


# Firebase configuration
config = {
    "apiKey": os.getenv('FIREBASE_API_KEY'),
    "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN'),
    "projectId": os.getenv('FIREBASE_PROJECT_ID'),
    "storageBucket": os.getenv('FIREBASE_STORAGE_BUCKET'),
    "messagingSenderId": os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    "appId": os.getenv('FIREBASE_APP_ID'),
    "databaseURL": "",
}

# Initialize Firebase
firebase = pyrebase.initialize_app(config)

# Initialize Firebase Authentication
auth = firebase.auth()

# Initialize Firebase Storage
#storage = firebase.storage()

# Initialize Firebase only if it's not already initialized
credentials_base64 = os.getenv(
    'GOOGLE_APPLICATION_CREDENTIALS_BASE64')
credentials_bytes = base64.b64decode(credentials_base64)
with open('credentials.json', 'wb') as temp_file:
    temp_file.write(credentials_bytes)
cred = credentials.Certificate('credentials.json')

if not firebase_admin._apps:
    app = firebase_admin.initialize_app(cred)

# Initialize Firebase Firestore
firestore = FirestoreClient.from_service_account_json('credentials.json')
