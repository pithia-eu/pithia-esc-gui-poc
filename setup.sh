#!/bin/bash
python3 -m venv venv
printf "\nCreated Python virtual environment\n"

source venv/bin/activate
printf "\nActivated Python virtual environment\n"

pip3 install -r requirements.txt
printf "\nFinished installing packages from requirements.txt\n"

# Setup default .env file
printf "\nSetting up default .env\n"
envfile="./pithiaesc/.env"
secret_key=$(python3 -c "import secrets; print(secrets.token_urlsafe())")
echo "SECRET_KEY=$secret_key" > $envfile
echo "MONGODB_CONNECTION_STRING=mongodb://localhost:27017" >> $envfile
echo "DB_NAME=pithia-esc" >> $envfile
cat $envfile
printf "\nFinished setting up default .env\n"