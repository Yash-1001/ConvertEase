import os

import dj_database_url



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'your-secret-key'  # Replace with your secret key

DEBUG = True


ALLOWED_HOSTS = ['convertease-1.onrender.com', 'localhost', '127.0.0.1']


INSTALLED_APPS = [
    # Default Django apps...
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your app
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',  # Optional if you want full control
    'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'ConvertEase.urls'  # Fixed case to match folder name

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'ConvertEase.wsgi.application'  # Fixed case to match folder name

# DATABASES = {
#     'default': dj_database_url.config(
#         default=os.getenv("DATABASE_URL")
#     )
# }

import dj_database_url
import os

DATABASES = {
    'default': dj_database_url.parse(
        os.environ.get('DATABASE_URL', 'postgresql://convertease_db_user:T2IiFdRDwzPgYpsVmEKiSR9CN1fbak3n@dpg-d0o56bqli9vc73fmj6t0-a.oregon-postgres.render.com/convertease_db')
    )
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME', 'convertease_db'),
#         'USER': os.environ.get('DB_USER', 'convertease_db_user'),
#         'PASSWORD': os.environ.get('DB_PASSWORD', 'T2IiFdRDwzPgYpsVmEKiSR9CN1fbak3n'),
#         'HOST': os.environ.get('DB_HOST', 'dpg-d0o56bqli9vc73fmj6t0-a'),
#         'PORT': os.environ.get('DB_PORT', '5432'),
#     }
# }

# Static files (CSS, JavaScript)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'core', 'static')]

# Media files (Uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'
LOGIN_URL = '/login/'