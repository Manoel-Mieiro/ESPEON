py -m ensurepip --upgrade
py -3 -m venv .venv
.venv/Scripts/activate
pip install Flask
python -m pip install pymongo
pip install psycopg2-binary

# optional
pip install python-dotenv

# reportLab
pip install reportlab

# on ubuntu
#python3 -m pip install --user Flask
#python3 -m pip install --user python-dotenv
#python3 -m pip install --user pymongo
