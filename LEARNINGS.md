# 📚 Secure Login System - Learnings

> My personal revision notes while building this project from scratch.

---

## Goal

I am writing these notes so that before interviews or future projects, I can quickly revise what I have actually built instead of watching tutorials again.

Each day I will write:
- What I learned
- Important concepts
- Important commands
- Common mistakes
- Interview points

---

# Day 1 - Project Setup

## 🎯 Objective
Set up the FastAPI project and understand the basic project structure.

## 🧠 Concepts Learned
- FastAPI is a modern Python framework for building APIs.
- A Virtual Environment (venv) keeps project dependencies isolated.
- Uvicorn is the server that runs the FastAPI application.
- Swagger UI is automatically generated at `/docs`.

## 💻 Commands Used

```bash
source venv/bin/activate
uvicorn main:app --reload
```

## 📁 Files Created
- main.py

## ❌ Mistakes I Made
- Forgot to activate the virtual environment.
- Didn't understand why `uvicorn` was not found.

## 💡 Interview Notes
- FastAPI is an ASGI framework.
- Uvicorn is an ASGI server.
- Virtual environments prevent dependency conflicts.

## 📌 Summary
Built and ran my first FastAPI application successfully.

---

# Day 2 - PostgreSQL & SQLAlchemy

## 🎯 Objective
Connect FastAPI with PostgreSQL and understand how Python communicates with the database.

## 🧠 Concepts Learned
- PostgreSQL is a relational database.
- SQLAlchemy is an ORM (Object Relational Mapper).
- ORM allows us to work with Python objects instead of writing SQL everywhere.
- A Model represents a table in the database.
- A Session is used to communicate with the database.

## 💻 Commands Used

```bash
psql postgres
```

```sql
\c secure_login_db
\dt
SELECT * FROM users;
```

## 📁 Files Created
- database/database.py
- config.py

## ❌ Mistakes I Made
- Had trouble connecting PostgreSQL.
- Got confused between database, table and model.
- Didn't understand where `.git` should be located after restructuring the project.

## 💡 Interview Notes
- ORM stands for Object Relational Mapper.
- SQLAlchemy converts Python objects into SQL queries.
- Sessions are used to execute database operations.

## 📌 Summary
Connected FastAPI with PostgreSQL and learned how SQLAlchemy manages database communication.

---

# Day 3 - User Registration API

## 🎯 Objective
Build a user registration API that accepts user data and stores it in PostgreSQL.

## 🧠 Concepts Learned
- APIRouter helps organize API endpoints.
- Pydantic validates incoming request data.
- POST requests are used to create new resources.
- Dependency Injection (`Depends`) provides database sessions.
- SQLAlchemy models map Python classes to database tables.

## 🔄 Request Flow

```
Client
   │
   ▼
Swagger / Postman
   │
   ▼
FastAPI Router
   │
   ▼
Pydantic Validation
   │
   ▼
SQLAlchemy
   │
   ▼
PostgreSQL
```

## 💻 Commands Used

```bash
uvicorn main:app --reload
```

```bash
git add .
git commit -m "Implement user registration API with PostgreSQL"
git push
```

## 📁 Files Created
- models/user.py
- schemas/user.py
- routers/auth.py

## ❌ Mistakes I Made
- Forgot Python indentation in functions.
- Accidentally moved the Git repository to the wrong folder.
- Had trouble understanding how routers connect to main.py.

## 💡 Interview Notes
- APIRouter keeps APIs modular.
- Pydantic validates request data automatically.
- SQLAlchemy ORM converts Python objects into database records.

## 📌 Summary
Built my first production-style Registration API using FastAPI, SQLAlchemy and PostgreSQL.

---

# Day 4 - Secure Authentication

## 🎯 Objective
Build a secure authentication system by hashing passwords, verifying user credentials, and implementing a login API.

## 🧠 Concepts Learned

### Password Security
- Never store passwords in plain text.
- bcrypt hashes passwords securely.
- Hashing is one-way and cannot be reversed.
- verify_password() compares a plain password with a stored hash.

