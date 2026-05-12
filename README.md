# 💬 CoolChat - REST APIs

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue.svg)

A complete full-stack social media web application featuring a Python Flask backend and a vanilla HTML/CSS/JS frontend. It provides complete RESTful APIs for authentication, posts, nested comments, likes, follows, user profiles, and image uploads.

---

## ✨ Features

- **Authentication**: Secure user signup, login, and session management.
- **Posts**: Create, view, and delete multimedia posts (with image uploads).
- **Engagement**: Like/unlike posts and nested commenting system.
- **Social Graph**: Follow and unfollow users, search for users.
- **Profiles**: Customizable user profiles with bio and profile picture URLs.
- **Optimized Frontend**: Separated HTML, CSS, and JS architecture for better caching and performance.

---

## 🏗️ Project Structure

```text
cool-chat/
├── backend/            # Flask application entry point
├── controllers/        # Request handlers and input validation
├── routes/             # API routing declarations
├── models/             # Database access and SQL queries
├── services/           # Reusable business logic layer
├── database/           # DB connections and schema dumps (`socialapp.sql`)
├── middleware/         # Custom Flask middleware
├── templates/          # Client-side frontend application
│   ├── html/           # HTML views (home, login, signup, profile)
│   ├── css/            # Stylesheets
│   └── js/             # Client-side JavaScript
├── config.py           # Application and database configuration
└── requirements.txt    # Python dependencies (in backend/)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL installed and running locally
- A PostgreSQL database named `socialapp`

### 1. Database Setup

Create the database and apply the initial schema:
```bash
psql -U your_postgres_user -d postgres -c "CREATE DATABASE socialapp;"
psql -U your_postgres_user -d socialapp -f database/socialapp.sql
```

Update your connection credentials in `config.py`:
```python
DB_HOST = "localhost"
DB_NAME = "socialapp"
DB_USER = "your_postgres_user"
DB_PASSWORD = "your_postgres_password"
DB_PORT = "5432"
```

### 2. Backend Setup

Install the required Python dependencies:
```bash
python3 -m pip install -r backend/requirements.txt
```

Run the Flask server:
```bash
python3 backend/app.py
```
*The backend API will start on `http://127.0.0.1:5000`.*

### 3. Frontend Setup

To serve the frontend static files and prevent CORS/routing issues, run a local web server from the project root:
```bash
python3 -m http.server 5500
```
*You can now access the application at `http://127.0.0.1:5500/templates/html/login.html`.*

---

## 📡 API Reference

### Authentication
- `POST /signup` - Register a new user
- `POST /login` - Authenticate an existing user

### Posts & Feed
- `GET /posts` - Retrieve the global feed
- `POST /create-post` - Create a new post with a caption and image
- `DELETE /delete-post/<postid>` - Delete a specific post

### Comments & Likes
- `POST /add-comment` - Comment on a post or reply to another comment
- `GET /get-comments/<postid>` - Fetch all comments for a post
- `POST /like-post` - Like a post
- `DELETE /unlike-post` - Remove a like from a post

### Social
- `POST /follow-user` - Follow another user
- `DELETE /unfollow-user` - Unfollow a user
- `GET /search-users` - Search the user directory

### Profiles & Media
- `PUT /update-profile` - Update profile details (bio, avatar, fullname)
- `POST /upload-image` - Upload an image (returns a hosted URL)

---

## 🛡️ Notes & Best Practices

- **CORS** is enabled globally for local development. Make sure to restrict origins before deploying to production.
- **Environment Variables**: Sensitive data is currently read from `config.py`. For a production environment, it is highly recommended to migrate these to a `.env` file to keep secrets out of version control.
