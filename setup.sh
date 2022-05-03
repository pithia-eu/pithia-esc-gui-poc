#!/bin/bash
python3 -m venv venv
printf "\nCreated Python virtual environment"

source venv/bin/activate
printf "\nActivated Python virtual environment"

pip3 install -r requirements.txt
printf "\nFinished installing packages from requirements.txt"

# Setup default .env file
envfile=".env"
secret_key=$(python3 -c "import secrets; print(secrets.token_urlsafe())")
echo "SECRET_KEY=$secret_key"
echo "MONGODB_CONNECTION_STRING=mongodb://localhost:27017"
echo "DB_NAME=pithia-esc"
cat $envfile