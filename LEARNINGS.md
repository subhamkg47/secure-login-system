# 📚 Secure Login System — Learning Notes

> Personal revision notes for the Secure Login System project. These notes document what I built, what I learned, the security decisions I made, the mistakes I encountered, and the tests I completed.

---

# Day 1 — Project Setup

## 🎯 Objective

Set up a FastAPI backend, understand the project structure, run the application with Uvicorn, and use FastAPI's automatic API documentation.

## 🧠 Concepts Learned

- FastAPI is an ASGI framework for building APIs.
- Uvicorn is an ASGI server.
- A Python virtual environment isolates project dependencies.
- FastAPI automatically provides Swagger UI at `/docs`.
- A clean project structure separates routers, models, schemas, database code, utilities, and services.

## 💻 Commands

```bash
python3 -m venv venv
source venv/bin/activate
uvicorn main:app --reload
```

## 💡 Interview Notes

- ASGI allows Python web applications to communicate with asynchronous servers.
- Uvicorn runs the FastAPI application.
- Virtual environments prevent project dependency conflicts.

## 📌 Summary

Created and ran the initial FastAPI project and learned the basic backend structure.

---

# Day 2 — PostgreSQL & SQLAlchemy

## 🎯 Objective

Connect the application to PostgreSQL and learn how SQLAlchemy communicates with the database.

## 🧠 Concepts Learned

- PostgreSQL is a relational database.
- SQLAlchemy is an ORM.
- A model represents a database table.
- A session is used to communicate with the database.
- SQLAlchemy allows database records to be represented as Python objects.
- The project uses PostgreSQL for persistent user and file metadata.

## 🔄 Database Flow

```text
FastAPI
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

## 💡 Interview Notes

- ORM = Object Relational Mapper.
- SQLAlchemy converts Python ORM operations into SQL.
- Database sessions should be managed through dependency injection.

## 📌 Summary

Connected FastAPI to PostgreSQL through SQLAlchemy.

---

# Day 3 — User Registration

## 🎯 Objective

Build a registration endpoint that validates input, prevents duplicate emails, hashes passwords, and stores users in PostgreSQL.

## 🧠 Concepts Learned

- Pydantic schemas validate request bodies.
- `APIRouter` keeps endpoints modular.
- Duplicate accounts must be rejected.
- Passwords must never be stored in plaintext.
- SQLAlchemy is used to insert the new user.

## 🔄 Registration Flow

```text
Client
  ↓
POST /register
  ↓
Validate input
  ↓
Check existing email
  ↓
Hash password
  ↓
Store user
  ↓
Return success
```

## 💡 Interview Notes

- Validation belongs at the API boundary.
- Password hashing happens before persistence.
- A unique identity such as email must not be blindly accepted.

## 📌 Summary

Implemented secure user registration with PostgreSQL and password hashing.

---

# Day 4 — Password Hashing & Secure Login

## 🎯 Objective

Implement password verification and secure login.

## 🧠 Concepts Learned

### Password Hashing

The project uses bcrypt through Passlib.

```python
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
```

Passwords are hashed before storage:

```python
pwd_context.hash(password)
```

Passwords are verified against the stored hash:

```python
pwd_context.verify(plain_password, hashed_password)
```

### Why Hashing?

Password hashing is intentionally one-way. The application should verify a password rather than decrypt a stored password.

## 🔄 Login Flow

```text
Email + Password
      ↓
Find user
      ↓
Verify bcrypt hash
      ↓
Valid?
 ┌────┴────┐
No        Yes
 ↓          ↓
