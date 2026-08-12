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

---

# Day 8 - Server-Side Logout with JWT Blacklisting

## 🎯 Objective

Implement secure server-side logout by invalidating JWT tokens after logout instead of only removing them from the client.

## 🧠 Concepts Learned

### Why Server-Side Logout?

- JWTs are stateless, meaning the server does not automatically know if a user has logged out.
- Simply deleting the JWT on the client is not secure because a copied token can still be used until it expires.
- To solve this, revoked tokens are stored in a blacklist and rejected on future requests.

### Token Blacklisting

- Created an in-memory blacklist using a Python `set`.
- Added helper functions:
  - `blacklist_token()` – Adds a JWT to the blacklist.
  - `is_blacklisted()` – Checks whether a JWT has been revoked.
- Every protected request checks the blacklist before verifying the JWT.

### Logout Flow

```text
User Logs In
      │
      ▼
JWT Issued
      │
      ▼
User Logs Out
      │
      ▼
JWT Added to Blacklist
      │
      ▼
Future Requests
      │
      ▼
Token Found in Blacklist
      │
      ▼
401 Unauthorized
```

## 📁 Files Created

- `services/token_blacklist.py`

## 📁 Files Updated

- `dependencies/auth.py`
- `routers/auth.py`

## 🔑 Changes Made

- Created an in-memory JWT blacklist.
- Implemented `blacklist_token()` and `is_blacklisted()`.
- Updated authentication dependency to reject revoked tokens before JWT verification.
- Added `/auth/logout` endpoint.
- Refactored logout to use `Depends(oauth2_scheme)` for consistent authentication.
- Successfully tested server-side logout.

## 💡 Interview Notes

- JWT is stateless, so logout requires additional server-side logic.
- A blacklist is one way to invalidate JWTs before they expire.
- `set` is used because membership checks are much faster than a list.
- Authentication credentials should be passed using the `Authorization` header.
- Checking the blacklist before JWT verification avoids unnecessary processing.

## ⭐ Key Takeaways

- Server-side logout is more secure than deleting the token only on the client.
- Authentication should remain consistent across all protected endpoints.
- Revoked tokens should always be rejected before accessing protected resources.
- Helper functions make authentication code cleaner and reusable.

## 📌 Summary

Implemented secure server-side logout using JWT blacklisting. Revoked tokens are now rejected across all protected routes, fulfilling the FOSSEE requirement for server-side session invalidation.

---

# Day 9 - File Model & Database Relationships

## 🎯 Objective

Design the database structure for storing user files and establish a one-to-many relationship between users and files using SQLAlchemy.

## 🧠 Concepts Learned

### One-to-Many Relationship

- A single user can own multiple files.
- Each file belongs to exactly one user.
- This relationship is implemented using a foreign key and SQLAlchemy relationships.

### File Table Design

The `files` table contains:

- `id` – Unique identifier for each file.
- `filename` – Name of the file displayed to the user.
- `filepath` – Actual storage location of the file.
- `user_id` – Foreign key that links the file to its owner.

### Foreign Key

- `ForeignKey("users.id")` creates a relationship between the `files` table and the `users` table.
- It ensures every file belongs to a valid user.

### SQLAlchemy Relationship

- `relationship()` allows SQLAlchemy to navigate between related objects.
- From a user:
  ```python
  user.files
  ```
  returns all files owned by that user.
- From a file:
  ```python
  file.owner
  ```
  returns the user who owns the file.

### Model Registration

- SQLAlchemy only creates tables for models that are imported into the application.
- Importing the `File` model in `main.py` registers it before running:
  ```python
  Base.metadata.create_all(bind=engine)
  ```

## 📁 Files Created

- `models/file.py`

## 📁 Files Updated

- `models/user.py`
- `main.py`

## 🔑 Changes Made

- Created the `File` model.
- Added `filename`, `filepath`, and `user_id` columns.
- Linked the `File` model to the `User` model using `ForeignKey`.
- Implemented bidirectional relationships using `relationship()` and `back_populates`.
- Registered the `File` model so SQLAlchemy could create the `files` table.
- Verified that the `files` table was successfully created in PostgreSQL.

## 💡 Interview Notes

- A foreign key connects related tables in a relational database.
- `relationship()` is an ORM feature that allows navigation between related objects.
- One user can own many files, but each file belongs to only one user.
- `filename` stores the display name, while `filepath` stores the actual file location.
- Models must be imported before SQLAlchemy can create their database tables.

## ⭐ Key Takeaways

- Database relationships should be designed before building API endpoints.
- Foreign keys maintain data integrity between related tables.
- SQLAlchemy relationships simplify working with related data.
- A well-designed database makes authorization and ownership checks much easier.

