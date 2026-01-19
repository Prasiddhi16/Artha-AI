import os
from pathlib import Path
import pymysql

# PyMySQL setup for Django MySQL backend
pymysql.version_info = (2, 2, 1, 'final', 0)
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = 'django-insecure-78(tzg5ghtga(nqa47=q6&z5vg@60=01x6b15qbz#z(ff-h!%+'
SECRET_KEY = 'put key of homepage here'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',  # Added for frontend connection
    'social_django',  
    'myapp', 
   


]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
SITE_ID = 1

SOCIAL_AUTH_PIPELINE = (
      'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    
    # custom success message
    'myapp.social_pipeline.google_signup_message',
    'myapp.social_pipeline.redirect_to_set_password',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'put key of google auth here'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'put key of google auth here'

SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['first_name', 'last_name']

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # Added at the top
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',

            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'artha_db',
        'USER': 'artha_user',
        'PASSWORD': 'MySQL@1234',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Custom User Model
AUTH_USER_MODEL = 'myapp.User'

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS = True # Allows any frontend to connect (local development only)

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'   # or your provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'email'
EMAIL_HOST_PASSWORD = 'passb' # use app password, not real password



# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = []
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/signin/'
LOGIN_REDIRECT_URL = '/set-password/'
LOGOUT_REDIRECT_URL = '/signin/'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/set-password/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/signin/'
