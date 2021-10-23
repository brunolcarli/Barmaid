<table align="center"><tr><td align="center" width="9999">
<img src="https://i.ibb.co/X2tyQ1f/Captura-de-Tela-2021-10-18-a-s-23-30-20.png" align="center" width="200" alt="Project icon">


# Barmaid

> [![Version badge](https://img.shields.io/badge/version-0.0.1-silver.svg)](https://lisa--brunolcarli.repl.co/graphql/?query=query%7B%0A%09lisa%0A%7D)


</td></tr>

</table>

This is a for fun bot whic serves as fictional pub waitress. Users earn fictional coins as they send messages on discord chat. They may use the coins for "buying" illustrative items such as beer or whatever its registered on the database. The database is initially populated from a json file on `barmaid/items.json`. The items must have a thumbnail picture on `static/img`.

All items and coins re **fictionall** and merelly **illustrative**. No real product will or can be acquired from this bot. This is a non profit project and no trademark has been claimed. We take no endorsements from any company or trademark displayed.

## Configure and executing

## Local

Install dependencies on a python virtual env:

```
$ export ENV_REF=development
$ make install
```

Create a file on the directory root named `.env`, add and edit the following content wth your custom values for the variables:

`.env`

```
export ENV_REF=development
export TOKEN=<your_bot_token>
export MAIN_CHANNEL=<your_server_main_channel>
export MYSQL_HOST=<mysql_host>
export MYSQL_USER=barmaid
export MYSQL_PASSWORD=<your_mysl_user_password>
export MYSQL_DATABASE=barmaid
```

Make sure you have a MYSQL user named barmaid with the right access privileges.

Run the database initialization command to create schema, tables and populatewith the items on `barmaid/items.json`

```
$ make migrate
```

Run bot with:

```
$ make run
```


## Run with docker

Install python docker-compose from pip:

```
$ pip install docker-compose
```

Create a file named `barmaid_env` on `barmaid/environment/barmaid_env` from the template on `barmaid/environment/template` and add your variable values.

Build and run the docker container:

```
$ docker-compose build
$ docker-compose up -d
```

Get the container id with

```
$ docker ps -a | grep barmaid
```

run initial database migrations:

```
$ docker exec -ti <container_hash_id> make migrate
```