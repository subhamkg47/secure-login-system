# 🔐 Secure Login System

A security-focused authentication and file-access project built to demonstrate **authentication, authorization, secure file handling, database design, JWT security, account lockout, and Appwrite integration**.

The project supports two backend implementations behind the same frontend:

- **Custom REST backend** — FastAPI + PostgreSQL + SQLAlchemy
- **Appwrite implementation** — Appwrite Account + TablesDB + Storage + Functions

The supplied frontend can switch between **Mock**, **Custom REST**, and **Appwrite** modes.

---

## 🚀 Features

### Authentication

- User registration
- Secure bcrypt password hashing
- Email/password login
- JWT access tokens
- JWT expiration
- Required JWT `sub` claim
- Protected current-user endpoint
- Server-side JWT logout using token blacklisting
- Generic login errors
- Temporary account lockout after repeated failed attempts

### Authorization

- User-specific resource access
- File ownership validation
- Object-level authorization
- IDOR protection
- Cross-user access rejection
- Clear `401`, `403`, `404`, and `422` behavior

### File Security

- User-specific file listing
- Individual file access
- Ownership-checked downloads
- Local file storage for the Custom backend
- Appwrite Storage for the Appwrite implementation
- Appwrite Function for server-side file authorization
- Short-lived Appwrite download tokens

### Database & Backend

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic migrations
- Dependency injection
- CORS configuration
- Environment-based secrets

### Frontend

- Provided browser client
- Mock mode
- Custom REST mode
- Appwrite mode
- Shared API-style interface
- Appwrite adapter
- Browser file-download handling

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Custom API | FastAPI |
| Custom Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Password Security | bcrypt / Passlib |
| Authentication | JWT |
| Appwrite Auth | Appwrite Account |
| Appwrite Database | TablesDB |
| Appwrite Files | Storage |
| Appwrite Authorization | Functions |
| Server | Uvicorn |
| Version Control | Git |

---

## 📂 Project Structure

```text
secure-login-system/
│
├── backend/
│   ├── alembic/
│   │   └── versions/
│   ├── database/
│   │   └── database.py
│   ├── dependencies/
│   │   └── auth.py
│   ├── models/
│   │   ├── user.py
│   │   └── file.py
│   ├── routers/
│   │   ├── auth.py
│   │   └── files.py
│   ├── schemas/
│   │   ├── user.py
│   │   └── file.py
│   ├── services/
│   │   └── token_blacklist.py
│   ├── utils/
│   │   ├── jwt_handler.py
│   │   └── security.py
│   ├── uploads/
│   ├── main.py
│   ├── seed_files.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── index.html
│   ├── appwrite-adapter.js
│   ├── mock-api.js
│   ├── seed-data.json
│   ├── package.json
│   └── package-lock.json
│
├── function-src/
│   ├── src/
│   │   └── main.js
│   └── package.json
│
├── seed-appwrite.mjs
├── README.md
├── LEARNINGS.md
└── .gitignore
```

> `.env` and other secret configuration files should remain local and must not be committed.

---

# ⚙️ Custom FastAPI Backend

## 1. Create and activate the virtual environment

From the project root:

```bash
cd ~/Documents/secure-login-system

cd backend
python3 -m venv venv
source venv/bin/activate
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Configure environment variables

Create:

```text
backend/.env
```

Example structure:

```env
JWT_SECRET_KEY=<strong-random-secret>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=<token-lifetime>
DATABASE_URL=postgresql://<user>@localhost:5432/secure_login_db
```

Do not use real credentials from this repository in documentation or source control.

## 4. Start PostgreSQL

Make sure PostgreSQL is running and that the configured database exists.

## 5. Apply migrations

From:

```bash
cd backend
```

run:

```bash
alembic upgrade head
```

Check the current migration:

```bash
alembic current
```

## 6. Start FastAPI

```bash
uvicorn main:app --reload
```

The default development API URL is:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# 🔑 Custom REST API

The frontend uses the following API-style operations:

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/register` | Register a user |
| POST | `/login` | Login and receive an access token |
| POST | `/logout` | Blacklist the current JWT |
| GET | `/me` | Get the authenticated user |
| GET | `/files` | List files owned by the user |
| GET | `/files/{id}` | Get one authorized file |
| GET | `/files/{id}/download` | Download one authorized file |

