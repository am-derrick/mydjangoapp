# The Forum

[![Python Version](https://img.shields.io/badge/python-3.8-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-4.2.2-brightgreen.svg)](https://www.djangoproject.com/download/)

![The_Forum](https://github.com/am-derrick/mydjangoapp/assets/65196859/8f5bfae3-be5f-4145-9dad-2d81c89e4181)

## Demo

Watch the demo [here.](https://youtu.be/KR2RB8S00Og)

App hosted on Digital Ocean using Nginx Server under domain name [theforumxyz.xyz](http://theforumxyz.xyz) 🚧

## Running the Project Locally

First, clone the repository to your local machine:

```bash
git clone git@github.com:am-derrick/mydjangoapp.git
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Setup the local configurations:

```bash
cp .env.example .env
```

Create the database:

```bash
python manage.py migrate
```

Finally, run the development server:

```bash
python manage.py runserver
```

The project will be available at **127.0.0.1:8000**.