# 💬 CoolChat - REST APIs

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue.svg)

A complete full-stack social media web application featuring a Python Flask backend and a vanilla HTML/CSS/JS frontend. It provides RESTful APIs for authentication, posts, nested comments, likes, follows, follower counts, user profiles, and image uploads.

---

## ✨ Features

- **Authentication**: Secure user signup and login.
- **Posts**: Create, view, and delete multimedia posts with image uploads.
- **Engagement**: Like/unlike posts and nested commenting system.
- **Social Graph**: Follow and unfollow users; follower/following counts shown on profiles.
- **Profile Page**: View any user's profile with live follower count, following count, post count, and a Follow/Unfollow button that reflects current follow state.
- **Optimized Frontend**: Separated HTML, CSS, and JS architecture for better caching and performance.

---

## 🏗️ Project Structure

```text
cool-chat/
├── backend/            # Flask application entry point (app.py)
├── controllers/        # Request handlers and input validation
│   ├── auth_controller.py
│   ├── post_controller.py
│   ├── comment_controller.py
│   ├── like_controller.py
│   ├── follow_controller.py
│   └── user_controller.py
├── routes/             # API routing declarations
│   ├── auth_routes.py
│   ├── post_routes.py
│   ├── comment_routes.py
│   ├── like_routes.py
│   ├── follow_routes.py
│   ├── user_routes.py
│   └── upload_routes.py
├── models/             # Database access and SQL queries
├── services/           # Reusable business logic layer
├── database/           # DB connection helper and schema (socialapp.sql)
├── middleware/         # Custom Flask middleware
├── templates/          # Client-side frontend application
│   ├── html/           # HTML views (login, signup, home, profile)
│   ├── css/            # Stylesheets per page
│   └── js/             # Client-side JavaScript per page
├── config.py           # Application and database configuration
└── .env                # Environment variables (not committed)
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

Create a `.env` file in the project root with your credentials:
```env
DB_HOST=localhost
DB_NAME=socialapp
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
DB_PORT=5432
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

Serve the frontend from the project root to avoid CORS/path issues:
```bash
python3 -m http.server 5500
```
*Access the app at `http://127.0.0.1:5500/templates/html/login.html`.*

---

## 📡 API Reference

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/signup` | Register a new user |
| `POST` | `/login` | Authenticate an existing user |

### Posts & Feed
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/posts` | Retrieve the global feed |
| `POST` | `/create-post` | Create a new post with caption and image |
| `DELETE` | `/delete-post/<postid>` | Delete a specific post |

### Comments & Likes
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/add-comment` | Comment on a post or reply to a comment |
| `GET` | `/get-comments/<postid>` | Fetch all comments for a post |
| `POST` | `/like-post` | Like a post |
| `DELETE` | `/unlike-post` | Remove a like from a post |

### Social — Follow System
| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| `POST` | `/follow-user` | `{followerid, followeeid}` | Follow a user |
| `DELETE` | `/unfollow-user` | `{followerid, followeeid}` | Unfollow a user |
| `POST` | `/check-follow` | `{followerid, followeeid}` | Returns `{is_following: bool}` |
| `POST` | `/follower-count` | `{followeeid}` | Returns count of followers for a user |
| `POST` | `/following-count` | `{followerid}` | Returns count of users someone follows |

### Users & Media
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/user/<userid>` | Fetch a user's profile data |
| `PUT` | `/update-profile` | Update bio, avatar, fullname |
| `GET` | `/search-users` | Search the user directory |
| `POST` | `/upload-image` | Upload an image (returns hosted URL) |

---

## 🛡️ Notes & Best Practices

- **CORS** is enabled globally (`*`) for local development. Restrict origins before deploying to production.
- **Environment Variables**: Credentials are loaded from `.env` via `python-dotenv`. Never commit your `.env` file.
- **No auth tokens**: The current implementation trusts `userid` sent from the client. For production, add JWT-based authentication middleware.
