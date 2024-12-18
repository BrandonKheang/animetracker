# Anime Tracker

## A website which allows users to track the anime they've watched. Website available at: http://animetracker.online/ (Not currently active)

This website was built in Python using Django. It's hosted on AWS using Gunicorn and Nginx. The website is kept live 24/7 using Supervisor. Users may access the following features:

- Browse anime stored in an SQL database by genre
- Functional search bar and pagination
- Create an account to add or remove anime from their personal list
- Browse other users' lists 
- Upvote or downvote anime which updates overall rating of that anime
- Send messages to other users
- Logged in users may leave reviewes on animes and delete reviews they have left
- Logged in users may reset their password through email

## Getting Started

### Prerequisites

-Python
```
https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe
```
-pip
```
python get-pip.py
```
-Django
```
pip install django
```
-Pillow
```
pip install pillow
```
-whitenoise
```
pip install whitenoise
```

### Running Locally

1. Clone the repository
```
git clone https://github.com/BrandonKheang/animetracker
```
2. Go to cloned repository directory
3. Create database migrations
```
python3 manage.py makemigrations
```
4. Apply the migrations
```
python3 manage.py migrate
```
5. Create an admin user and provide a username and password
```
python3 manage.py createsuperuser
```
6. Start up the server
```
python3 manage.py runserver
```
