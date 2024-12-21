# Nordic Capitals API

A comprehensive Django REST Framework (DRF) example project that demonstrates various DRF features. This project serves as both a learning resource and a reference implementation for DRF concepts.

## Project Structure

```
nordic_capitals/
├── capitals/                # Main app directory
│   ├── migrations/         # Database migrations
│   ├── templates/         # HTML templates
│   ├── models.py          # Data models
│   ├── serializers.py     # API serializers
│   ├── views.py           # ViewSet implementations
│   ├── urls.py            # API endpoints
│   ├── forms.py           # Forms for template views
│   ├── permissions.py     # Custom permissions
│   ├── paginators.py      # Custom pagination classes
│   ├── admin.py          # Admin panel configuration
│   └── tests.py          # Unit tests
├── nordic_capitals/       # Project settings directory
│   ├── settings.py       # Main settings file
│   ├── local_settings.py # Local environment settings
│   └── urls.py           # Main URL configuration
├── manage.py             # Django management script
├── requirements.txt      # Project dependencies
├── README.md            # Project documentation
└── start.sh             # Startup script
```

## Installation and Setup

### Linux

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nordic_capitals.git
cd nordic_capitals
```

2. Make the startup script executable:
```bash
chmod +x start.sh
```

3. Run the script:
```bash
./start.sh
```

The script will automatically:
- Create a virtual environment
- Install all dependencies
- Configure the project
- Apply migrations
- Create a superuser (on first run)
- Start the server

### Windows

#### Option 1: Using Git Bash
1. Install [Git for Windows](https://gitforwindows.org/)
2. Open Git Bash
3. Follow the Linux instructions

#### Option 2: Manual Setup
1. Clone the repository
2. Create a virtual environment:
```cmd
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```cmd
pip install -r requirements.txt
```

4. Copy settings file:
```cmd
copy nordic_capitals\local_settings.py.example nordic_capitals\local_settings.py
```

5. Generate secret key:
```cmd
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" > nordic_capitals\secret_key.txt
```

6. Apply migrations:
```cmd
python manage.py migrate
```

7. Create superuser:
```cmd
python manage.py createsuperuser
```

8. Start the server:
```cmd
python manage.py runserver
```
