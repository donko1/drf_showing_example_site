# Nordic Capitals API

A comprehensive Django REST Framework (DRF) example project that demonstrates various DRF features and my practices. This project serves as both a learning resource and a reference implementation for DRF concepts.

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

## Project Structure

```
nordic_capitals/
├── capitals/              # Main app directory
│   ├── models.py         # Data models
│   ├── serializers.py    # Various serializer examples
│   ├── views.py         # ViewSet implementations
│   ├── permissions.py   # Custom permissions
│   └── urls.py          # API endpoints
├── manage.py
└── requirements.txt
```

## Installation

### Linux

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nordic_capitals.git
cd nordic_capitals
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create local settings:
```bash
cp nordic_capitals/local_settings.py.example nordic_capitals/local_settings.py
```

5. Generate a new secret key and update local_settings.py:
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copy the generated key and replace 'your-secret-key-here' in local_settings.py with it.

6. Apply migrations:
```bash
python3 manage.py migrate
```

7. Create superuser (optional):
```bash
python3 manage.py createsuperuser
```

8. Run the development server:
```bash
python3 manage.py runserver
```

### Windows

1. Clone the repository:
```cmd
git clone https://github.com/yourusername/nordic_capitals.git
cd nordic_capitals
```

2. Create and activate virtual environment:
```cmd
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```cmd
pip install -r requirements.txt
```

4. Create local settings:
```cmd
copy nordic_capitals\local_settings.py.example nordic_capitals\local_settings.py
```

5. Generate a new secret key and update local_settings.py:
```cmd
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copy the generated key and replace 'your-secret-key-here' in local_settings.py with it.

6. Apply migrations:
```cmd
python manage.py migrate
```

7. Create superuser (optional):
```cmd
python manage.py createsuperuser
```

8. Run the development server:
```cmd
python manage.py runserver
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
