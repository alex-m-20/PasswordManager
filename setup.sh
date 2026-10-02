#!/bin/bash
# This script file sets everything needed to run the password manager

set -e  # stop the script on error

# Create the virtual environment
python -m venv venv

# Windows paths for the venv's pip and python
PIP="venv/Scripts/pip"
PYTHON="venv/Scripts/python"

# Install the project's dependencies
"$PIP" install Flask Flask-SQLAlchemy Flask-WTF Flask-Login cryptography python-dotenv

# Generate .env only if it doesn't already exist
if [ ! -f ".env" ]; then
    SECRET_KEY=$("$PYTHON" -c "import secrets; print(secrets.token_hex(16))")
    ENCRYPTION_KEY=$("$PYTHON" -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
    echo "SECRET_KEY=$SECRET_KEY" > .env
    echo "ENCRYPTION_KEY=$ENCRYPTION_KEY" >> .env
else
    :
fi

# Create the database tables
"$PYTHON" database_setup.py