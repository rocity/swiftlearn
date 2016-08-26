import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = True

ALLOWED_HOSTS = ['']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEFAULT_FROM_EMAIL = ''
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 465
EMAIL_USE_SSL = True
<<<<<<< HEAD:swiftlearn/example.local_settings.py
=======

PAYPAL_RECEIVER_EMAIL = 'swiftkindgong-facilitator@gmail.com'
>>>>>>> Paypal payment:swiftlearn/local_settings.py
