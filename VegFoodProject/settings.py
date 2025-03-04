"""
Django settings for VegFoodProject project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from decouple import config
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG',cast=bool)

ALLOWED_HOSTS = ['13.201.191.197','127.0.0.1','vegpyfood.com','www.vegpyfood.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'accounts',
    'vendor',
    'menu',
    'marketplace',
    'customers',
    'orders',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'orders.request_object.requestObjectMiddleware',#custom middleware to access request obejct in models

]

ROOT_URLCONF = 'VegFoodProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.context_processor.get_vendor',
                'accounts.context_processor.get_user_profile',
                'accounts.context_processor.getGoogleApiKey',
                'marketplace.context_processors.cart_counter',
                'marketplace.context_processors.get_cart_amount',
            ],
        },
    },
]

WSGI_APPLICATION = 'VegFoodProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.postgresql',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': config('DB_NAME'),
        'USER':config('DB_USER'),
        'PASSWORD':config('DB_PASSWORD'),
        'HOST':config('DB_HOST'),
    }
}

AUTH_USER_MODEL="accounts.User"

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT= BASE_DIR/"static"

STATICFILES_DIRS=["VegFoodProject/static"]

MEDIA_URL = '/media/'

MEDIA_ROOT= BASE_DIR/"media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

#Email configurations
EMAIL_HOST=config('EMAIL_HOST')
EMAIL_PORT=config('EMAIL_PORT',cast=int)
EMAIL_HOST_USER=config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=config('DEFAULT_FROM_EMAIL')

GOOGLE_API_KEY=config('GOOGLE_API_KEY')




BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if DEBUG==True:
    # GDAL Settings
    GDAL_LIBRARY_PATH = os.path.join(BASE_DIR, 'venv', 'Lib', 'site-packages', 'osgeo', 'gdal.dll')

    # GEOS Settings
    GEOS_LIBRARY_PATH = os.path.join(BASE_DIR, 'venv', 'Lib', 'site-packages', 'osgeo', 'geos_c.dll')

    os.environ['PROJ_LIB'] = os.path.join(BASE_DIR, 'venv', 'Lib', 'site-packages', 'osgeo', 'data', 'proj')
    os.environ['PATH'] += os.pathsep + os.path.join(BASE_DIR, 'venv', 'Lib', 'site-packages', 'osgeo')


SECURE_CROSS_ORIGIN_OPENER_POLICY = None

TIME_ZONE = 'Asia/Kolkata'  # Change timezone based on location
USE_TZ = True