### Authentication

After login, the client sends:

```http
Authorization: Bearer <access_token>
```

Protected endpoints authenticate the user through the reusable FastAPI authentication dependency.

---

# 🛡️ Security Model

The core security rule is:

```text
Authentication
      ↓
Identify current user
      ↓
Authorization
      ↓
Check ownership
      ↓
Return resource
```

For a file:

```text
file_id
   +
current_user.id
   ↓
ownership check
```

A file ID alone is never treated as proof of ownership.

### Expected authorization behavior

```text
Own file
  → 200 OK

Existing file owned by another user
  → 403 Forbidden

Nonexistent file
  → 404 Not Found

Invalid path parameter
  → 422 Unprocessable Entity
```

---

# 🔒 JWT Security

The Custom backend uses JWTs signed with HS256.

Important claims:

- `sub` — identifies the user
- `exp` — token expiration

The JWT secret is loaded from the environment.

Token creation requires a subject:

```python
if "sub" not in to_encode:
    raise ValueError("Token subject (sub) is required")
```

Authentication safely validates the subject before using it.

---

# 🚫 Login Lockout

The current account protection policy is:

```text
5 failed login attempts
        ↓
15-minute temporary lockout
```

The user's failed-attempt state is reset after successful authentication.

The database schema change is managed through Alembic.

---

# 🚪 Server-Side Logout

JWTs are normally stateless.

This project maintains an in-memory blacklist so that a logged-out JWT is rejected before protected routes are accessed.

```text
Login
  ↓
JWT
  ↓
Logout
  ↓
Blacklist token
  ↓
Same JWT used again
  ↓
401 Unauthorized
```

### Production consideration

The current blacklist is intentionally simple and in-memory.

A production implementation could use Redis or a persistent database-backed revocation system.

---

# 📦 Appwrite Implementation

The project also implements the application using Appwrite.

The frontend Appwrite adapter uses:

```text
Appwrite Account
Appwrite TablesDB
Appwrite Storage
Appwrite Functions
```

Configured resources include:

```text
Database: secure-login-db
Table: files
Bucket: secure-login-files
```

## Appwrite Authentication

Appwrite Account handles:

- Registration
- Login
- Logout
- Current-user lookup

## Appwrite File Metadata

TablesDB stores file metadata and ownership information.

Conceptually:

```text
File row
 ├── id
 ├── userId
 ├── filename
 └── storageFileId
```

## Appwrite Storage

The actual file content is stored in the Appwrite Storage bucket.

The database row and storage file are connected through the storage file ID.

---

# ⚡ Appwrite Function Authorization

The Appwrite Function provides the server-side authorization boundary for file operations.

The Function:

1. Receives the authenticated Appwrite user ID.
2. Creates a server-side Appwrite client using the dynamic function API key.
3. Retrieves the requested file row from TablesDB.
4. Checks the file owner.
5. Rejects cross-user access with `403`.
6. Creates a short-lived file token only after authorization succeeds.

The critical rule is:

```text
authenticated user ID == file row userId
```

If the ownership check fails:

```json
{
  "error": "You do not have permission to access this file"
}
```

with:

```text
403 Forbidden
```

---

# ⏱️ Temporary Appwrite Download URLs

Authorized Appwrite downloads use a temporary file token.

```text
Authenticated user
        ↓
Appwrite Function
        ↓
Find file row
        ↓
Verify ownership
        ↓
Create temporary file token
        ↓
Return downloadUrl
        ↓
Browser downloads file
```

The current Function creates the token with an approximately **5-minute expiration**.

Example response shape:

```json
{
  "id": "file_003",
  "fileName": "notes.pdf",
  "downloadUrl": "...",
  "expiresAt": "..."
}
```

Authorization happens **before** the download URL is generated.

---

# 🖥️ Frontend Backend Modes

The provided frontend supports:

```text
┌───────────────┐
│  Mock Mode    │
└───────────────┘

┌───────────────┐
│ Custom REST   │
└───────────────┘

┌───────────────┐
│ Appwrite      │
└───────────────┘
```

