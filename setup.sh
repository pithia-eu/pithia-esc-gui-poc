!#/bin/sh

source venv/bin/activate
echo "Activated Python virtual environment"

pip3 install -r requirements.txt
echo "Installed packages from requirements.txt"

read -rsn1 -p "Done! Press any key to exit"
exit