401       Continue
```

## ❌ Mistakes

- Encountered bcrypt version compatibility issues.
- Learned to pin compatible dependency versions.
- Fixed Python indentation and import errors.

## 💡 Interview Notes

- Hashing is not encryption.
- bcrypt uses a salt.
- The same password can produce different bcrypt hashes.
- Never compare plaintext passwords with stored hashes directly.

## 📌 Summary

Implemented secure password storage and password verification.

---

# Day 5 — JWT Authentication

## 🎯 Objective

Use JWTs to authenticate users after login.

## 🧠 Concepts Learned

A JWT contains:

```text
Header
Payload
Signature
```

Important claims in this project:

- `sub` — identifies the user.
- `exp` — specifies token expiration.

The project signs tokens using HS256.

## 🔄 Authentication Flow

```text
Login
  ↓
Verify password
  ↓
Create JWT
  ↓
Return access_token
  ↓
Client sends:
Authorization: Bearer <token>
  ↓
Server verifies JWT
  ↓
Protected endpoint
```

## 💡 Interview Notes

- JWTs are signed, not encrypted.
- `sub` identifies the token subject.
- `exp` limits token lifetime.
- The signing secret must remain private.
- Bearer tokens are normally sent through the `Authorization` header.

## 📌 Summary

Added JWT-based authentication to the login system.

---

# Day 6 — Dependency Injection & Reusable Authentication

## 🎯 Objective

Avoid repeating authentication logic in every protected route.

## 🧠 Concepts Learned

FastAPI's `Depends()` allows reusable dependencies.

The project uses:

```python
current_user = Depends(get_current_user)
```

The authentication dependency:

1. Extracts the bearer token.
2. Checks the blacklist.
3. Verifies the JWT.
4. Reads the `sub` claim.
5. Finds the corresponding user in PostgreSQL.
6. Returns the authenticated user.

## 💡 Interview Notes

Dependency injection improves:

- Reusability
- Separation of concerns
- Testability
- Maintainability

## 📌 Summary

Created reusable server-side authentication logic using FastAPI dependencies.

---

# Day 7 — Fetching the Current User

## 🎯 Objective

Do not trust user identity supplied by the client after authentication.

## 🧠 Concepts Learned

The JWT identifies the user, and the backend then queries PostgreSQL using that identity.

```text
JWT
 ↓
sub
 ↓
Find User
 ↓
current_user
```

The protected `/me` endpoint returns information about the authenticated user.

## 💡 Security Lesson

The client should not be allowed to say:

```text
"I am user 25"
```

and have the backend blindly trust it.

The backend derives the identity from the validated token.

## 📌 Summary

Connected JWT authentication to the actual database user.

---

# Day 8 — Server-Side JWT Logout

## 🎯 Objective

Invalidate a JWT after logout.

## 🧠 Problem

JWTs are normally stateless. Simply deleting a token from a frontend field does not automatically invalidate it on the server.

## 🛡️ Solution

The project uses a token blacklist:

```python
blacklisted_tokens = set()
```

Logout adds the token to the blacklist.

Protected routes check:

```text
Is token blacklisted?
      ↓
Yes → 401
No  → Continue
```

## ⚠️ Limitation

The current blacklist is in memory.

Therefore:

- It is lost when the backend restarts.
- It is suitable for the learning project.
- A production system could use PostgreSQL or Redis for persistent token revocation.

## 📌 Summary

Implemented server-side JWT logout using token blacklisting.

---

# Day 9 — File Model & Database Relationships

## 🎯 Objective

Connect uploaded file metadata to users.

## 🧠 Concepts Learned

The `File` model contains:

```text
id
filename
filepath
user_id
```

`user_id` is a foreign key to the users table.

Conceptually:

```text
One User
   │
   ├── File
   ├── File
   └── File
```

This is a one-to-many relationship.

## 🔐 Why Ownership Matters

Every file must have an owner.

The backend must use:

```text
file.user_id
```

together with:

```text
current_user.id
```

when authorizing access.

## 📌 Summary

Created the file model and connected files to users through a foreign key.

---

# Day 10 — Secure File Access & Authorization

## 🎯 Objective

Ensure users can only access files belonging to their own account.

## 🧠 Authentication vs Authorization

Authentication asks:

> Who are you?

Authorization asks:

> What are you allowed to access?

In this project:

```text
JWT
 ↓