### Mock

Uses the local mock API and seed data.

Useful for testing the UI without a backend.

### Custom REST

Communicates with the FastAPI backend.

Default Base URL:

```text
http://127.0.0.1:8000
```

### Appwrite

`appwrite-adapter.js` communicates directly with Appwrite using the Web SDK while preserving the frontend's API-style interface.

This means the UI can continue using operations such as:

```text
POST /register
POST /login
POST /logout
GET /me
GET /files
GET /files/{id}
GET /files/{id}/download
```

without being tightly coupled to one backend implementation.

---

# 📥 Download Handling

The frontend handles the two download styles differently.

### Custom REST

```text
FastAPI
   ↓
Binary FileResponse
   ↓
Blob
   ↓
Browser download
```

### Appwrite / Mock

```text
Backend adapter
   ↓
JSON containing downloadUrl
   ↓
Browser navigates to URL
```

---

# 🌐 CORS

The FastAPI backend uses `CORSMiddleware` for the development frontend.

Allowed development origins include:

```text
http://localhost:5500
http://127.0.0.1:5500
```

The backend also exposes:

```text
Content-Disposition
```

for browser-based file handling.

CORS is a browser security mechanism; it is **not** a replacement for authentication or authorization.

---

# 🧪 Security Testing

The project was tested using:

- Swagger UI
- `curl`
- Frontend client
- Direct API requests
- Database/migration checks

## Authentication

Tested:

- Registration
- Valid login
- Invalid password
- Non-existent user
- Protected route without authentication
- Protected route with a valid token
- Invalid JWT
- JWT without `sub`
- Blacklisted JWT
- Account lockout

## Authorization

Tested:

- User accessing their own file
- User accessing another user's file
- Nonexistent file
- User downloading their own file
- User attempting to download another user's file

## Appwrite

Tested:

- User-specific file listing
- Authorized file access
- Cross-user file access rejection
- Authorized download URL creation
- Temporary download token
- Cross-user download rejection

---

# 🧠 Important Lessons

### Authentication ≠ Authorization

Authentication determines:

```text
Who is the user?
```

Authorization determines:

```text
What is that user allowed to access?
```

### Never trust an object ID

This is unsafe:

```text
GET /files/{id}
↓
Find file
↓
Return file
```

The secure flow is:

```text
GET /files/{id}
↓
Authenticate user
↓
Find file
↓
Check ownership
↓
Return file only if authorized
```

### JWTs are signed, not encrypted

The signature protects integrity and authenticity of the token, but it does not make its payload secret.

### CORS is not authorization

CORS controls which browser origins may make certain requests. It does not decide whether a user owns a resource.

### Temporary URLs should be protected

The Appwrite Function generates a download token only after checking ownership.

---

# 🧰 Useful Development Commands

### Activate backend environment

```bash
cd ~/Documents/secure-login-system/backend
source venv/bin/activate
```

### Run FastAPI

```bash
uvicorn main:app --reload
```

### Check migrations

```bash
alembic current
alembic history
```

### Apply migrations

```bash
alembic upgrade head
```

### Check Python imports

```bash
python3 -c "import main; print('main imported successfully')"
```

### Check Git state

```bash
cd ~/Documents/secure-login-system
git status --short
```

---

# 🔐 Repository & Secret Safety

Never commit:

```text
.env
.env.appwrite
API keys
JWT secrets
database passwords
personal credentials
venv/
node_modules/
temporary project archives
```

Before creating the final project ZIP, verify that secret configuration files are excluded or replaced with safe examples.

If an API key has been exposed outside the intended secret store, rotate it before final submission.

---

# 📚 Learning Notes

Detailed day-by-day learning notes are maintained separately in:

```text
LEARNINGS.md
```

That document contains the development journey, concepts learned, debugging mistakes, security decisions, testing strategy, and final project review.

---

# 👨‍💻 Author

**Shubham Kumar Gupta**

Computer Engineering student

GitHub: https://github.com/subhamkg47

This project was built as a hands-on learning project focused on secure backend development, authentication, authorization, and practical application security.
