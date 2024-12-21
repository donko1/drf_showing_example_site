# Nordic Capitals API

A comprehensive Django REST Framework (DRF) example project that demonstrates various DRF features. This project serves as both a learning resource and a reference implementation for DRF concepts.

## Prerequisites

### Linux (Ubuntu/Debian)

1. Install Python:
```bash
# Update package list
sudo apt update

# Install Python
sudo apt install python3
sudo apt install python3-pip

# Verify installation
python3 --version
pip3 --version
```

2. Install Git:
```bash
sudo apt install git
git --version
```

### Windows

1. Install Python:
   - Go to [Python Downloads](https://www.python.org/downloads/)
   - Download the latest Python installer (e.g., Python 3.11)
   - Run the installer
   - Check "Add Python to PATH" during installation
   - Click "Install Now"
   - Verify installation by opening Command Prompt:
   ```cmd
   python --version
   pip --version
   ```

2. Install Git:
   - Go to [Git Downloads](https://git-scm.com/downloads)
   - Download Git for Windows
   - Run the installer with default settings
   - Verify installation:
   ```cmd
   git --version
   ```

### macOS

1. Install Homebrew (if not installed):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install Python and Git:
```bash
brew install python git

# Verify installation
python3 --version
pip3 --version
git --version
```

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

### Linux and macOS

1. Clone the repository:
```bash
git clone https://github.com/donko1/drf_showing_example_site.git
cd drf_showing_example_site
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

### Restarting the Server

To restart the server after the initial setup u have 2 options:
#### Option 1: Manual restart
1. Activate the virtual environment:
```bash
source venv/bin/activate  
```
2. Start the server:
```bash
python manage.py runserver
```
#### Option 2: start.sh restart
1. Start start.sh
```bash
./start.sh
```

### Windows

#### Option 1: Using Git Bash
1. Clone the repository:
```bash
git clone https://github.com/donko1/drf_showing_example_site.git
cd drf_showing_example_site
```

2. Follow the Linux instructions using Git Bash

#### Option 2: Manual Setup
1. Clone the repository:
```cmd
git clone https://github.com/donko1/drf_showing_example_site.git
cd drf_showing_example_site
```

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
python -c "from django.core.management.utils import get_random_secret_key; key=get_random_secret_key(); print(key);"
```
$${\color{red}Important!}$$ Add key to nordic_capitals/secret_key.txt file

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

### Restarting the Server (Windows)

To restart the server after the initial setup:
1. Activate the virtual environment:
```cmd
venv\Scripts\activate
```
2. Start the server:
```cmd
python manage.py runserver
