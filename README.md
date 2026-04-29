# Payment App REST API

Async REST API for managing users, accounts and payment top-ups.

## Stack

- FastAPI
- PostgreSQL
- SQLAlchemy Async
- Alembic
- Docker Compose
- JWT authentication

## Features

### User

- Login by email/password
- Get profile
- Get accounts and balances
- Get payments

### Admin

- Login by email/password
- Get profile
- Create, update and delete users
- Get users with their accounts and balances

### Payments

- Webhook endpoint for payment top-ups
- SHA256 signature verification
- Unique transaction processing
- Automatic account creation if needed

---

## Environment Variables

Create a `.env` file in the project root.

For running the app inside Docker:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=payment_app

PAYMENT_SECRET_KEY=your_secret_key
JWT_SECRET=your_jwt_secret
```

For running Alembic locally against Docker PostgreSQL, temporarily use:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5444
```

---

## Run with Docker Compose

Start PostgreSQL:

```bash
docker compose up -d db
```

Run migrations:

```bash
alembic upgrade head
```

Then set `.env` back to Docker mode:

```env
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

Start the application:

```bash
docker compose up --build
```

Interactive API docs:

```text
http://localhost:8000/docs
```

---

## Run Locally (PostgreSQL in Docker)

Start PostgreSQL:

```bash
docker compose up -d db
```

Use local database connection in `.env`:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5444
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
alembic upgrade head
```

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

Interactive API docs:

```text
http://localhost:8000/docs
```

---

## Default Credentials

### Admin

```text
email: admin@example.com
password: 123456
```

### User

```text
email: user@example.com
password: 123456
```

---

## API Prefix

All endpoints are available under:

```text
/api/v1
```

Examples:

```text
POST /api/v1/auth/user/login
POST /api/v1/auth/admin/login
GET  /api/v1/users/me
GET  /api/v1/admins/users
POST /api/v1/payments/webhook
```

---

## Payment Webhook Signature

Signature is generated using SHA256 from concatenated values in alphabetical key order plus secret key:

```text
{account_id}{amount}{transaction_id}{user_id}{secret_key}
```

Example endpoint:

```text
POST /api/v1/payments/webhook
```