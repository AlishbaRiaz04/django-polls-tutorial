# Django Polls Tutorial

A polling web application built while learning Django 6.1. The project follows the official Django tutorial and includes questions, choices, voting, results, automated tests, admin customization, static files, and Django Debug Toolbar.

## Features

- Display the latest published poll questions
- View question details and available choices
- Vote on a choice and view the results
- Manage questions and choices through Django Admin
- Run automated tests for models and views
- Inspect requests and database queries with Django Debug Toolbar

## Requirements

The project was developed and tested with:

- Python 3.14.2
- Django 6.1.2
- django-debug-toolbar 8.0.0
- pip

Install the project dependencies from `requirements.txt` using the setup instructions below.

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd django-polls-tutorial
```

Replace `<repository-url>` with this repository's HTTPS URL.

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Secret key configuration

For local development, the project uses a fallback secret key if `DJANGO_SECRET_KEY` is not set. You can optionally provide your own development key through an environment variable.
**Windows PowerShell:**
```powershell
$env:DJANGO_SECRET_KEY = "your-local-development-key"
```

**macOS/Linux:**
```bash
export DJANGO_SECRET_KEY="your-local-development-key"
```

**Production:** Always configure a secure, private `DJANGO_SECRET_KEY` through your deployment environment. Never use the development fallback in production.
### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Create an administrator account (optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to create the account.

### 7. Start the development server

```bash
python manage.py runserver
```
Open the following URLs in your browser:

- Polls: http://127.0.0.1:8000/polls/
- Django Admin: http://127.0.0.1:8000/admin/

The Django development server is intended for local development, not production hosting.

## Run tests

```bash
python manage.py test polls
```

## Project structure

```text
django-polls-tutorial/
├── manage.py
├── requirements.txt
├── mysite/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── polls/
    ├── migrations/
    │   └── 0004_alter_question_pub_date.py
    ├── static/
    │   └── polls/
    │       ├── style.css
    │       └── images/
    │           └── background.jpg
    ├── templates/
    │   └── polls/
    │       ├── base.html
    │       ├── index.html
    │       ├── detail.html
    │       └── results.html
    ├── admin.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py
```

## Notes

- The project uses SQLite for local development.
- The database file is generated locally by running migrations and is not committed to the repository.
- Django Debug Toolbar is included for development and debugging.

## Learning reference

This project is based on the official Django documentation and tutorial:

https://docs.djangoproject.com/en/6.1/