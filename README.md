# hy-restaurant-app

Sovelluksen avulla voi löytää ravintoloita kartalta, etsiä niistä tietoa, arvostella niitä ja lukea muiden arvosteluita. 

Sovelluksen ominaisuuksia ovat:

- [x] Käyttäjä voi kirjautua sisään tai luoda uuden tunnuksen. Jokainen käyttäjä on joko peruskäyttäjä tai ylläpitäjä.
- [x] Käyttäjä näkee ravintolat kartalla. Ravintolaa klikatessa näytetään siihen liittyvää informaatiota (kuvaus, aukioloajat, jne.)
- [x] Käyttäjä voi antaa ravintolalle arvion (tähdet 1-5 ja vapaamuotoinen kommentti)
- [x] Käyttäjä voi lukea muiden kirjoittamia arvioita
- [x] Ylläpitäjä voi lisätä ja poistaa ravintoloita, sekä määritellä ravintolasta näytettävät tiedot
- [x] Käyttäjä voi hakea ravintoloita avainsanojen perusteella, joita etsitään ravintoloiden nimistä ja kuvauksista.
- [x] Käyttäjä näkee ravintolat listassa, jossa ravintolat voidaan järjestää ainakin arvostelujen perusteella.
- [x] Ylläpitäjä pystyy poistamaan käyttäjän arvion ravintolalta
- [ ] Ylläpitäjä voi luoda ryhmiä, joihin ravintolat voidaan luokitella. Ravintola voi kuulua yhteen tai useampaan ryhmään.

## Usage

To run, set up a PostgreSQL database with the University of Helsinki's [installation script](https://github.com/hy-tsoha/local-pg).

Once you have PostgreSQL up and running, open the Postgres front-end by running `psql` and run the SQL queries in *schema.sql*.

You can also do that by creating the database with:

```
$ psql
user=# CREATE DATABASE <database-name>;
```

and then running the following command on the command line:

```
psql -d <database-name> < schema.sql
```

After PostgreSQL has been set up, you can run the application with the following command:

```
DB_SECRET=<secret> flask --app app/app.py run
```

Generate yourself a secret using e.g. the Python terminal:

```
$ python3
>>> import secrets
>>> secrets.token_hex(16)
```