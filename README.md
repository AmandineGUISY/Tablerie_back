TABLERIE

# for different python versions

python -m venv venv
python3 -m venv venv

## activate environment
# Windows : 
.\venv\Scripts\activate

# Mac/Linux : 
source venv/bin/activate

pip install -r requirement.txt

docker compose up -d

fastapi dev main.py

# pour relancer la base de données et son volume
docker volume rm constellation_backend_postgres_data
docker compose up -d


