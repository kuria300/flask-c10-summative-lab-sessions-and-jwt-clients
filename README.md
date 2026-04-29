# Flask JWT Authentication & Expense API

## Project Description

This is a professional Flask REST API that provides secure authentication using JWT tokens stored in HTTP-only cookies, coupled with a complete expense system. The application demonstrates best practices in backend development including secure password hashing, token-based authentication and comprehensive API design.

### Key Features

- **Secure JWT Authentication**: Access and refresh tokens stored in HTTP-only cookies for enhanced security
- **User Account Management**: Registration and login with bcrypt password hashing
- **Expense Tracking**: Full CRUD operations for managing expenses
- **Pagination Support**: Efficient data retrieval with built-in pagination
- **Database Persistence**: SQLite database with flask-SQLAlchemy ORM
- **Data Validation**: Marshmallow schemas for input validation and serialization
- **CORS Support**: Configured for local frontend development (optional only if using frontend code provided one can just use postman)
- **Comprehensive Error Handling**: Detailed error responses for debugging

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Running the Server](#running-the-server)
4. [API Endpoints](#api-endpoints)
5. [Authentication](#authentication)
6. [Testing with Postman](#testing-with-postman)
7. [Project Structure](#project-structure)
8. [Database & Seeding](#database--seeding)
9. [Dependencies](#dependencies)
10. [Environment Variables](#environment-variables)
11. [Author](#Author)
12. [Contributing](#Contributing)
13. [License](#license)

## Installation

### Prerequisites

- Python 3.10 or higher
- Pipenv (package manager)

### Step-by-Step Setup

1. **Clone and navigate to the project directory**:
   ```bash
   git clone (https://github.com/username/repo.git)

   cd backend-auth
   ```

2. **Install dependencies using Pipenv**:
   ```bash
   pipenv install or pipenv sync
   ```

3. **Activate the virtual environment**:
   ```bash
   pipenv shell
   ```

4. **Set up environment variables** (see [Environment Variables](#environment-variables) section)

5. **Initialize the database**:
   ```bash
   # Create database tables
   flask db upgrade
   ```
   
   If you're starting fresh:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Populate the database with sample data** (optional):
   ```bash
   python seed.py
   ```

## Configuration

The application uses a configuration file (`config.py`) that sets up:

- **Database**: SQLite database stored at `instance/db.db`
- **JWT Configuration**: 
  - Tokens stored in HTTP-only cookies
  - Access token path: `/api/`
  - Refresh token path: `/token/refresh`
  - CSRF protection enabled for secure operations
- **Secret Key** set up shown (see [Environment Variables](#environment-variables) section) then populated from env file.


## Running the Server

### Start the Flask development server:

```bash
python app.py
```

**Default Configuration:**
- Host: `http://127.0.0.1:5001`
- Port: `5001`

### Custom Port:

Modify the port in `app.py`:

```python
if __name__== "__main__":
    app.run(port=5000)  
```

Then run:

```bash
python app.py
```

## API Endpoints

### Authentication

**Sign Up - Create New Account**
```
POST /auth/signup
Body: { "username": "string", "password": "string" }
```

**Log In - Get Access Tokens**
```
POST /auth/login
Body: { "username": "string", "password": "string" }
```

**Refresh Token - Get New Access Token**
```
POST /token/refresh
(Use when access token expires)
```

**Log Out - Clear Cookies**
```
DELETE /api/auth/logout
```

### Expense Management (Login Required due to Token-protected route)

**Get All Your Expenses**
```
GET /api/resource?page=1&per_page=10
```

**Create New Expense**
```
POST /api/resource
Body: { "title": "string", "amount": "number", "description": "string" }
```

**Get One Expense**
```
GET /api/resource/1
Replace 1 with the expense ID
```

**Update Expense**
```
PATCH /api/resource/1
Body: { "title": "string", "amount": "number", "description": "string" }
```

**Delete Expense**
```
DELETE /api/resource/1
Replace 1 with the expense ID
```

### Home

**API Health Check**
```
GET / (Home)
```

## Authentication

### JWT Cookie-Based Authentication

This API uses JWT tokens stored in **HTTP-only cookies** for enhanced security. HTTP-only cookies cannot be accessed by JavaScript, protecting against XSS attacks.

#### Token Types

1. **Access Token** (`access_token`):
   - Used for authenticating API requests
   - Short-lived token
   - Automatically attached to protected requests
   - Sent in cookie with path `/api/`

2. **Refresh Token** (`refresh_token`):
   - Used only to obtain new access tokens
   - Longer-lived token
   - Sent in cookie with path `/token/refresh`
   - Used when access token expires

#### Authentication Flow

```
1. User Registration
   POST /auth/signup
   ↓
2. User Login
   POST /auth/login
   ↓ Sets cookies: access_token, refresh_token
   ↓
3. Access Protected Routes
   GET /api/resource (cookie auto-sent)
   ↓
4. Access Token Expires
   POST /token/refresh (using refresh token)
   ↓ Returns new access_token in cookie
   ↓
5. Logout
   DELETE /api/auth/logout
   ↓ Clears all cookies
```

#### Protected Routes

All endpoints prefixed with `/api/` are protected and require a valid JWT access token. If the token is missing, invalid, or expired, the API returns:

- **401 Unauthorized**: Missing token
- **401 Token Expired**: Session expired (use refresh endpoint)
- **422 Unprocessable Entity**: Invalid or malformed token

### Error Responses custom exanple in app.py:

```json
// Missing token
{
  "message": "You must log in to access this resource"
}

// Invalid token
{
  "error": "invalid_token",
  "message": "Token is invalid or malformed"
}

// Expired token
{
  "error": "token_expired",
  "message": "Your session has expired. Please log in again"
}
```

## Testing with Postman

### Setup Postman Environment

1. **Open Postman** and create a new collection
2. **Configure Cookie Handling**:
   - Go to Settings → General
   - Enable "Automatically follow redirects" (on by Default)
   - Ensure cookie jar is enabled (on by Default)

3. **Create Environment Variables** (optional):
   - Create an environment called "Flask API"
   - Set `base_url` = `http://localhost:5001`
   - Set `username` = `testuser`
   - Set `password` = `testpass123`

### Testing Workflow

#### 1. User Registration

```
POST http://localhost:5001/auth/signup
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securePassword123"
}
```

**Expected Response (201 Created)**:
```json
{
  "id": 1,
  "username": "johndoe"
}
```

#### 2. User Login

```
POST http://localhost:5001/auth/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securePassword123"
}
```

**Expected Response (200 OK)**:
```json
{
  "message": "login successful"
}
```

**Cookies Set**:
- `access_token` (HTTP-only)
- `refresh_token` (HTTP-only)

#### 3. Access Protected Route

```
GET http://localhost:5001/api/resource?page=1&per_page=10
```

Postman will **automatically include cookies** in the request.

**Expected Response (200 OK)**:
```json
{
  "items": [
    {
      "id": 1,
      "title": "Groceries",
      "amount": 45.50,
      "description": "Weekly shopping"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total_pages": 2,
    "total_items": 15,
    "has_next": true,
    "has_prev": false
  }
}
```

#### 4. Create Expense

```
POST http://localhost:5001/api/resource
Content-Type: application/json

{
  "title": "Office Supplies",
  "amount": 125.75,
  "description": "Purchased pens, notebooks, and folders"
}
```

**Expected Response (200 OK)**:
```json
{
  "message": "expense created successfully!"
}
```

#### 5. Get Single Expense

```
GET http://localhost:5001/api/resource/1
```

**Expected Response (200 OK)**:
```json
{
  "id": 1,
  "title": "Office Supplies",
  "amount": 125.75,
  "description": "Purchased pens, notebooks, and folders"
}
```

#### 6. Update Expense

```
PATCH http://localhost:5001/api/resource/1
Content-Type: application/json

{
  "title": "Office Supplies Updated",
  "amount": 135.00,
  "description": "Purchased pens, notebooks, folders, and markers"
}
```

**Expected Response (200 OK)**:
```json
{
  "message": "expense updated"
}
```

#### 7. Delete Expense

```
DELETE http://localhost:5001/api/resource/1
```

**Expected Response (200 OK)**:
```json
{
  "message": "expense deleted"
}
```

#### 8. Refresh Token

```
POST http://localhost:5001/token/refresh
```

**Expected Response (200 OK)**:
```json
{
  "refresh": "new access_token created"
}
```

**Cookies Updated**:
- New `access_token` set in response

#### 9. Logout

```
DELETE http://localhost:5001/api/auth/logout
```

**Expected Response (200 OK)**:
```json
{
  "message": "logout successful"
}
```

**Cookies Cleared**:
- `access_token` removed
- `refresh_token` removed

## Project Structure

```
backend-auth/
├── app.py                          # Main Flask application & route registration
├── config.py                       # Configuration settings (DB, JWT, CORS)
├── extensions.py                   # Flask extensions initialization
├── models.py                       # SQLAlchemy database models
├── seed.py                         # Database seeding with Faker data
├── Pipfile                         # Pipenv dependencies
├── Pipfile.lock                    # Locked dependency versions
├── .env                            # Environment variables (not in repo)
├── instance/
│   └── db.db                       # SQLite database file (auto-created)
├── migrations/                     # Alembic database migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       ├── [migration_files].py
├── resources/                      # API resource handlers (routes)
│   ├── home.py
│   ├── auth/
│   │   ├── signup.py              # User registration
│   │   ├── login.py               # User login
│   │   ├── logout.py              # User logout
│   │   └── refresh_tkn.py         # Token refresh
│   └── expenses/
│       ├── resource_list.py       # GET/POST expenses (list & create)
│       └── expense_detail.py      # GET/PATCH/DELETE individual expense
└── schemas/                        # Marshmallow validation schemas
    ├── person_schema.py           # User/Person schema
    └── expense_schema.py          # Expense schema
```

## Database & Seeding

### Database Models

#### Person Model
Represents application users with secure password storage:

```python
class Person(db.Model):
    id: Integer (Primary Key)
    username: String(100) - Unique, required
    password: String(150) - Hashed with bcrypt
    expenses: Relationship (One-to-Many with Expense)
```

#### Expense Model
Represents expense entries linked to users:

```python
class Expense(db.Model):
    id: Integer (Primary Key)
    title: String(100) - Required
    amount: Numeric(10,2) - Currency amount
    description: Text - Optional details
    person_id: Integer (Foreign Key) - Links to Person
    person: Relationship (Many-to-One with Person)
```

### Seeding Sample Data

The `seed.py` script uses the Faker library to generate realistic sample data:

```bash
python seed.py
```

**What it creates**:
- some random expenses with:
  - Faker-generated titles and descriptions
  - Random amounts between $1,000 and $5,000
  - Associated with existing users in the database

**Note**: The seed script assumes users already exist in the database. Create at least one user via signup before running the seed.

### Manual Seeding Example

```python
# Create a user programmatically
user = Person(username="demo_user")
user.hash_password("demo_password")
db.session.add(user)
db.session.commit()

# Then run seed.py
python seed.py
```

## Dependencies

All dependencies are in the `Pipfile`. Install with:

```bash
pipenv install
```

### What's Included:

- **Flask** - Web framework
- **Flask-RESTful** - REST API toolkit  
- **Flask-SQLAlchemy** - Database ORM
- **Flask-Migrate** - Database migrations
- **Flask-JWT-Extended** - JWT authentication
- **Flask-Bcrypt** - Secure password hashing
- **Flask-Marshmallow** - Data validation & serialization
- **Flask-CORS** - Cross-origin requests support
- **python-dotenv** - Load environment variables
- **Faker** - Generate fake data for testing

### Installation

```bash
pipenv install 

pipenv sync (to use exact versions in lock file)
```

To add a new dependency:

```bash
pipenv install package-name
```

## Environment Variables

Create a `.env` file in the project root directory with the following variables (optional some in Config.py):

```env
# JWT Secret Key (generate a strong random key)
SECRET_KEY=your-super-secret-key-change-this-in-production
```

### Generating a Secure Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and use it as your `SECRET_KEY` in the `.env` file then exported to Config.py.

## Author

Eugene Kuria Maina

## Contributing

Contributions are always welcome!

Please adhere to this project's `code of conduct`.


## License

This project is provided as-is for educational purposes. Modify and use as needed for your projects 
