# Django-Vulnerable-App

A deliberately vulnerable Django application built for educational and Capture The Flag (CTF) purposes. This project demonstrates common web vulnerabilities, including SQL Injection, Cross-Site Scripting (XSS), Server-Side Template Injection (SSTI), and more.

## Features
- User registration and authentication system.
- SQL Injection vulnerability.
- Cross-Site Scripting (XSS) vulnerability.
- Server-Side Template Injection (SSTI) vulnerability.
- User profile and amount transfer functionality.

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

# Activate the virtual environment
source challenge/bin/activate

# Apply migrations
python3 manage.py migrate

# Run the development server
python3 manage.py runserver
```

## Usage
1. Visit `http://127.0.0.1:8000/` to access the application.
2. Explore the application and test various features.
3. Identify and exploit vulnerabilities for educational purposes.

