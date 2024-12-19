## Installation

### Prerequisites
- Python 3.x installed on your machine.
- Virtualenv for managing Python environments.

### Steps:


```bash

# Clone the repository
git clone git@github.com:Mabenchi/Django-Vulnerable-App.git

# Navigate into the project directory
cd Django-Vulnerable-App

# Create Vitual Environment
Linux: python -m venv challenge
Windows: py -m venv challenge

#install Django
Linux: python -m pip install Django
Windows: py -m pip install Django

# Activate the virtual environment
Linux: source challenge/bin/activate
Windows: challenge\Scripts\activate.bat

# Apply migrations
python3 manage.py migrate
py manage.py migrate

# Run the development server
python3 manage.py runserver
py manage.py runserver
```

