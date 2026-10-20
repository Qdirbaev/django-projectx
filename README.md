# Xgame

Simple Django catalog of games: categories, search, game pages with trailers,
comments, registration/login and torrent downloads for authenticated users.
Staff users can add games from the site.

## Run locally

```bash
pip install -r requirements.txt
cd projectx
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/. Add categories and games via `/admin/`.
