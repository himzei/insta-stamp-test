import os
import json
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())


# Keep secret keys in secrets.json
def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_secret("SECRET_KEY")


DEBUG = True

ALLOWED_HOSTS = ["*"]



THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders"
]

CUSTOM_APPS = [
    "insta_stamp.apps.InstaStampConfig", 
    "insta_admin.apps.InstaAdminConfig", 
]

SYSTEM_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_APPS = SYSTEM_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


if DEBUG: 
    DATABASES = {
        "default": {
            'ENGINE'  : get_secret("DB_ENGINE"),
            'NAME'    : get_secret("DB_NAME"),
            'USER'    : get_secret("DB_USER"),
            'PASSWORD': get_secret("DB_PASSWORD"),
            'HOST'    : get_secret("DB_HOST"),
            'PORT'    : get_secret("DB_PORT"),
            'OPTIONS': {
              'driver': 'ODBC Driver 17 for SQL Server',
              'isolation_level': 'READ UNCOMMITTED'
          }
        }
    }
else: 
#     DATABASES = {
#         "default": dj_database_url.config(
#             conn_max_age=600
#     )
# }
    DATABASES = {
        "default": {
            'ENGINE'  : get_secret("DB_ENGINE"),
            'NAME'    : get_secret("DB_NAME"),
            'USER'    : get_secret("DB_USER"),
            'PASSWORD': get_secret("DB_PASSWORD"),
            'HOST'    : get_secret("DB_HOST"),
            'PORT'    : get_secret("DB_PORT"),
            'OPTIONS': {
              'driver': 'ODBC Driver 17 for SQL Server',
              'isolation_level': 'READ UNCOMMITTED'
          }
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul' 

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:3000', 
    'http://127.0.0.1:3001', 
    'http://localhost:3000',
    'http://localhost:3001',
    "https://stamp-insta-admin.netlify.app",
    "https://animated-rolypoly-a81464.netlify.app",
]
CORS_ALLOW_CREDENTIALS = True


