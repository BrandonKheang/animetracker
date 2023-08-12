# Anime Tracker

## A website which allows users to track the anime they've watched. 

Website available at: http://animetracker.online/

This website was built in Python using Django. It's hosted on AWS using Gunicorn and Nginx. The website is kept live 24/7 using Supervisor. Users may access the following features:

- Browse anime by genre stored in an SQL database
- Functional search bar and pagination
- Create an account to add or remove anime from their personal list
- Browse other users' lists 
- Upvote or downvote anime which updates overall rating of that anime
- Send messages to other users
- Logged in users may leave reviewes on animes and delete reviews they have left
- Logged in users may reset their password through email

## Getting Started

### Prerequisites

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

### Installation

1. Clone the repository
```
git clone https://github.com/BrandonKheang/animetracker.git
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
