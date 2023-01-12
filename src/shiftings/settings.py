"""
Django settings for shiftings project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-nz!p&+=-@g_@4xyd9u+5zj^l#)acpzt7li4b=lx4at(vaba1oi'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

PROVIDER = 'Shiftings'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
    'bootstrap5',
    'colorfield',
    'phonenumber_field',
    'shiftings.accounts',
    'shiftings.organizations',
    'shiftings.events',
    'shiftings.shifts',
    'shiftings.cal',
    'shiftings.mail'
]

FEATURES = {
    'event': False
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'shiftings.utils.middlewares.http403.Http403Middleware'
]

ROOT_URLCONF = 'shiftings.urls'

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates',
            os.path.join(os.path.dirname(__file__), 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'builtins': [
                'django.templatetags.static',
                'django.templatetags.i18n',
                'bootstrap5.templatetags.bootstrap5',
                'shiftings.templatetags.base',
                'shiftings.templatetags.debug',
                'shiftings.templatetags.modal',
                'shiftings.cal.templatetags.calendar',
            ],
            'context_processors': [
                'shiftings.utils.context_processors.debug',
                'shiftings.utils.context_processors.feature',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'shiftings.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR.parent / 'test_db' / 'db.sqlite3',
    }
}

LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('user_profile')
AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'shiftings.organizations.backend.OrganizationPermissionBackend'
]

LOCAL_LOGIN_ENABLED = True
OAUTH_ENABLED = False
if OAUTH_ENABLED:
    try:
        from oauth_settings import *
    except ImportError:
        pass
LDAP_ENABLED = False
if LDAP_ENABLED:
    try:
        from ldap_settings import *
    except ImportError:
        pass

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

# mailserver settings
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
# use console backend for debugging
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'support@hadiko.de'

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/
LANGUAGE_CODE = 'en-gb'
LANGUAGES = [
    ['de', 'Deutsch'],
    ['en', 'English'],
]
USE_I18N = True
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

TIME_ZONE = 'UTC'
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'shiftings', 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'shiftings', 'staticfiles')

MEDIA_ROOT = os.path.join(BASE_DIR, 'shiftings', 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

try:
    from shiftings.events.settings import *
    from shiftings.organizations.settings import *
    from shiftings.shifts.settings import *

    # try to load local settings (for production settings or rpc passwords)
    from .local_settings import *
except ImportError:
    pass