Authentication
 ↓
current_user
 ↓
Authorization
 ↓
File ownership check
```

## 🔐 User-Specific File Listing

The backend filters the file list using the authenticated user's ID:

```python
db.query(File).filter(
    File.user_id == current_user.id
).all()
```

The frontend does not perform the security filtering.

## 🛡️ IDOR / Object-Level Authorization

A client knowing another user's file ID must not be enough to access that file.

The backend checks:

```python
if file.user_id != current_user.id:
    raise HTTPException(
        status_code=403,
        detail="You do not have permission to access this file"
    )
```

## 403 vs 404

```text
File does not exist
        ↓
404 Not Found

File exists but belongs to another user
        ↓
403 Forbidden
```

## 💡 Interview Notes

- Never treat an object ID as proof of ownership.
- Authorization must happen on the backend.
- IDOR is an object-level authorization problem.
- Every protected resource needs an ownership/access check.

## 📌 Summary

Implemented user-specific file listing, single-file authorization, IDOR protection, and clear 403/404 behavior.

---

# Day 11 — File Storage & Secure Downloads

## 🎯 Objective

Store actual files on the server and securely download them.

## 🧠 Concepts Learned

The project separates:

```text
Database
  ↓
File metadata

uploads/
  ↓
Actual file content
```

The database stores the filename and ownership information. The physical file is stored in `backend/uploads/`.

## 📥 Download Flow

```text
GET /files/{file_id}/download
          ↓
Authenticate user
          ↓
Find file
          ↓
Check ownership
          ↓
Check physical file exists
          ↓
FileResponse
```

The backend uses FastAPI's `FileResponse`.

## 🧪 Expected Results

```text
Own file                  → 200
Other user's file         → 403
Unknown file              → 404
Missing physical content  → 404
```

## 💡 Important Lesson

A `.pdf` filename does not make a file a valid PDF. File contents should be verified when creating test data.

## 📌 Summary

Implemented secure server-side file downloads with ownership checks and physical file validation.

---

# Day 12 — Login Lockout & Alembic

## 🎯 Objective

Protect accounts against repeated failed login attempts and learn safe database schema migrations.

## 🔒 Brute-Force Protection

The current policy is:

```text
5 failed attempts
        ↓
15-minute lockout
```

The `User` model tracks:

```python
failed_attempts
locked_until
```

Before login, the backend checks whether the account is locked.

After a failed password:

```text
failed_attempts += 1
```

After five failures:

```text
locked_until = now + 15 minutes
```

After successful login:

```python
failed_attempts = 0
locked_until = None
```

## 🗃️ Alembic

Changing a SQLAlchemy model does not automatically change an existing PostgreSQL database.

Alembic manages schema changes.

The project contains an Alembic migration for the login lockout fields.

Useful commands:

```bash
alembic current
alembic history
alembic upgrade head
```

The verified migration state is:

```text
363b9a5c9ef2 (head)
```

## 💡 Interview Notes

- Database schema changes should be version controlled.
- Alembic migrations provide repeatable schema changes.
- Account lockout reduces repeated password guessing.
- Successful authentication resets failed-attempt state.

## 📌 Summary

Implemented temporary account lockout and managed the corresponding PostgreSQL schema with Alembic.

---

# Day 13 — JWT Security Hardening & Environment Configuration

## 🎯 Objective

Remove sensitive JWT configuration from source code and enforce safe JWT validation.

## 🌱 Environment Variables

The project loads:

```text
JWT_SECRET_KEY
JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
```

from environment configuration.

The application refuses to start without a JWT secret.

## 🔑 Required JWT Subject

Token creation requires `sub`:

```python
if "sub" not in to_encode:
    raise ValueError("Token subject (sub) is required")
```

This prevents creation of tokens that cannot identify a user.

## 🛡️ Safe Validation

The authentication dependency uses:

```python
email = payload.get("sub")

