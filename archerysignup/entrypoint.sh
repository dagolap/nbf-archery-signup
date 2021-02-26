if [[ -z "$DJANGO_SUPERUSER_USERNAME" ]]; then
  echo "DJANGO_SUPERUSER_USERNAME must be set" 1>&2
  exit 1
fi

if [[ -z "$DJANGO_SUPERUSER_EMAIL" ]]; then
  echo "DJANGO_SUPERUSER_EMAIL must be set" 1>&2
  exit 1
fi

if [[ -z "$DJANGO_SUPERUSER_PASSWORD" ]]; then
  echo "DJANGO_SUPERUSER_PASSWORD must be set" 1>&2
  exit 1
fi

poetry run python manage.py migrate
poetry run python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME  --email $DJANGO_SUPERUSER_EMAIL
poetry run python manage.py collectstatic --noinput


poetry run gunicorn archerysignup.wsgi:application --bind 0.0.0.0:8000