## 📌 Summary

Designed and implemented the database layer for the file management system by creating the `File` model, establishing a one-to-many relationship with the `User` model, and successfully creating the `files` table in PostgreSQL. This lays the foundation for implementing secure file access in the upcoming stages of the FOSSEE project.


---

# Day 10 - Secure File Access & Authorization

## 🎯 Objective

Implement secure file access for authenticated users and ensure that users can only view and download files belonging to their own account.

This directly addresses the FOSSEE requirements for:

- User-specific file listing
- Single-file access
- File downloading
- Cross-user data isolation

---

## 🧠 Concepts Learned

### Authentication vs Authorization

**Authentication** answers:

> Who is the user?

Our application determines this using the validated JWT.

**Authorization** answers:

> What is the authenticated user allowed to access?

For files, the authenticated user's ID is compared with the file's `user_id`.

---

## 🔐 User Data Isolation

The most important authorization rule is:

```python
File.user_id == current_user.id

A user must never be able to access another user's file simply by changing the file_id.
📂 File Ownership
Every file belongs to a specific user through:
user_id
Therefore, file access must always consider both:
file_id
+
current_user.id
rather than trusting the file_id alone.
📥 Secure File Download
The backend authenticates the user before allowing a file to be downloaded.
The server checks that the requested file belongs to the authenticated user before returning the physical file.
This prevents unauthorized users from accessing files belonging to another account.
🔄 Secure File Access Flow
Client
   │
   ▼
JWT Token
   │
   ▼
Authenticate User
   │
   ▼
Get current_user
   │
   ▼
Request File
   │
   ▼
Find File
   │
   ▼
Check File Ownership
   │
   ├── Not Owner → Reject Access
   │
   └── Owner → Allow Access
                    │
                    ▼
                Return File
📁 Files Created
routers/files.py
schemas/file.py
seed_files.py
📁 Files Updated
main.py
🔑 Changes Made
Created file-related API routes.
Added authenticated file listing.
Added single-file access.
Added file download functionality.
Connected files with authenticated users.
Implemented ownership-based authorization.
Added sample files for testing.
Tested file downloading through Swagger.
❌ Mistakes I Made
Initially misunderstood the difference between authentication and authorization.
Had to understand why checking only file_id is insecure.
Initially created sample PDF files that were only ASCII text.
Learned how to create valid PDF files.
Initially created an invalid ZIP file.
Learned to verify file types using the file command.
💡 Interview Notes
Authentication identifies the user.
Authorization determines what the user can access.
Never trust an object ID supplied by the client by itself.
Always verify resource ownership before returning protected data.
File IDs should not be treated as proof of ownership.
User data isolation is an important security requirement.
⭐ Key Takeaways
Authentication ≠ Authorization.
Every protected resource needs an authorization check.
current_user.id should be used when checking ownership.
File ownership must be enforced on the backend.
User data isolation prevents one user from accessing another user's resources.
📌 Summary
Implemented secure, user-specific file access using JWT authentication and ownership-based authorization. Users can access their own files while unauthorized access to another user's files is prevented.
---

# Day 11 - File Storage & Secure File Downloads

## 🎯 Objective

Complete the file management functionality by storing sample files, implementing secure file downloads, and verifying that users can only access files they own.

## 🧠 Concepts Learned

### 📂 File Storage

- File metadata is stored in PostgreSQL.
- The actual file is stored inside the `uploads/` directory.
- The database connects the file to its owner using `user_id`.

### 📥 File Download

FastAPI's `FileResponse` is used to return files to the client.

Before returning a file, the backend checks:

1. Whether the file exists in the database.
2. Whether the authenticated user owns the file.
3. Whether the actual file exists on the server.

### 🔐 Authorization

The important ownership check is:

```python
if file.user_id != current_user.id:
    raise HTTPException(
        status_code=403,
        detail="You do not have permission to access this file"
    )


    This prevents one user from accessing another user's files.