if not email:
    raise HTTPException(
        status_code=401,
        detail="Invalid token"
    )
```

This avoids blindly indexing a missing claim.

## 🧪 Security Tests

Tested:

- Valid JWT.
- Token without `sub`.
- Token creation without `sub`.
- Expiration/invalid token handling.

## 💡 Security Lessons

- JWT secrets must not be hard-coded.
- `.env` files must not be committed.
- A correctly signed JWT can still contain an invalid application-level payload.
- Required claims must be explicitly validated.
- Invalid authentication data should result in controlled `401` responses rather than server crashes.

## 📌 Summary

Hardened JWT creation and validation and moved sensitive configuration into environment variables.

---

# Day 14 — Complete Custom Backend Security

## 🎯 Objective

Bring authentication, authorization, file security, and frontend integration together into a complete Custom REST implementation.

## ✅ Custom Backend Features

- User registration
- Password hashing
- Login
- JWT access tokens
- JWT expiration
- JWT subject validation
- Reusable authentication dependency
- Protected `/me`
- Server-side logout
- Token blacklist
- Generic login errors
- Login lockout
- PostgreSQL persistence
- Alembic migration
- User-specific file listing
- Individual file authorization
- IDOR protection
- 403/404 handling
- Secure file downloads
- CORS

## 🔄 Complete Custom Flow

```text
Register
   ↓
Hash password
   ↓
PostgreSQL

Login
   ↓
Verify password
   ↓
Check lockout
   ↓
Create JWT
   ↓
Client stores bearer token

Protected request
   ↓
Extract token
   ↓
Blacklist check
   ↓
JWT verification
   ↓
Validate sub
   ↓
Find database user
   ↓
Authorization check
   ↓
Return resource
```

## 🧪 Security Tests Completed

The project was manually tested for:

```text
Registration                         PASS
Login                               PASS
Protected profile                   PASS
Logout                              PASS
Blacklisted token rejection         PASS
Generic login errors                PASS
Login lockout                       PASS
User-specific file listing          PASS
Own file access                     PASS
Cross-user file access              PASS
Nonexistent file                    PASS
Own file download                   PASS
Cross-user download                 PASS
CORS preflight                      PASS
CORS authenticated download         PASS
```

## 📌 Summary

The Custom FastAPI + PostgreSQL implementation satisfies the core authentication, authorization, file access, and security requirements of the project.

---

# Day 15 — Appwrite Implementation

## 🎯 Objective

Implement the same application flow using Appwrite services and connect the provided frontend to Appwrite through a dedicated adapter.

## 🧠 Architecture

The Appwrite implementation uses:

```text
Frontend
   │
   ├── Appwrite Account
   ├── Appwrite TablesDB
   ├── Appwrite Storage
   └── Appwrite Functions
```

The frontend does not need a completely separate GUI.

`appwrite-adapter.js` intercepts the frontend's `fetch()` calls and maps the existing API-style operations to Appwrite.

## 🔌 Appwrite Resources

The project is configured around:

```text
Endpoint:
https://sgp.cloud.appwrite.io/v1

Database:
secure-login-db

Table:
files

Storage bucket:
secure-login-files
```

The Appwrite project ID is configured in the frontend adapter.

## 🔐 Appwrite Authentication

The adapter uses:

```javascript
new Appwrite.Account(appwriteClient)
```

Registration uses Appwrite account creation.

Login uses an email/password session.

Logout deletes the current Appwrite session.

The current user is retrieved with:

```javascript
account.get()
```

## 🔄 Appwrite Authentication Flow

```text
Register
   ↓
Appwrite Account

Login
   ↓
Email/password session
   ↓
Appwrite session

GET /me
   ↓
account.get()

Logout
   ↓
