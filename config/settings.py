"""
Configuração do projeto Ataraxia.

Os padrões servem ao desenvolvimento: sem nenhuma variável de ambiente
definida, o projeto roda com SQLite e DEBUG ligado. Produção é configurada
inteiramente por variáveis — ver `.env.example`.

Documentação do Django 6.1:
https://docs.djangoproject.com/en/6.1/ref/settings/
"""

import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega o `.env` da raiz do projeto, se existir. Variáveis já definidas no
# ambiente têm precedência sobre o arquivo.
load_dotenv(BASE_DIR / '.env')


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {'1', 'true', 'on', 'yes', 'sim'}


def env_list(name):
    value = os.environ.get(name, '')
    return [item.strip() for item in value.split(',') if item.strip()]


# Segurança -------------------------------------------------------------------

DEBUG = env_bool('DJANGO_DEBUG', default=True)

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured(
            'Defina DJANGO_SECRET_KEY para rodar com DEBUG desligado. '
            'Gere uma chave com: '
            'python -c "from django.core.management.utils import '
            'get_random_secret_key; print(get_random_secret_key())"'
        )
    # Chave fixa de desenvolvimento. Nunca é usada com DEBUG desligado.
    SECRET_KEY = 'django-insecure-chave-de-desenvolvimento-nao-use-em-producao'

ALLOWED_HOSTS = env_list('DJANGO_ALLOWED_HOSTS')
if DEBUG and not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

CSRF_TRUSTED_ORIGINS = env_list('DJANGO_CSRF_TRUSTED_ORIGINS')

if not DEBUG:
    # O tráfego chega por um proxy que termina o TLS; sem este cabeçalho o
    # Django acha que a requisição veio em HTTP e entra em laço de redirecionamento.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31_536_000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    X_FRAME_OPTIONS = 'DENY'


# Aplicações ------------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # As aplicações do projeto entram aqui conforme forem criadas.
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Serve os arquivos estáticos em produção, sem depender do nginx.
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Banco de dados --------------------------------------------------------------
#
# Com DATABASE_URL definida, usa o banco apontado por ela (Postgres em
# produção). Sem ela, cai em SQLite — que é o caso na máquina de cada
# integrante. Trocar de banco é definir a variável; o código não muda.

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600),
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Autenticação ----------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# Internacionalização ---------------------------------------------------------

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Arquivos estáticos e de mídia -----------------------------------------------

STATIC_URL = 'static/'
STATIC_ROOT = Path(os.environ.get('DJANGO_STATIC_ROOT', BASE_DIR / 'staticfiles'))
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = 'media/'
MEDIA_ROOT = Path(os.environ.get('DJANGO_MEDIA_ROOT', BASE_DIR / 'media'))

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}


# E-mail ----------------------------------------------------------------------

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}
