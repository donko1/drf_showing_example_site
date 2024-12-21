#!/bin/bash

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

if [ ! -f "nordic_capitals/secret_key.txt" ]; then
    echo "Performing full installation..."
    
    pip install -r requirements.txt
    
    cp nordic_capitals/local_settings.py.example nordic_capitals/local_settings.py
    
    python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" > nordic_capitals/secret_key.txt
    
    python3 manage.py migrate
    
    python3 manage.py createsuperuser
    
    echo "Installation complete!"
fi

# Запускаем сервер
echo "Starting server..."
python3 manage.py runserver