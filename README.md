NBF Signup Application
======================

Enkel app skrevet i Django for å ta i mot signups til stevner.

Påmeldinger eksporteres så til ianseo via. CSV.

Applikasjonen kan ta i mot resultatbevis i form av bilder av scorekort og skive.

Deps
-----
- Python
- Poetry


Utvikling
---------
poetry install
cd archerysignup
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py runserver


Prod deployment
---------------
Bygg docker-image.
docker build .
cd server
docker-compose up

For et produksjonsmiljø kreves det at man setter en del environment-variabler.

Se i compose-filen for hvilke dette er.