🧪 Testing
Tested:
Listing authenticated user's files
Accessing a specific file
Downloading a file
Accessing a non-existent file
Accessing another user's file
Expected responses:
200 → Authorized access
403 → User does not own the file
404 → File does not exist
💻 Commands Learned
mkdir -p uploads
file backend/uploads/*
du -h backend/uploads/*
❌ Mistakes I Made
Initially created sample PDFs as plain text files.
Learned that a .pdf extension does not make a file a real PDF.
Initially created an invalid ZIP file.
Learned to verify the actual file format before testing downloads.
💡 Interview Notes
Authentication determines who the user is.
Authorization determines what the user can access.
Never trust a file_id alone to authorize access.
Always check resource ownership before returning protected data.
FileResponse is used to send files from a FastAPI backend.
⭐ Key Takeaways
Every protected resource needs an authorization check.
File ownership should be enforced on the backend.
Database metadata and physical file storage are separate.
Always verify that stored files actually match their expected format.
📌 Summary
Implemented and tested secure file access and downloading. The backend now ensures that authenticated users can only access files belonging to their own account.


---

 #Day 12 - Login Security & Account Lockout

## 🎯 Objective

Improve the authentication system by protecting user accounts against repeated failed login attempts and learn how to safely update the PostgreSQL database using Alembic migrations.

## 🧠 Concepts Learned

### 🔒 Brute-Force Protection

Repeated failed login attempts can be used to guess a user's password.

A temporary account lockout helps reduce this risk.

Our rule:

```text
5 failed login attempts
        ↓
15-minute account lockout

📊 Tracking Login Attempts
Added two fields to the User model:
failed_attempts = Column(Integer, default=0, nullable=False)
locked_until = Column(DateTime, nullable=True)
failed_attempts stores the number of failed login attempts.
locked_until stores when the temporary lock expires.
⏳ Account Lockout
Before allowing login, the system checks whether the account is currently locked.
After 5 failed attempts, the account is locked for 15 minutes.
Even the correct password cannot bypass an active lockout.
🔄 Reset After Successful Login
After a successful login:
existing_user.failed_attempts = 0
existing_user.locked_until = None
This resets the authentication security state.
🗃️ Alembic Database Migrations
Changing a SQLAlchemy model does not automatically change an existing PostgreSQL database.
Alembic is used to safely manage database schema changes.
💻 Commands Used
alembic init alembic
alembic revision --autogenerate -m "Add login lockout fields"
alembic upgrade head
🔄 Migration Flow
SQLAlchemy Model
       ↓
Alembic Autogenerate
       ↓
Migration File
       ↓
alembic upgrade head
       ↓
PostgreSQL Schema Updated
🔑 Alembic Metadata
Configured Alembic to use:
target_metadata = Base.metadata
This allows Alembic to compare the SQLAlchemy models with the existing database schema.
🧪 Testing
Tested the complete authentication security flow:
Wrong password
      ↓
Failed attempts increase
      ↓
5 failed attempts
      ↓
15-minute lockout
      ↓
Correct password while locked
      ↓
401 Unauthorized
      ↓
Lock expires
      ↓
Correct password
      ↓
200 OK
      ↓
failed_attempts = 0
locked_until = None
The final database verification showed:
Failed attempts: 0
Locked until: None
❌ Mistakes I Made
Initially expected changes to the SQLAlchemy model to automatically appear in PostgreSQL.
Encountered an SQLAlchemy relationship error because the File model was not imported before querying User.
Accidentally typed db.clos() instead of db.close().
Tried to use variables from a previous Python REPL session.
Learned why the correct password is rejected while the account is still locked.
💡 Interview Notes
Account lockout helps protect against brute-force attacks.
Authentication state should be maintained server-side.
locked_until stores the exact expiration time of a temporary lock.
Alembic is used to manage SQLAlchemy database migrations.
--autogenerate detects differences between models and the database schema.
upgrade head applies pending migrations.
⭐ Key Takeaways
Changing a SQLAlchemy model does not automatically change PostgreSQL.
Database schema changes should be handled through migrations.
Failed login attempts should be tracked securely on the server.
Temporary lockouts can reduce brute-force attacks.
Successful authentication should reset failed-attempt state.
Security features should be tested through both the API and database.
📌 Summary
Implemented a temporary account lockout system that locks users for 15 minutes after 5 failed login attempts. Added the required database fields, created and applied an Alembic migration, and successfully tested the complete lockout and reset lifecycle.


----

# Day 13 - JWT Security Hardening & Environment Configuration

## 🎯 Objective

Improve the security of the JWT authentication system by moving sensitive configuration into environment variables, validating JWT claims safely, and ensuring access tokens always identify a user.

## 🧠 Concepts Learned

### 🔐 Environment-Based JWT Configuration

Sensitive JWT configuration should not be hard-coded inside Python source code.

The project now loads:

- `JWT_SECRET_KEY`
- `JWT_ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`

from the `.env` file.

The application also checks that the JWT secret exists before starting.

```python
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not set")
````

### 🔑 JWT Secret Key

The `SECRET_KEY` is used to digitally sign JWTs.

It should:

* Be long and random
* Never be hard-coded in source code
* Never be committed to Git
* Be stored securely as an environment variable

### 🧾 JWT Claims

The project uses two important JWT claims:

* `sub` → identifies the user
* `exp` → defines when the token expires

The token automatically receives an expiration time when it is created.

### 🛡️ Required `sub` Claim

Access tokens must identify the user they belong to.

The token creation function now checks:

```python
if "sub" not in to_encode:
    raise ValueError("Token subject (sub) is required")
```

This prevents the application from accidentally creating a token that cannot identify a user.

### 🔍 Safe JWT Validation

During authentication, the application now safely retrieves the subject:

```python
email = payload.get("sub")

if not email:
    raise HTTPException(
        status_code=401,
        detail="Invalid token"
    )
```

Using `.get()` prevents a missing `sub` claim from causing a `KeyError`.

Instead, the API correctly returns:

```text
401 Unauthorized
```

## 🔄 Improved Authentication Flow

```text
User Login
    │
    ▼
Verify Email & Password
    │
    ▼
Create JWT
    │
    ├── Add sub
    │
    └── Add exp
    │
    ▼
Send JWT to Client
    │
    ▼
Client Sends Bearer Token
    │
    ▼
Check Blacklist
    │
    ▼
Verify JWT Signature & Expiration
    │
    ▼
Check sub Claim
    │
    ├── Missing → 401
    │
    └── Present
          │
          ▼
      Find User
          │
          ▼
   Protected Route
```

## 🧪 Security Testing

### Valid Token

Normal login was tested successfully:

```text
POST /auth/login
200 OK
```

The resulting token successfully accessed:

```text
GET /auth/profile
200 OK
```

### Token Without `sub`

A correctly signed JWT without a `sub` claim was generated for testing.

The protected endpoint correctly returned:

```json
{
    "detail": "Invalid token"
}
```

with:

```text
401 Unauthorized
```

This confirmed that the application does not blindly trust the JWT payload.

### Token Creation Without `sub`

The following was tested:

```python
create_access_token({
    "email": "test@example.com"
})
```

The application correctly rejected it:

```text
ValueError: Token subject (sub) is required
```

This confirms that token creation also enforces the required user identity.

## 💻 Commands Used

```bash
python -m py_compile utils/jwt_handler.py

python -c "from utils.jwt_handler import create_access_token; create_access_token({'email':'test@example.com'})"

git status

git add backend/utils/jwt_handler.py

git commit -m "Require JWT subject claim"

git push
```

## 📁 Files Updated

* `backend/utils/jwt_handler.py`
* `backend/dependencies/auth.py`

## ❌ Mistakes I Made

* Initially hard-coded the JWT secret inside the Python source code.
* Accidentally exposed a generated JWT secret and replaced it with a new secret.
* Made indentation mistakes while modifying `dependencies/auth.py`.
* Caused a `return outside function` `SyntaxError`.
* Initially tried to test a custom JWT through Swagger's OAuth2 authorization dialog.
* Learned to use `curl` when Swagger could not directly provide the required custom token for testing.

## 💡 Interview Notes

* JWTs are signed, not encrypted.
* `sub` identifies the subject/user of the token.
* `exp` defines token expiration.
* Never hard-code production secrets in source code.
* Environment variables are commonly used for sensitive configuration.
* A valid JWT signature does not automatically mean every required claim exists.
* Required JWT claims should be validated before using them.
* Missing claims should result in controlled authentication errors rather than server crashes.
* Authentication verifies who the user is.
* Authorization determines what the authenticated user can access.
* Protected endpoints should never blindly trust client-supplied identity information.

## ⭐ Key Takeaways

* 🔐 Keep JWT secrets outside source code.
* 🔑 Use a strong random secret for signing tokens.
* ⏳ Always include token expiration.
* 👤 Require `sub` when creating access tokens.
* 🛡️ Validate required claims before using them.
* ❌ Never assume a JWT payload contains every expected field.
* 🚫 Invalid tokens should return `401 Unauthorized`, not crash the server.
* 🧪 Security features should be tested with both valid and intentionally invalid tokens.
* 🌱 Keep `.env` files out of Git.

## 📌 Summary

Hardened the JWT authentication system by moving JWT configuration into environment variables, replacing the placeholder secret with a random secret, requiring the `sub` claim during token creation, safely validating the `sub` claim during authentication, and testing both valid and malformed JWT scenarios.

## 🪞 Reflection

### What did I build today?

I improved the security of my existing JWT authentication system by separating secrets from source code and enforcing required JWT claims.

### What was the most important security lesson today?

A token being correctly signed does not mean the application should blindly trust every value inside its payload. Required claims must still be validated.

### What was the hardest bug today?

Fixing the indentation error in `dependencies/auth.py` that caused:

```text
SyntaxError: 'return' outside function
```

### If someone asked me to explain today's work without looking at the code, could I?

Yes. I can explain why JWT secrets should be stored in environment variables, what `sub` and `exp` represent, why required claims need validation, and how invalid JWTs are safely rejected.

```
```
