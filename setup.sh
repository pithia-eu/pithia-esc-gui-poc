#!/bin/sh

source venv/bin/activate
echo "Activated Python virtual environment"

pip3 install -r requirements.txt
echo ""
echo "Finished packages from requirements.txt"