### SQLAlchemy
- `db.add()` inserts a new record.
- `select(User)` reads data from the database.
- `.where()` filters records.
- `.scalar_one_or_none()` returns one result or None.

### Authentication Flow

```
Register

User
 │
 ▼
Validate Input
 │
 ▼
Check Duplicate Email
 │
 ▼
Hash Password
 │
 ▼
Store in PostgreSQL
```

```
Login

User
 │
 ▼
Find User
 │
 ▼
Verify Password
 │
 ▼
Success / 401 Unauthorized
```

## 💻 Commands Used

```bash
pip install "passlib[bcrypt]"
pip uninstall bcrypt
pip install bcrypt==4.0.1
pip freeze > requirements.txt
```

```bash
git add .
git commit -m "Implement secure login with password verification"
git push
```

## 📁 Files Created

- utils/security.py

## 📁 Files Updated

- routers/auth.py
- schemas/user.py
- main.py

## ❌ Mistakes I Made

- bcrypt version compatibility issue.
- Python indentation errors.
- SyntaxError due to incorrect indentation.
- Forgot to import required modules.
- Swagger stopped loading because the server crashed after a syntax error.

## 💡 Interview Notes

- bcrypt uses random salt, so the same password generates different hashes.
- Never compare hashed passwords directly.
- Use `verify_password()` instead.
- 400 → Bad Request
- 401 → Unauthorized
- HTTPException returns proper API responses.

## 📌 Summary

Built a secure user authentication system with password hashing, login verification, duplicate email validation, and professional API error handling.

---

# Day 5 - JWT Authentication & Protected Routes

## 🎯 Objective

Implement JWT (JSON Web Token) authentication to securely identify logged-in users and protect private API routes.

## 🧠 Concepts Learned

### JWT (JSON Web Token)

- JWT is a signed token used for authentication.
- After successful login, the server generates a JWT instead of asking for the password again.
- The client stores the JWT and sends it with future requests.
- JWT contains three parts:
  - Header
  - Payload
  - Signature

### JWT Claims

- `sub` (Subject) → Identifies the logged-in user.
- `exp` (Expiration) → Specifies when the token expires.

### JWT Security

- Tokens are digitally signed using a `SECRET_KEY`.
- The server verifies the signature before trusting the token.
- If the token is modified or expired, authentication fails.
- JWTs should have an expiration time to reduce security risks if they are stolen.

### Protected Routes

- Public routes:
  - `/auth/register`
  - `/auth/login`
- Protected route:
  - `/auth/profile`

- Protected routes verify the JWT before returning data.

## 🔄 Authentication Flow

```text
User Login
    │
    ▼
Verify Email & Password
    │
    ▼
Generate JWT
    │
    ▼
Send JWT to Client
    │
    ▼
Client Stores JWT
    │
    ▼
Client Sends JWT
    │
    ▼
Server Verifies JWT
    │
    ▼
Protected Route Access
```

## 💻 Commands Used

```bash
pip install "python-jose[cryptography]"

pip freeze > requirements.txt

git add .
git commit -m "Implement JWT authentication and protected routes"
git push
```

## 📁 Files Created

- utils/jwt_handler.py

## 📁 Files Updated

- routers/auth.py

## 🔑 Functions Implemented

- `create_access_token()`
- `verify_access_token()`

## ❌ Mistakes I Made

- Indentation errors caused `return outside function`.
- Forgot that JWTs are sent through the `Authorization` header.
- Swagger did not send the Authorization header correctly, but testing with `curl` confirmed the backend was working.

## 💡 Interview Notes

- JWT stands for JSON Web Token.
- JWT is authentication, not encryption.
- bcrypt is hashing, not encryption.
- Authentication verifies who the user is.
- Authorization determines what the user can access.
- JWTs are usually sent in the `Authorization` header as:
  ```
  Authorization: Bearer <token>
  ```
- `SECRET_KEY` is used to digitally sign JWTs.
- `HS256` is the signing algorithm used in this project.
- Protected routes verify the JWT before allowing access.

## 📌 Summary

Built a complete JWT authentication system capable of generating JWTs after login, verifying JWTs, and protecting API routes using bearer tokens.