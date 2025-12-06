# projeto/settings.py (ou loja/settings.py, dependendo do nome que você usa)
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- NOVO: Define o caminho da pasta de build do React ---
# Assumimos que o build do React estará em 'MEU_PROJETO/frontend-react/build'
REACT_APP_DIR = os.path.join(BASE_DIR, 'frontend-react/build')
# --------------------------------------------------------

SECRET_KEY = 'django-insecure-teste-rapido'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # CORS deve vir aqui
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
]

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'loja.urls' 

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # --- ALTERADO: Adiciona o caminho do build do React aqui ---
        'DIRS': [REACT_APP_DIR],
        # -----------------------------------------------------------
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

WSGI_APPLICATION = 'loja.wsgi.application' # Ajuste o nome do projeto aqui se for diferente

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

# --- NOVO: Adiciona a busca por arquivos estáticos dentro da pasta build/static ---
STATICFILES_DIRS = [
    os.path.join(REACT_APP_DIR, 'static'),
]
# Define onde coletar os arquivos estáticos (essencial para produção)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_root')
# ----------------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'