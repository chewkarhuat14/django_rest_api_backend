# Django REST API with Authentication

A professional Django REST API with JWT authentication, user registration, login, and profile management using PostgreSQL.

## Project Structure

```
django-rest-api/
├── backend/
│   ├── apps/
│   │   ├── __init__.py
│   │   └── users/
│   │       ├── __init__.py
│   │       ├── admin.py          # Django admin configuration
│   │       ├── apps.py           # App configuration
│   │       ├── models.py         # Custom User model
│   │       ├── serializers.py    # DRF serializers
│   │       ├── views.py          # API views
│   │       └── urls.py           # URL routing
│   ├── config/
│   │   ├── __init__.py
│   │   ├── asgi.py              # ASGI configuration
│   │   ├── settings.py          # Django settings
│   │   ├── urls.py              # Main URL configuration
│   │   └── wsgi.py              # WSGI configuration
│   └── manage.py                # Django management script
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Features

- Custom User model with email as username
- JWT token-based authentication
- User registration with validation
- User login and logout
- User profile retrieval and update
- Password change functionality
- PostgreSQL database
- CORS support
- Django REST Framework
- Token refresh mechanism

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)
- virtualenv (recommended)

## Installation & Setup

### 1. Clone or Navigate to the Project

```bash
cd django-rest-api
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL Database

Create a PostgreSQL database:

```sql
CREATE DATABASE django_rest_db;
CREATE USER postgres WITH PASSWORD 'your_password';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE django_rest_db TO postgres;
```

### 5. Configure Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env` file:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=django_rest_db
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 6. Run Migrations

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 8. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Login user | No |
| POST | `/api/auth/logout/` | Logout user | Yes |
| POST | `/api/auth/token/refresh/` | Refresh access token | No |

### Profile Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/auth/profile/` | Get user profile | Yes |
| PUT/PATCH | `/api/auth/profile/update/` | Update user profile | Yes |
| POST | `/api/auth/change-password/` | Change password | Yes |

## API Usage Examples

### 1. Register User

```bash
POST /api/auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890",
  "password": "SecurePass123!",
  "password2": "SecurePass123!"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "phone_number": "+1234567890",
    "date_joined": "2025-01-01T12:00:00Z",
    "last_login": null
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "message": "User registered successfully."
}
```

### 2. Login User

```bash
POST /api/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "phone_number": "+1234567890",
    "date_joined": "2025-01-01T12:00:00Z",
    "last_login": "2025-01-01T13:00:00Z"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "message": "Login successful."
}
```

### 3. Get User Profile

```bash
GET /api/auth/profile/
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "full_name": "John Doe",
  "phone_number": "+1234567890",
  "date_joined": "2025-01-01T12:00:00Z",
  "last_login": "2025-01-01T13:00:00Z"
}
```

### 4. Update User Profile

```bash
PATCH /api/auth/profile/update/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "Jane",
  "phone_number": "+9876543210"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "Jane",
    "last_name": "Doe",
    "full_name": "Jane Doe",
    "phone_number": "+9876543210",
    "date_joined": "2025-01-01T12:00:00Z",
    "last_login": "2025-01-01T13:00:00Z"
  },
  "message": "Profile updated successfully."
}
```

### 5. Change Password

```bash
POST /api/auth/change-password/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "old_password": "SecurePass123!",
  "new_password": "NewSecurePass456!",
  "new_password2": "NewSecurePass456!"
}
```

**Response:**
```json
{
  "message": "Password changed successfully."
}
```

### 6. Refresh Token

```bash
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 7. Logout

```bash
POST /api/auth/logout/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**
```json
{
  "message": "Logout successful."
}
```

## Authentication

This API uses JWT (JSON Web Token) authentication. After login or registration, you'll receive:

- **Access Token**: Used to authenticate API requests (expires in 60 minutes)
- **Refresh Token**: Used to obtain new access tokens (expires in 7 days)

Include the access token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

## Technology Stack

- **Django 4.2.7**: Web framework
- **Django REST Framework 3.14.0**: REST API toolkit
- **PostgreSQL**: Database
- **SimpleJWT**: JWT authentication
- **python-decouple**: Environment configuration

## Project Organization

### Apps Structure
- `backend/apps/users/`: User authentication and profile management
  - `models.py`: Custom User model with email authentication
  - `serializers.py`: Request/response serializers
  - `views.py`: API view logic
  - `urls.py`: URL routing
  - `admin.py`: Django admin interface

### Configuration
- `backend/config/`: Main project configuration
  - `settings.py`: Django settings with PostgreSQL and JWT config
  - `urls.py`: Root URL configuration
  - `wsgi.py`/`asgi.py`: Server configurations

## Development Tips

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Django Shell
```bash
python manage.py shell
```

### Django Admin
Access at: `http://127.0.0.1:8000/admin/`

## Common Issues & Solutions

### Issue: Database Connection Error
**Solution**: Check PostgreSQL is running and credentials in `.env` are correct

### Issue: Migration Errors
**Solution**: Delete migrations and database, recreate:
```bash
python manage.py migrate --run-syncdb
```

### Issue: Token Expired
**Solution**: Use the refresh token endpoint to get a new access token

## Security Notes

- Never commit `.env` file to version control
- Use strong SECRET_KEY in production
- Set DEBUG=False in production
- Configure proper ALLOWED_HOSTS in production
- Use HTTPS in production
- Implement rate limiting for authentication endpoints

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please create an issue in the repository.
