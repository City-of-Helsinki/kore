KORE - School register backend with ReST API
============================================
[![Build status](https://travis-ci.org/City-of-Helsinki/kore.svg?branch=master)](https://travis-ci.org/City-of-Helsinki/kore)
[![codecov](https://codecov.io/gh/City-of-Helsinki/kore/branch/master/graph/badge.svg)](https://codecov.io/gh/City-of-Helsinki/kore)

KORE is a backend service for storing current and historical information about
schools. It is based on a model designed for Helsinki schools, but it is not
supposed to be specific only to Helsinki.

KORE outputs the data by the way of ReST API. The UI pair of KORE is the
imaginatively named KORE-ui. KORE-ui can show the data served out by KORE
in pretty fashion with maps and all. You really should take a
[look](https://koulurekisteri.hel.fi) at it! (It is somewhat Helsinki specific,sadly.)

Editing data is currently done by using a somewhat simplistic UI based on
Django admin. In case you are not familiar with Django admin, it is a simple
forms based editor of Web 1.0 style.

## Installation

This applies to both development and simple production scale (school
information rarely causes a stampede of viewers). Note that you
won't need to follow this approach if you have your own favorite Python
process.

### Prerequisites

* Python 3
* PostgreSQL (other databases are not tested at all)

### Clone the repository
If you haven't already:
```
https://github.com/City-of-Helsinki/kerrokantasi.git
```

### Virtualenv setup

This step creates a virtualenv in your current working directory. You may
place it anywhere you want, although it might to useful to put it somewhere
conceptually close to the source code.

```
virtualenv -p python3 venv
```

Activate the virtualenv (for installing requirements)
```
source venv/bin/activate
```

### Install requirements

We use prequ to manage dependencies. It is a tool similar to pip-tools.
```
prequ sync
```

### Configuration

KORE is a Python/Django project configured in the typical way: a file
containing Python code. However we have created a level of indirection:
`local_settings.py`

The file `local_settings.py.example` contains typical settings you will want
to change when running. It is commented with short explanations of the
relevant settings. Most of them are standard Django settings, and you
should refer to Django documentation for those.

Note though, that only DATABASE needs be set correctly in development.

## Running in development
Django has a development server that autoloads your changes. Remember to
start your virtualenv if you use one.
```
source venv/bin/activate
python manage.py runserver
```

## Running in production
You can serve out KORE using your favorite WSGI-capable application server.
The WSGI-entrypoint for KORE is kore.wsgi or in file kore/wsgi.py. Former
is used by gunicorn, latter by uwsgi. The callable is `application`.

You will also need to serve out static and media folders at /static and /media
in your URL space. Note STATIC_URL and MEDIA_URL settings
