# Nooriam OA

Simple web app with **FastAPI** with following features:

- User registration & login
- JWT-based authentication
- Real-time notification
- Homepage using HTML + plain JS

Deployed here: https://madmage9999.github.io/nooriamoa/

DB hosted by Rails and backend hosted by Render. After the first request try again after 5-15 minutes as the backend server needs time to spin up after sleeping.

## Tech Stack

- Python 3.11+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- WebSockets
- HTML + JS


## How to Set Up Locally

### 1. Clone Repo

First clone repo to your desired location and enter the directory

```bash
git clone https://github.com/madmage9999/nooriamoa.git
cd nooriamo
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install PSQL and open DB 

Follow these instructions https://www.prisma.io/dataguide/postgresql/setting-up-a-local-postgresql-databaseto set up PSQL for your platform

### 5. Set Up Environment Variables

In the .env file add the database url.
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/yourdb
```
Make sure to replace user, password and yourdb with the credentials set up when opening the shell. By default it can be:
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/postgres
```

### 6. Run the App Locally

Run this command in root to run the backend:
```bash
uvicorn app.main:app --reload
```

Then open `static/index.html` from your preferred web browser to start viewing the app.

# How to test

1. Open two browser windows or tabs

2. Register a user in one tab

3. The other tab will receive a real-time WebSocket notification

4. Repeat with more browsers to see continuous updates of users registering

You can inspect localStorage to view the saved JWT token.

Unit tests can also be run with pytest


# Technical Discussion

## Technology Stack Decisions & Trade-offs

### Backend Framework: FastAPI
- **Pros:**
  - High performance due to async support
  - Built-in OpenAPI documentation
  - Modern, Pythonic API design
- **Trade-offs:**
  - Smaller ecosystem compared to Django/Flask
  - Less built-in functionality (auth, admin, etc)


### Database: PostgreSQL with asyncpg
- **Pros:**
  - Good performance and reliability
  - Scalable with larger dbs
- **Trade-offs:**
  - More complex setup than SQLite
  - Requires separate database server
  - Higher resource usage

### Authentication: JWT
- **Pros:**
  - Stateless authentication
  - Scalable across multiple servers
  - Client-side storage
- **Trade-offs:**
  - Cannot invalidate individual tokens
  - Token size adds overhead
  - Need to handle token refresh

### Real-time Updates: WebSockets
- **Pros:**
  - True bi-directional communication
  - Lower latency than polling
  - Native browser support
- **Trade-offs:**
  - Requires connection management
  - Issues with scaling

### Frontend: Plain HTML/JS
- **Pros:**
  - Simple to understand and maintain
  - No build process needed
  - Fast initial load
- **Trade-offs:**
  - Limited reusability
  - No component architecture
  - Manual state management