deleteSession("current")
```

## 🗄️ Appwrite TablesDB

The Appwrite implementation uses `TablesDB` for file metadata.

The frontend adapter reads file rows and maps them to the API format:

```text
id
ownerId
fileName
storageFileId
```

## 📂 Appwrite Storage

The actual file content is stored in an Appwrite Storage bucket.

The project keeps:

```text
Database row
      +
Storage file
```

connected through the storage file ID.

## 🧩 Why an Appwrite Function?

The browser should not be trusted to decide whether a user owns a file.

The Appwrite Function receives a file ID and:

1. Gets the authenticated Appwrite user.
2. Gets the dynamic function API key.
3. Looks up the database row.
4. Checks the row owner.
5. Rejects unauthorized access.
6. Creates a short-lived file token for authorized downloads.

## 🔐 Appwrite File Authorization

The Function performs:

```javascript
if (row.userId !== userId) {
    return res.json(
        {
            error: "You do not have permission to access this file"
        },
        403
    );
}
```

Therefore:

```text
User A + User A file → allowed
User B + User A file → 403
```

## ⏱️ Temporary Download Tokens

Authorized Appwrite downloads use a short-lived file token.

The current implementation creates a token with an expiration approximately five minutes in the future.

The resulting download URL contains:

```text
bucket
file
project
temporary token
```

The frontend can then navigate to the generated URL.

## 🔄 Appwrite File Flow

```text
GET /files/{id}
        ↓
Appwrite Function
        ↓
Get current user
        ↓
Get database row
        ↓
Check owner
        ↓
Return metadata
```

Download:

```text
GET /files/{id}/download
        ↓
Appwrite Function
        ↓
Check owner
        ↓
Create temporary file token
        ↓
Return downloadUrl
        ↓
Browser downloads file
```

## 🧪 Appwrite Tests Completed

The Appwrite implementation was tested for:

```text
User-specific file listing          PASS
Own file access                     PASS
Cross-user file access              PASS
Own file download URL               PASS
Cross-user download                 PASS
Temporary download token            PASS
```

A valid Appwrite download response contains:

```json
{
  "id": "file_003",
  "fileName": "notes.pdf",
  "downloadUrl": "...",
  "expiresAt": "..."
}
```

A cross-user request returns:

```json
{
  "error": "You do not have permission to access this file"
}
```

with HTTP `403`.

## 📌 Summary

Implemented Appwrite Account, TablesDB, Storage, and Functions integration while preserving the existing frontend API interface.

---

# Day 16 — Frontend Backend Abstraction

## 🎯 Objective

Allow the same provided frontend to work with Mock, Custom REST, and Appwrite modes.

## 🧠 Concepts Learned

The frontend supports three modes:

```text
Mock
Custom REST
Appwrite
```

The backend mode is selected through radio buttons.

## 🔄 Request Abstraction

The frontend uses:

```javascript
request(path, options)
```

The Appwrite adapter overrides `window.fetch` when Appwrite mode is selected.

Therefore existing frontend code can continue using API-style calls such as:

```text
POST /register
POST /login
POST /logout
GET /me
GET /files
GET /files/{id}
GET /files/{id}/download
```

without the UI needing to know every Appwrite SDK detail.

## 📥 Download Handling

The frontend handles the difference between backends:

```text
Mock/Appwrite
      ↓
JSON downloadUrl
      ↓
Navigate to URL

Custom REST
      ↓
Binary file response
      ↓
Blob
      ↓
Temporary browser URL
      ↓
Download
```

## 💡 Design Lesson

A stable frontend API contract makes it possible to swap backend implementations without rewriting the user interface.

## 📌 Summary

Built a frontend adapter layer that allows the supplied client to communicate with both the Custom REST backend and Appwrite.

---

# Day 17 — CORS & Browser Integration

## 🎯 Objective

Allow the browser-hosted frontend to communicate with the local FastAPI backend.

## 🧠 Problem

Browsers enforce the same-origin policy.

The frontend and backend may run on different origins, for example:

```text
Frontend
http://localhost:5500

