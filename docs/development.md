# Development Setup Guide

## Prerequisites
- Python 3.10 or later
- PostgreSQL - download packages/installers from the [PostgreSQL Downloads](https://www.postgresql.org/download/) page. The [PgAdmin 4 client](https://www.pgadmin.org/download/) is an easy way to interact with the PostgreSQL database if you are not comfortable with using the CLI.

## Change to the project directory
Download the code and `cd` into the project's root folder from the command line.

## Install Python dependencies
```
pip3 install -r requirements.txt --no-deps
```

## Create the .env file
```
cd pithiaesc
sudo touch .env
```

## Set up the .env file variables
The project uses environment variables which are stored in a `.env` file in the `/pithiaesc` folder. Enter the variables using whatever method works for you. Below is an example of a filled out .env file which you can follow:
```
SECRET_KEY=escdevsecretkey

DATABASE_NAME=esc-dev
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432

DATABASE_READ_USER=escuser-r
DATABASE_WRITE_USER=escuser-rw
DATABASE_READ_PASSWORD=password123
DATABASE_WRITE_PASSWORD=password123
```
**Note:** This guide does not provide instructions for setting up the Handle generation features for development, so the environment variables for those features have been excluded here.

## Setup the PostgreSQL database
Create the development database and database users with the same information you entered in the .env file. Next, create all the database tables by running the following in the command line:
```
python3 manage.py migrate
```

## Verify the project runs
To test the project runs enter the following in the command line:
```
python3 manage.py runserver
```
The command line should display output similar to this:
```
System check identified no issues (0 silenced).
January 18, 2024 - 17:18:37
Django version 4.0.5, using settings 'pithiaesc.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
All the e-Science Centre's features should be now be available, with the exception of the Handle features. To view the project in your browser, enter [http://localhost:8000](http://localhost:8000) in your address bar!


