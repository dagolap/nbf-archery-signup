NBF Signup Application
======================

Enkel app skrevet i Django for å ta i mot signups til stevner.

Påmeldinger eksporteres så til ianseo via. CSV.

Applikasjonen kan ta i mot resultatbevis i form av bilder av scorekort og skive.

Deps
-----

- Python
- Poetry


Installation
-------------

### Sett opp env-variabler:

```toml
DATABASE_URL=sqlite:///db.sqlite3
SECRET_KEY=<random string>
MEDIA_ROOT=Sti der media-filer skal lastes opp til og serves fra
STATIC_ROOT=Sti der webserver serverer statiske filer fra
```

### First time run
```shell
poetry run python manage.py migrate
poerty run python manage.py createsuperuser
# <fyll inn svar på spørsmål>
poetry run python manage.py collectstatic
```

Starte server? Vet ikke.. Må sjekke. Unicorn-specs osv.