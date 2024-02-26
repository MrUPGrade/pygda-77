export PYGDA_DB_DRIVER="postgresql+psycopg2"
export PYGDA_DB_USER="dbuser"
export PYGDA_DB_PASS="dbpass"
export PYGDA_DB_HOST="localhost"
export PYGDA_DB_PORT=22222
export PYGDA_DB_NAME="db"
export PYGDA_API_PORT=22221

env | grep PYGDA_ > .env.dev

# Python
export PYTHONPATH=$(pwd)