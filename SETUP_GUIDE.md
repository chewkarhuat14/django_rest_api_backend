# Django REST API Setup Guide - Step by Step Commands

This guide documents all the commands and steps used to create this Django REST API template with PostgreSQL and JWT authentication.

## Table of Contents
1. [Initial Setup](#initial-setup)
2. [Project Structure Creation](#project-structure-creation)
3. [Installing Dependencies](#installing-dependencies)
4. [Database Setup](#database-setup)
5. [Running the Project](#running-the-project)
6. [Testing the API](#testing-the-api)

---

## Initial Setup

### 1. Create Project Directory
```bash
mkdir django-rest-api
cd django-rest-api
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv

# Linux/Mac
python3 -m venv venv
```

### 3. Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 4. Upgrade pip
```bash
python -m pip install --upgrade pip
```

---

## Project Structure Creation

### 5. Create Directory Structure
```bash
# Create main backend directories
mkdir -p backend/config
mkdir -p backend/apps/users

# Create __init__.py files to make directories Python packages
touch backend/config/__init__.py
touch backend/apps/__init__.py
touch backend/apps/users/__init__.py
```

**Windows alternative (if `touch` doesn't work):**
```bash
type nul > backend/config/__init__.py
type nul > backend/apps/__init__.py
type nul > backend/apps/users/__init__.py
```

### 6. Create requirements.txt
Create a file named `requirements.txt` in the project root with these dependencies:

```txt
# Django Framework
Django==4.2.7
djangorestframework==3.14.0

# PostgreSQL Database
psycopg2-binary==2.9.9

# Authentication & JWT
djangorestframework-simplejwt==5.3.0

# CORS Headers
django-cors-headers==4.3.0

# Environment Variables
python-decouple==3.8

# Password Validation
django-password-validators==1.7.1
```

---

## Installing Dependencies

### 7. Install All Dependencies
```bash
pip install -r requirements.txt
```

### 8. Verify Installation
```bash
pip list
```

You should see all the packages installed including:
- Django
- djangorestframework
- psycopg2-binary
- djangorestframework-simplejwt
- django-cors-headers
- python-decouple

---

## Database Setup

### 9. Install PostgreSQL
Download and install PostgreSQL from: https://www.postgresql.org/download/

### 10. Create PostgreSQL Database
Open PostgreSQL terminal (psql) or pgAdmin and run:

```sql
-- Create database
CREATE DATABASE django_rest_db;

-- Create user (if not exists)
CREATE USER DTI_Admin WITH PASSWORD 'secret@123';

-- Set encoding and privileges
ALTER ROLE DTI_Admin SET client_encoding TO 'utf8';
ALTER ROLE DTI_Admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE DTI_Admin SET timezone TO 'UTC';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE django_rest_db TO DTI_Admin;
```

**Alternative using command line:**
```bash
# Windows (open cmd as admin or use psql)
psql -U postgres

# Then run the SQL commands above
```

### 11. Create Environment Configuration
Create `.env` file in project root:

```bash
# Copy from example
cp .env.example .env

# Or on Windows
copy .env.example .env
```

Edit `.env` with your actual values:
```env
SECRET_KEY=your-secret-key-here-generate-a-secure-one
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=django_rest_db
DB_USER=DTI_Admin
DB_PASSWORD=secret@123
DB_HOST=localhost
DB_PORT=5432

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## Running the Project

### 12. Navigate to Backend Directory
```bash
cd backend
```

### 13. Create Migrations for Users App
```bash
python manage.py makemigrations users
```

Expected output:
```
Migrations for 'users':
  apps\users\migrations\0001_initial.py
    - Create model User
```

### 14. Run All Migrations
```bash
python manage.py migrate
```

Expected output will show migrations being applied for:
- contenttypes
- auth
- admin
- sessions
- users

### 15. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```

You'll be prompted:
```
Email: admin@example.com
First name: Admin
Last name: User
Password: ********
Password (again): ********
```

### 16. Run Development Server
```bash
python manage.py runserver
```

Expected output:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
January 01, 2025 - 12:00:00
Django version 4.2.7, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## Testing the API

### 17. Access Django Admin
Open browser: `http://127.0.0.1:8000/admin/`

Login with superuser credentials created in step 15.

### 18. Test API Endpoints Using cURL

#### Register a New User
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"first_name\":\"John\",\"last_name\":\"Doe\",\"phone_number\":\"+1234567890\",\"password\":\"SecurePass123!\",\"password2\":\"SecurePass123!\"}"
```

**Windows PowerShell:**
```powershell
$body = @{
    email = "test@example.com"
    first_name = "John"
    last_name = "Doe"
    phone_number = "+1234567890"
    password = "SecurePass123!"
    password2 = "SecurePass123!"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/register/" -Method POST -Body $body -ContentType "application/json"
```

#### Login User
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"SecurePass123!\"}"
```

**Windows PowerShell:**
```powershell
$body = @{
    email = "test@example.com"
    password = "SecurePass123!"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/login/" -Method POST -Body $body -ContentType "application/json"
$response
```

#### Get User Profile (Authenticated)
```bash
# Save access token from login response
ACCESS_TOKEN="your_access_token_here"

curl -X GET http://127.0.0.1:8000/api/auth/profile/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Windows PowerShell:**
```powershell
$accessToken = "your_access_token_here"
$headers = @{
    "Authorization" = "Bearer $accessToken"
}

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/profile/" -Method GET -Headers $headers
```

### 19. Test Using Postman or Thunder Client

1. **Install Postman** or **Thunder Client** (VS Code extension)
2. Create a new collection: "Django REST API"
3. Add requests for each endpoint (see README.md for all endpoints)
4. Test each endpoint with sample data

---

## Running Tests

### 20. Run Unit Tests
```bash
cd backend
python manage.py test apps.users
```

Expected output:
```
Creating test database...
......
----------------------------------------------------------------------
Ran 6 tests in 0.XXXs

OK
Destroying test database...
```

### 21. Run Tests with Verbose Output
```bash
python manage.py test apps.users --verbosity=2
```

### 22. Run Specific Test Class
```bash
python manage.py test apps.users.tests.UserModelTests
```

---

## Additional Useful Commands

### Check for Issues
```bash
python manage.py check
```

### Create New Migration
```bash
python manage.py makemigrations
```

### Show Migration Status
```bash
python manage.py showmigrations
```

### Open Django Shell
```bash
python manage.py shell
```

Inside shell, you can interact with models:
```python
from apps.users.models import User

# Get all users
users = User.objects.all()

# Create a user
user = User.objects.create_user(
    email='shell@example.com',
    password='TestPass123!',
    first_name='Shell',
    last_name='User'
)

# Query users
user = User.objects.get(email='shell@example.com')
print(user.get_full_name())
```

### Collect Static Files (for production)
```bash
python manage.py collectstatic
```

### Create Database Backup (PostgreSQL)
```bash
# Backup
pg_dump -U DTI_Admin django_rest_db > backup.sql

# Restore
psql -U DTI_Admin django_rest_db < backup.sql
```

---

## File Creation Summary

Here's what files were created and their purposes:

### Configuration Files
1. **requirements.txt** - Python dependencies
2. **.env.example** - Environment variables template
3. **.env** - Actual environment variables (not in git)
4. **.gitignore** - Git ignore rules

### Backend Core Files
5. **backend/manage.py** - Django management script
6. **backend/config/settings.py** - Django settings (database, apps, middleware, JWT, CORS)
7. **backend/config/urls.py** - Main URL routing
8. **backend/config/wsgi.py** - WSGI server config
9. **backend/config/asgi.py** - ASGI server config

### Users App Files
10. **backend/apps/users/models.py** - Custom User model
11. **backend/apps/users/serializers.py** - API serializers
12. **backend/apps/users/views.py** - API views/endpoints
13. **backend/apps/users/urls.py** - App URL routing
14. **backend/apps/users/admin.py** - Django admin config
15. **backend/apps/users/apps.py** - App configuration
16. **backend/apps/users/tests.py** - Unit tests

### Documentation
17. **README.md** - Project documentation
18. **SETUP_GUIDE.md** - This file (setup commands)

---

## Quick Start Script

Save this as `setup.sh` (Linux/Mac) or `setup.bat` (Windows) for future projects:

### Linux/Mac (setup.sh)
```bash
#!/bin/bash

# Create project structure
mkdir -p django-rest-api/backend/{config,apps/users}
cd django-rest-api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Create __init__.py files
touch backend/config/__init__.py
touch backend/apps/__init__.py
touch backend/apps/users/__init__.py

# Create requirements.txt (you'll need to add content)
touch requirements.txt

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env from example
cp .env.example .env

echo "Setup complete! Now:"
echo "1. Edit .env with your database credentials"
echo "2. Create PostgreSQL database"
echo "3. cd backend && python manage.py migrate"
echo "4. python manage.py createsuperuser"
echo "5. python manage.py runserver"
```

### Windows (setup.bat)
```batch
@echo off

REM Create project structure
mkdir django-rest-api\backend\config
mkdir django-rest-api\backend\apps\users
cd django-rest-api

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

REM Create __init__.py files
type nul > backend\config\__init__.py
type nul > backend\apps\__init__.py
type nul > backend\apps\users\__init__.py

REM Create requirements.txt
type nul > requirements.txt

REM Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env from example
copy .env.example .env

echo Setup complete! Now:
echo 1. Edit .env with your database credentials
echo 2. Create PostgreSQL database
echo 3. cd backend ^&^& python manage.py migrate
echo 4. python manage.py createsuperuser
echo 5. python manage.py runserver
```

---

## Troubleshooting Common Issues

### Issue: psycopg2 installation fails
**Solution:**
```bash
# Use binary version
pip install psycopg2-binary==2.9.9
```

### Issue: Port 8000 already in use
**Solution:**
```bash
# Run on different port
python manage.py runserver 8080
```

### Issue: Database connection refused
**Solution:**
1. Check PostgreSQL is running
2. Verify credentials in .env
3. Test connection:
```bash
psql -U DTI_Admin -d django_rest_db -h localhost
```

### Issue: Module not found errors
**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: Migration conflicts
**Solution:**
```bash
# Reset migrations (development only!)
python manage.py migrate --run-syncdb
```

---

## Next Steps for Learning

1. **Add More Apps**: Create new apps like `products`, `orders`, etc.
   ```bash
   python manage.py startapp products backend/apps/products
   ```

2. **Add More Endpoints**: Extend the API with:
   - Password reset via email
   - Email verification
   - Social authentication
   - File uploads

3. **Add Permissions**: Custom permissions for different user roles

4. **Add Pagination**: Implement pagination for list endpoints

5. **Add Filtering**: Use django-filter for advanced filtering

6. **Add Documentation**: Install drf-spectacular for auto API docs
   ```bash
   pip install drf-spectacular
   ```

7. **Deploy**: Learn to deploy on platforms like:
   - Heroku
   - AWS EC2
   - DigitalOcean
   - Railway

---

## Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **SimpleJWT**: https://django-rest-framework-simplejwt.readthedocs.io/
- **PostgreSQL**: https://www.postgresql.org/docs/
- **Python Decouple**: https://github.com/henriquebastos/python-decouple

---

## Summary Checklist

Use this checklist for future setups:

- [ ] Create project directory
- [ ] Create virtual environment
- [ ] Activate virtual environment
- [ ] Create directory structure (backend, config, apps)
- [ ] Create requirements.txt with dependencies
- [ ] Install dependencies with pip
- [ ] Create Django project files (settings, urls, wsgi, asgi, manage.py)
- [ ] Install and configure PostgreSQL
- [ ] Create database and user
- [ ] Create .env file with credentials
- [ ] Create User app (models, serializers, views, urls, admin)
- [ ] Create migrations
- [ ] Run migrations
- [ ] Create superuser
- [ ] Test endpoints
- [ ] Write documentation

**Congratulations!** You now have a complete reference for setting up Django REST API projects with PostgreSQL and JWT authentication.
