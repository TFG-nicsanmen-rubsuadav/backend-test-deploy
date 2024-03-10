# Instalation
You need to create a virtual environment and install the requirements using the following commands:
```bash
python -m venv venv
source venv/bin/activate (in Linux/Mac) or .\venv\Scripts\activate (in Windows)
pip install -r requirements.txt
```

# Configuration
You need to add the following conf to your local_settings.py:
```python
FIREBASE_API_KEY = 'your_api_key'
FIREBASE_AUTH_DOMAIN = 'your_auth_domain'
FIREBASE_PROJECT_ID = 'your_project_id'
FIREBASE_STORAGE_BUCKET = 'your_storage_bucket'
FIREBASE_MESSAGING_SENDER_ID = 'your_messaging_sender_id'
FIREBASE_APP_ID = 'your_app_id'
GOOGLE_APPLICATION_CREDENTIALS_BASE64 = 'your_base64_credential'
```
You can get the base64 string from your google credentials file using the following command:
```bash
base64 your_google_credentials.json
```

# Running
```bash
python manage.py runserver
```