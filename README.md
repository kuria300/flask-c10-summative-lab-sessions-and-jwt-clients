# Backend Auth Api

## Project Title
Flask Authentication & User-Owned Expense Tracker API

---

## Project Description

This project is a RESTful API built with Flask that provides:

- User authentication (signup, login, logout)
- JWT-based secure access using cookies
- User-specific expense management
- Full CRUD operations on expenses
- Database migrations using Flask-Migrate
- Data validation using Marshmallow

Each user can only access their own expenses, ensuring full data isolation and security.

---

## ⚙️ Installation Instructions

### 1. Clone the repository

git clone <your-repo-url>
cd backend-auth

## ⚙️ Install Dependencies

Using Pipenv:

pipenv install
pipenv shell
python main.py / app.py

## Security Features

- JWT stored in HttpOnly cookies  
- User-specific data isolation  
- CSRF protection enabled (if configured)  
- Password hashing using Bcrypt  

---

## Dependencies (Pipfile)

Main dependencies include:

- Flask  
- Flask-SQLAlchemy  
- Flask-Migrate  
- Flask-JWT-Extended  
- Flask-RESTful  
- Flask-CORS  
- Flask-Bcrypt  
- Flask-Marshmallow  
- Marshmallow  
- python-dotenv  
- Faker  
