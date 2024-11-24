# Field Management webapp

You need to add 2 files to provide environment settings for development:
- `.env` file at the root of the project
- `django/server/local_settings.py` which extends the `server.base_settings`

In the `.env` file, declare the following variables:
```
POSTGRES_PASSWORD=supersecretpassword
```

In the `django/server/local_settings.py`, it is recommended to have the following settings:
```
from server.base_settings import *

# SECURITY WARNING: keep the secret key used a secret!
SECRET_KEY = 'super-secure-secret-key-32sd84373#$0f102!2-dsur'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django-main-db',
        'USER': 'postgres',
        'PASSWORD': 'supersecretpassword',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}
```

## Set up for Dockerized development

The following should be installed on the system:
- Docker 27+

Use `docker compose` to build and start the containers:
```
docker compose up
```

Once the containers have started you will have access to several ports on your localhost:
* http://localhost:5432 - Postgres database
* http://localhost:8000 - Django development server
* http://localhost:5173 - Vue.js web application

Go to the Vue.js URL http://localhost:5173 in your browser to see the webapp running.


## Set up for local development

The following should be installed on the system:
- Python 3.9+
- Poetry 1.8+
- NodeJS 22+
- Vue CLI service
- Postgres 17+

Alternatively, you can use the official Postgres Docker image
so as to avoid running Postgres on your local machine.

In Postgress, create a database named `django-main-db`:
```
CREATE DATABASE django-main-db;
```

Use Poetry to install the backend dependencies:
```
cd django
poetry install
```

Run Django migrations to ensure database connectivity and setup:
```
poetry run python3 manage.py migrate
```

Start the Django development server:
```
poetry run python3 manage.py runserver --settings=server.local_settings
```

Install the Vue project:
```
cd vue
npm install
```

Start the Vue.js web application:
```
npm run dev
```

Go to the Vue.js URL http://localhost:5173 in your browser to see the webapp running.