Backend
http://127.0.0.1:8000
```

The backend therefore needs CORS configuration.

## 🛠️ FastAPI Configuration

The backend uses `CORSMiddleware` and allows the development frontend origins:

```text
http://localhost:5500
http://127.0.0.1:5500
```

It also exposes:

```text
Content-Disposition
```

so browser code can access the download-related response header when required.

## 🧪 CORS Testing

The project was tested with:

```text
OPTIONS preflight
GET with Origin
GET with Authorization
```

The backend returned the expected CORS headers.

## 📌 Summary

Configured and tested CORS so the supplied browser client can communicate with the local Custom REST backend.

---

# Day 18 — Security Testing & Debugging Lessons

## 🎯 Objective

Learn how to isolate backend, frontend, authentication, authorization, and browser problems instead of changing working code blindly.

## 🧪 Useful Testing Strategy

When debugging an API:

```text
1. Test endpoint directly with curl
2. Check HTTP status
3. Check response body
4. Check headers
5. Test authentication
6. Test authorization
7. Test browser/frontend
```

This helped distinguish:

```text
401 → authentication problem
403 → authorization problem
404 → resource problem
422 → request/path validation problem
200 → successful request
```

## Example: File ID Types

The project has two different backend implementations.

### Custom FastAPI

The SQLAlchemy file ID is an integer:

```text
/files/1
/files/1/download
```

### Appwrite

The Appwrite file ID is a string:

```text
/files/file_001
/files/file_001/download
```

Therefore a Custom FastAPI request such as:

```text
/files/file_001/download
```

produces a `422` validation error because the Custom route declares:

```python
file_id: int
```

This is not an authorization failure; it is request parameter validation.

## 💡 Debugging Lesson

Do not change working backend code just because two implementations use different identifiers.

Always identify:

```text
Which backend?
Which route?
Which ID format?
Which authentication mechanism?
```

before changing code.

---

# Day 19 — Environment & Repository Security

## 🎯 Objective

Keep secrets and machine-specific files outside the repository.

## 🔐 Sensitive Configuration

The Custom backend uses environment variables for:

```text
JWT_SECRET_KEY
JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
DATABASE_URL
```

The Appwrite seed/function configuration also requires sensitive API credentials.

## 🚫 Never Commit

Do not commit:

```text
.env
.env.appwrite
API keys
JWT secrets
database passwords
personal credentials
venv/
node_modules/
temporary archives
```

The repository `.gitignore` should protect environment files.

## ⚠️ Important Lesson

A secret appearing in a local `.env` file is different from a secret being committed to Git, but a secret that has already been exposed outside the local machine should be rotated.

## 📌 Summary

Learned to separate source code from sensitive configuration and to inspect Git status before committing.

---

# Day 20 — Final Project Review

## 🎯 Objective

Review the complete system as an authentication and authorization project rather than as a collection of individual endpoints.

## 🏗️ Final Architecture

```text
                    ┌──────────────────────┐
                    │   Provided Frontend  │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
          Custom REST                    Appwrite
                 │                           │
        ┌────────┴────────┐          ┌───────┴────────┐
        │                 │          │                │
     FastAPI          PostgreSQL   Account         TablesDB
        │                            │                │
     JWT/Auth                     Storage          Function
        │                                             │
     uploads/                                  ownership check
                                                     │
                                              temporary token
