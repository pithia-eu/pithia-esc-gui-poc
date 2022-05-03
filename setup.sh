#!/bin/bash
python3 -m venv venv
echo "Created Python virtual environment"

source venv/bin/activate
echo "Activated Python virtual environment"

pip3 install -r requirements.txt
echo ""
echo "Finished installing packages from requirements.txt"