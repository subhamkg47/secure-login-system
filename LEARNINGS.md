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
- JWT consists of three parts:
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
- JWTs should always have an expiration time to reduce security risks.

### OAuth2 Integration

- Replaced manual Authorization header parsing with FastAPI's `OAuth2PasswordBearer`.
- Login endpoint now uses `OAuth2PasswordRequestForm`.
- Swagger UI authenticates users using the built-in **Authorize** button.
- Protected routes automatically receive the JWT using `Depends(oauth2_scheme)`.

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
Client Sends JWT in Authorization Header
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

- `utils/jwt_handler.py`

## 📁 Files Updated

- `routers/auth.py`

## 🔑 Functions Implemented

- `create_access_token()`
- `verify_access_token()`

## ❌ Mistakes I Made

- Indentation errors caused `return outside function`.
- Accidentally created duplicate `@router.get("/profile")` decorators.
- Initially implemented JWT authentication manually using `Header()`.
- Learned how `OAuth2PasswordBearer` simplifies authentication and integrates with Swagger.
- Used `curl` to verify the backend worked before debugging Swagger.

## 💡 Interview Notes

- JWT stands for **JSON Web Token**.
- JWT is **signed**, not encrypted.
- bcrypt performs **hashing**, not encryption.
- Authentication verifies **who the user is**.
- Authorization determines **what the user can access**.
- JWTs are usually sent in the HTTP `Authorization` header:

```text
Authorization: Bearer <token>
```

- `SECRET_KEY` is used to digitally sign JWTs.
- `HS256` is the signing algorithm used in this project.
- `OAuth2PasswordBearer` automatically extracts the JWT from the Authorization header.
- `OAuth2PasswordRequestForm` sends login credentials as form data.
- Protected routes verify the JWT before allowing access.

## ⭐ Key Takeaways

- Never store plain-text passwords.
- Always hash passwords before storing them.
- JWT allows users to stay logged in without sending passwords repeatedly.
- Protected routes should always verify the JWT before returning data.
- Read Python tracebacks carefully—they usually point to the actual problem.
- Test APIs with both Swagger and `curl` to isolate frontend and backend issues.

## 📌 Summary

Built a production-style authentication system using FastAPI, PostgreSQL, SQLAlchemy, bcrypt, JWT, and OAuth2PasswordBearer. Users can register, log in securely, receive a JWT, and access protected routes through Swagger or any API client.

## Reflection

### What did I build today?

A complete JWT authentication system with secure login, JWT generation, JWT verification, OAuth2 integration, and protected API routes.

### What was the hardest bug today?

Fixing Python indentation errors and understanding why Swagger wasn't sending the Authorization header before migrating to OAuth2PasswordBearer.

### If someone asked me to explain today's work without looking at the code, could I?

Yes. I understand how a user logs in, how a JWT is generated, how it is verified, and how protected routes authenticate users using bearer tokens.

---

# Day 6 - Dependency Injection & Reusable Authentication

## 🎯 Objective

Refactor the authentication system by moving JWT verification into a reusable dependency using FastAPI's Dependency Injection (`Depends`).

## 🧠 Concepts Learned

### Dependency Injection (Depends)

- `Depends()` is FastAPI's Dependency Injection system.
- It allows reusable logic to be written once and injected into multiple endpoints.
- It reduces code duplication and keeps the code clean and maintainable.

### Why Dependency Injection?

Without `Depends()`, every protected endpoint would have to:

- Read the JWT
- Verify the JWT
- Handle invalid tokens
- Return the authenticated user

This causes duplicate code and makes future updates difficult.

With `Depends()`, all authentication logic is written once and reused everywhere.

### Separation of Concerns

Each function should have only one responsibility.

Before refactoring:

- `/profile` was responsible for:
  - Reading the JWT
  - Verifying the JWT
  - Handling authentication errors
  - Returning profile data

After refactoring:

- `get_current_user()`
  - Reads the JWT
  - Verifies the JWT
  - Returns the authenticated user

- `/profile`
  - Only returns profile information

This makes the project much cleaner and easier to maintain.

### Reusable Dependencies

Created a new folder:

```
dependencies/
```

Created:

```
dependencies/auth.py
```

This file now contains reusable authentication logic that can be shared across all routers.

## 🔄 Authentication Flow

