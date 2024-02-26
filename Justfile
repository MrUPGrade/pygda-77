# Display help (this message)
default:
    @just --list

set dotenv-filename := ".env.dev"
set dotenv-load := true

user := `whoami`
# python
system_python := env("PYTHON_BIN", "python3")
venv := "venv"
pip := venv + "/bin/pip"
python := venv + "/bin/python3"
pytest := venv + "/bin/pytest"

export PYTHONPATH := justfile_directory()

# docker
dc_project := "pygda"
dc := "docker compose -p " + dc_project
docker := "docker"


#
# Python
#
# Create virtual env if not exists
[private]
venv:
    test -e venv || {{system_python}} -m venv venv

# Install applicaton dependencies
pip-install-base: venv
    {{pip}} install --upgrade pip
    {{pip}} install -r requirements.txt

# Install test dependencies
pip-install-test: venv
    {{pip}} install -r requirements-test.txt

# Install all dev packages
pip-install: pip-install-base pip-install-test

# Run tests
tests-run:
    {{pytest}} tests/unit



#
# Dev env
#
# Prepare and start whole environment
env-dev-setup:  pip-install run-env-script env-dev-up sleep db-reflect

# Start dev env
env-dev-up:
    {{dc}} up -d

# Stop dev env
env-dev-stop:
    {{dc}} stop

# Stop and destroy dev env
env-dev-down:
    {{dc}} down

# Perform full reset of dev environment
env-dev-reset: env-dev-down env-dev-setup


#
# db
#
# Create db schema
db-reflect:
    {{python}} api/cli.py db reflect

# Load fake data to db
db-fakedata-load:
    {{python}} api/cli.py db add-fake-data



#
# docker
#
# Build docker dev image with test tags
docker-build-dev:
    {{docker}} build -t mrupgrade/pygda:{{user}}-dev .

# Push docker dev image with test tags
docker-publish-dev:
    {{docker}} push mrupgrade/pygda:{{user}}-dev


#
# misc
#
# Run pycharm for this project 
pycharm-start:
	pycharm .

[private]
run-env-script:
    source env-dev.sh
    touch .env.override

[private]
sleep:
    sleep 5

