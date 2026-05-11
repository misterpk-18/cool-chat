# Cool Chat - REST APIs

A Flask + PostgreSQL backend for a social app with authentication, posts, comments, likes, follows, profile updates, and image uploads.

## Features

- User signup and login
- Create and fetch posts
- Add and fetch comments
- Like and unlike posts
- Follow and unfollow users
- Update user profile (`fullname`, `bio`, `profpicurl`)
- Upload images

## Tech Stack

- Python
- Flask
- Flask-CORS
- PostgreSQL

## Project Structure

```text
backend/          # Flask app entrypoint and Python dependencies
controllers/      # Request handlers
routes/           # API route declarations
models/           # Database queries and data access logic
services/         # Business logic helpers
database/         # DB connection and SQL schema
middleware/       # Middleware utilities
templates/        # Frontend HTML pages
config.py         # App/database config
```

## Prerequisites

- Python 3.10+
- PostgreSQL installed and running
- A PostgreSQL database named `socialapp`

## Setup

1. Clone the repository and open it:

```bash
git clone https://github.com/misterpk-18/cool-chat.git
cd cool-chat
```

2. Install dependencies:

```bash
python3 -m pip install -r backend/requirements.txt
```

3. Configure database connection in `config.py`:

```python
DB_HOST = "localhost"
DB_NAME = "socialapp"
DB_USER = "your_postgres_user"
DB_PASSWORD = "your_postgres_password"
DB_PORT = "5432"
```

4. Initialize database schema:

```bash
psql -U your_postgres_user -d socialapp -f database/socialapp.sql
```

## Run the Server

```bash
python3 backend/app.py
```

Server starts at:

`http://127.0.0.1:5000`

## API Endpoints

### Auth

- `POST /signup`
- `POST /login`

### Posts

- `GET /posts`
- `POST /create-post`
- `DELETE /delete-post/<postid>`

### Comments

- `POST /add-comment`
- `GET /get-comments/<postid>`

### Likes

- `POST /like-post`
- `DELETE /unlike-post`

### Follow

- `POST /follow-user`
- `DELETE /unfollow-user`

### User

- `PUT /update-profile`

### Upload

- `POST /upload-image`

## Notes

- CORS is enabled globally.
- Current config is read from `config.py`.
- Keep secrets out of git (use local environment configuration for production).
