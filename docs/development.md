# Development Setup Guide

## Prerequisites
- Python 3.10
- npm package manager
- Dart Sass
- PostgreSQL

## Quickstart
```bash
git clone https://github.com/pithia-eu/pithia-esc-gui-poc.git pithiaesc
cd pithiaesc
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate # or source ./venv.sh
# Install project requirements
pip install -r requirements.txt
# Install Bootstrap files
npm install
# Set up environment variables
cp .env_example pithiaesc/.env
```

## PostgreSQL database setup
- Create a development database and users with the details specified in the `.env` file (e.g., using pgAdmin).
- Next, generate the database structure by running the following command:
```bash
python3 manage.py migrate
```

## Run the project locally
To run the project, enter the following:
```bash
python3 manage.py runserver # or ./run.sh
```
which should print out something similar to below:
```bash
System check identified no issues (0 silenced).
October 15, 2026 - 11:50:53
Django version 5.2.18, using settings 'pithiaesc.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
The project should be running at [http://localhost:8000](http://localhost:8000) (with the exception of Handle features, and currently, user authentication).


