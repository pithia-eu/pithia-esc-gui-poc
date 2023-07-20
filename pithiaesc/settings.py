"""
Django settings for pithiaesc project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

import os
import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env(
    ALLOWED_HOSTS=('127.0.0.1,localhost,18.134.0.206,pithia.yangcpc.site'),
    CSRF_TRUSTED_ORIGINS=''
)

if env('CSRF_TRUSTED_ORIGINS') != '':
    CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS').split(',')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(',')


# Application definition

INSTALLED_APPS = [
    'common.apps.CommonConfig',
    'browse.apps.BrowseConfig',
    'delete.apps.DeleteConfig',
    'handle_management.apps.HandleManagementConfig',
    'ontology.apps.OntologyConfig',
    'present.apps.PresentConfig',
    'register.apps.RegisterConfig',
    'resource_management.apps.ResourceManagementConfig',
    'search.apps.SearchConfig',
    'update.apps.UpdateConfig',
    'user_management.apps.UserManagementConfig',
    'utils.apps.UtilsConfig',
    'validation.apps.ValidationConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.middleware.LoginMiddleware',
    'utils.middleware.InstitutionSelectionMiddleware',
    'utils.middleware.InstitutionSelectionFormMiddleware',
]

ROOT_URLCONF = 'pithiaesc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'project_tags': 'utils.templatetags.project_tags'
            }
        },
    },
]

WSGI_APPLICATION = 'pithiaesc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ['DATABASE_ENGINE'],
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_READ_USER'],
        'PASSWORD': os.environ['DATABASE_READ_PASSWORD'],
        'HOST': os.environ['DATABASE_HOST'],
        'PORT': os.environ['DATABASE_PORT'],
    },
    'esc_rw': {
        'ENGINE': os.environ['DATABASE_ENGINE'],
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_WRITE_USER'],
        'PASSWORD': os.environ['DATABASE_WRITE_PASSWORD'],
        'HOST': os.environ['DATABASE_HOST'],
        'PORT': os.environ['DATABASE_PORT'],
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'GMT'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Sessions

SESSION_SAVE_EVERY_REQUEST = True

LOGIN_REQUIRED_URLS = (
    r'/authorised/',
)

LOGIN_REQUIRED_URLS_EXCEPTIONS = (
    r'/login/(.*)$',
    r'/logout/(.*)$',
)
# Logging

#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'formatters': {
#        'custom': {
#            'format': '[{asctime}] [{levelname}] [{name}]  {message}',
#            'style': '{',
#        },
#    },
#    'handlers': {
#        'file': {
#            'level': 'INFO',
#            'class': 'logging.FileHandler',
#            'filename': os.path.join(BASE_DIR, 'pithiaesc.log'),
#            'formatter': 'custom',
#        },
#        'console': {
#            'level': 'INFO',
#            'class': 'logging.StreamHandler',
#        }
#    },
#    'loggers': {
#        '': {
#            'handlers': ['file', 'console'],
#            'level': 'INFO',
#            'propagate': True,
#        },
#    },
#}
