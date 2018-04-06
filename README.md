KORE - School register backend with ReST API
============================================
[![Build status](https://travis-ci.org/City-of-Helsinki/kore.svg?branch=master)](https://travis-ci.org/City-of-Helsinki/kore)
[![codecov](https://codecov.io/gh/City-of-Helsinki/kore/branch/master/graph/badge.svg)](https://codecov.io/gh/City-of-Helsinki/kore)

KORE is a backend service for storing current and historical information about
schools. It is based on a model designed for Helsinki schools, but it is not
supposed to be specific only to Helsinki.

KORE outputs the data by the way of ReST API.

Editing data is currently done by using a somewhat simplistic UI based on
Django admin. In case you are not familiar with Django admin, it is a simple
forms based editor of Web 1.0 style.

## How to set up

### Prerequisites

* Python 3
* PostgreSQL (other databases are not tested at all)

### Installation

This applies to both development and simple production scale (school
information rarely causes a stampede of viewers). Note that you
won't need to follow this approach if you have your own favorite Python
process.

Begin by cloning the repository:
```
https://github.com/City-of-Helsinki/kerrokantasi.git
```

#### Virtualenv setup

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

#### Install requirements

We use prequ to manage dependencies. It is a tool similar to pip-tools.
```
prequ sync
```

#### Configuration

KORE is a Python/Django project configured in the typical way: a file
containing Python code. However we have created a level of indirection:
`local_settings.py`

The file `local_settings.py.example` contains typical settings you will want
to change when running. It is commented with short explanations of the
relevant settings. Most of them are standard Django settings though, and you
should refer to Django documentation for those.

Note though, that only DATABASE needs be set correctly in development.

#### Running development server
Django has a development server that autoloads your changes:

```
python manage.py runserver
```