```

## ✅ Final Functional Areas

### Authentication

- Registration
- Login
- Password hashing
- JWT authentication
- JWT expiration
- JWT subject validation
- Protected current-user endpoint
- Logout
- Token blacklist
- Generic login errors
- Login lockout

### Authorization

- User-specific data
- File ownership checks
- Object-level authorization
- IDOR protection
- Cross-user access rejection
- 403/404 distinction

### File Security

- File metadata
- Local file storage
- Secure FileResponse downloads
- Appwrite Storage
- Appwrite Function authorization
- Temporary Appwrite download tokens

### Infrastructure

- PostgreSQL
- SQLAlchemy
- Alembic
- FastAPI
- Appwrite
- CORS
- Environment configuration
- Git

### Frontend

- Provided test client
- Mock mode
- Custom REST mode
- Appwrite mode
- Shared API-style interface
- Backend adapter
- Browser download handling

## 🎓 Main Security Lessons

1. Authentication and authorization are different.
2. Never trust client-supplied object IDs as proof of ownership.
3. Always authorize access on the backend.
4. Passwords must be hashed.
5. JWTs must be validated, not merely decoded.
6. Required claims such as `sub` must be checked.
7. JWT secrets must remain outside source code.
8. Logout for stateless tokens requires a revocation strategy when immediate invalidation is required.
9. Short-lived download tokens reduce the lifetime of sensitive file URLs.
10. CORS controls browser access; it is not an authorization mechanism.
11. Different backend implementations can legitimately use different resource ID formats.
12. Direct API testing with `curl` is useful for separating backend problems from frontend problems.

## 💼 Interview Explanation

If asked to explain the project:

> I built a secure authentication and file-access system using FastAPI, PostgreSQL, SQLAlchemy, JWT and bcrypt. I implemented registration, login, protected routes, JWT validation, server-side logout using token blacklisting, account lockout, and object-level authorization for files. I then implemented an equivalent Appwrite architecture using Account, TablesDB, Storage and Functions. The Appwrite Function performs server-side ownership checks and creates short-lived file tokens for authorized downloads. Finally, I connected the supplied frontend to both implementations through a backend adapter and tested cross-user access and download behavior.

## 📌 Final Takeaway

The biggest lesson from this project is that a secure application is not created by authentication alone.

A secure flow is:

```text
Identify the user
       ↓
Validate the authentication token
       ↓
Load trusted server-side identity
       ↓
Check authorization for the requested resource
       ↓
Return only what the user is allowed to access
```

For files:

```text
Authenticated user
       ↓
Requested file
       ↓
Does the file exist?
       ↓
Does the user own it?
       ↓
Does the content exist?
       ↓
Return file / temporary authorized URL
```

---

# 📋 Final Project Checklist

## Custom FastAPI

- [x] FastAPI application
- [x] PostgreSQL connection
- [x] SQLAlchemy ORM
- [x] User model
- [x] File model
- [x] Registration
- [x] bcrypt password hashing
- [x] Login
- [x] JWT access tokens
- [x] JWT expiration
- [x] Required `sub` claim
- [x] Protected `/me`
- [x] JWT blacklist
- [x] Logout
- [x] Generic login errors
- [x] Login lockout
- [x] Alembic migration
- [x] User-specific file listing
- [x] File ownership authorization
- [x] IDOR protection
- [x] 403/404 handling
- [x] Secure downloads
- [x] CORS

## Appwrite

- [x] Appwrite Account
- [x] Appwrite TablesDB
- [x] Appwrite Storage
- [x] Appwrite Function
- [x] Authenticated user lookup
- [x] File ownership check
- [x] Cross-user access protection
- [x] Temporary download tokens
- [x] Frontend adapter

## Testing

- [x] Registration
- [x] Login
- [x] Protected endpoint
- [x] Logout
- [x] Blacklisted JWT
- [x] Login lockout
- [x] Own file access
- [x] Cross-user file access
- [x] Nonexistent file
- [x] Own file download
- [x] Cross-user download
- [x] CORS
- [x] Appwrite file authorization
- [x] Appwrite download URL
- [x] Invalid file-ID format behavior

---

# 🧭 Next Steps

The implementation and testing phases are complete.

The remaining project work is documentation and repository hygiene:

1. Update `README.md` to describe the completed system.
2. Remove or redact any credentials from documentation.
3. Ensure `.env` and Appwrite secrets are excluded from Git.
4. Review `git diff`.
5. Create the final clean repository archive without secrets.
6. Make the final Git commit.