```text
Client Request
      │
      ▼
Authorization Header
      │
      ▼
OAuth2PasswordBearer
      │
      ▼
Depends(get_current_user)
      │
      ▼
Verify JWT
      │
      ▼
Return Authenticated User
      │
      ▼
Protected Endpoint
```

## 📁 Files Created

- `dependencies/auth.py`

## 📁 Files Updated

- `routers/auth.py`

## 🔑 Functions Implemented

- `get_current_user()`

## ❌ Mistakes I Made

- Forgot why creating another `oauth2_scheme` in the dependencies folder was useful.
- Initially thought authentication should remain inside every endpoint.
- Learned that reusable dependencies make debugging and future updates much easier.

## 💡 Interview Notes

- `Depends()` is FastAPI's Dependency Injection system.
- Dependency Injection helps reduce code duplication.
- Shared logic should be written once and reused.
- `get_current_user()` is responsible only for authentication.
- Protected endpoints should focus only on business logic.
- Separation of Concerns makes applications easier to maintain.
- Reusable dependencies are a common pattern in production backend applications.

## ⭐ Key Takeaways

- Never repeat the same authentication code in multiple endpoints.
- Centralizing authentication makes future changes easier.
- Every function should have a single responsibility.
- Clean architecture is just as important as writing working code.
- Good backend code is modular, reusable, and easy to maintain.

## 📌 Summary

Refactored the authentication system by introducing Dependency Injection with `Depends()`. Authentication is now centralized in `get_current_user()`, allowing every protected endpoint to reuse the same logic while keeping business logic clean and maintainable.

## Reflection

### What did I build today?

A reusable authentication dependency using FastAPI's `Depends()` that verifies JWTs and can be shared by all protected routes.

### What was the biggest lesson today?

I learned that writing code that works is only the first step. Professional backend development is about writing reusable, maintainable, and well-organized code.

### If someone asked me to explain today's work without looking at the code, could I?

Yes. I understand why Dependency Injection exists, how `Depends()` works, why `get_current_user()` is reusable, and how it keeps authentication separate from business logic.

---

# Day 7 - Fetch Current User from Database

## 🎯 Objective

Improve the authentication system by fetching the authenticated user from PostgreSQL instead of returning only the JWT payload.

## 🧠 Concepts Learned

### Why Fetch the User from the Database?

- JWT is only used to identify the user.
- After verifying the JWT, extract the user's email (`sub` claim).
- Query PostgreSQL to retrieve the latest user information.
- Return the complete `User` object instead of the JWT payload.

### Why Not Trust Only the JWT?

- JWT is a snapshot created at login.
- User information may change after the token is issued.
- Example:
  - User role changes.
  - User account is deleted.
  - User account is deactivated.
- Fetching the user from the database always provides the latest information.

### Database Authentication Flow

```text
Client Request
      │
      ▼
Receive JWT
      │
      ▼
Verify JWT
      │
      ▼
Extract Email (sub)
      │
      ▼
Search PostgreSQL
      │
      ▼
Return User Object
      │
      ▼
Protected Endpoint
```

## 📁 Files Updated

- `dependencies/auth.py`
- `routers/auth.py`

## 🔑 Changes Made

- Added database session (`Depends(get_db)`) inside `get_current_user()`.
- Extracted email from the JWT payload.
- Queried PostgreSQL using SQLAlchemy.
- Checked whether the user still exists.
- Returned the complete `User` object instead of the JWT payload.
- Updated `/profile` to use `current_user.email`.

## 💡 Interview Notes

- JWT should identify the user, not store all user information.
- Production applications usually verify the user against the database after validating the JWT.
- Returning a database model is cleaner than returning the JWT payload.
- `Depends(get_db)` injects a reusable database session.
- `Depends(get_current_user)` injects the authenticated user into protected endpoints.

## ⭐ Key Takeaways

- Always use the JWT to identify the user, then fetch the latest data from the database.
- Authentication logic should remain centralized in one dependency.
- Protected endpoints should focus only on business logic.
- Returning the authenticated `User` object makes future development easier.

## 📌 Summary

Refactored the authentication system to return the authenticated user directly from PostgreSQL after JWT verification. The project now follows a more production-ready authentication architecture by separating authentication from business logic and always using the latest user information from the database.