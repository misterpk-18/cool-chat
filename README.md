# 💬 CoolChat - REST APIs

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue.svg)
![Socket.IO](https://img.shields.io/badge/Socket.IO-4.x-black.svg)

A complete full-stack social media web application featuring a Python Flask backend and a vanilla HTML/CSS/JS frontend. It provides RESTful APIs and real-time Socket.IO events for authentication, posts, comments, likes, follows, messaging, user profiles, and image uploads.

---

## ✨ Features

- **Authentication**: Secure user signup and login.
- **Posts**: Create, view, and delete multimedia posts with image uploads.
- **Engagement**: Like/unlike posts and nested commenting system.
- **Social Graph**: Follow and unfollow users; follower/following counts shown on profiles.
- **Profile Page**: View any user's profile with live follower count, following count, post count, and a Follow/Unfollow button that reflects current follow state.
- **Real-time Messaging**: DM and group chat powered by Socket.IO — with typing indicators, seen receipts, and live message delivery.
- **Optimized Frontend**: Separated HTML, CSS, and JS architecture for better caching and performance.

---

## 🏗️ Project Structure

```text
cool-chat/
├── backend/
│   ├── app.py              # Flask + Socket.IO entry point
│   └── socket_events.py    # Socket.IO event handlers
├── controllers/            # Request handlers and input validation
│   ├── auth_controller.py
│   ├── post_controller.py
│   ├── comment_controller.py
│   ├── like_controller.py
│   ├── follow_controller.py
│   ├── user_controller.py
│   └── message_controller.py
├── routes/                 # API routing declarations
│   ├── auth_routes.py
│   ├── post_routes.py
│   ├── comment_routes.py
│   ├── like_routes.py
│   ├── follow_routes.py
│   ├── user_routes.py
│   ├── upload_routes.py
│   └── message_routes.py
├── models/                 # Database access and SQL queries
│   ├── message_model.py
│   └── follow_model.py
├── services/               # Reusable business logic layer
├── database/               # DB connection helper and schema (socialapp.sql)
├── middleware/             # Custom Flask middleware
├── templates/              # Client-side frontend application
│   ├── html/               # HTML views (login, signup, home, profile, messages)
│   ├── css/                # Stylesheets per page
│   └── js/                 # Client-side JavaScript per page
├── config.py               # Application and database configuration
└── .env                    # Environment variables (not committed)
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

Run the Flask + Socket.IO server:
```bash
python3 backend/app.py
```
*The backend API and WebSocket server will start on `http://127.0.0.1:5000`.*

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
| `POST` | `/follower-count` | `{followeeid}` | Returns follower count for a user |
| `POST` | `/following-count` | `{followerid}` | Returns following count for a user |

### Messaging (REST)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/conversations/create` | Create a DM or group conversation |
| `GET` | `/conversations/<userid>` | Get all conversations for a user |
| `GET` | `/conversations/<id>/messages` | Fetch message history for a conversation |
| `GET` | `/conversations/<id>/members` | Get members of a conversation |
| `POST` | `/conversations/send` | Send a message (REST fallback) |
| `PUT` | `/conversations/seen` | Mark messages as seen |
| `POST` | `/conversations/add-member` | Add a member to a group |

### Users & Media
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/user/<userid>` | Fetch a user's profile data |
| `PUT` | `/update-profile` | Update bio, avatar, fullname |
| `GET` | `/search-users` | Search the user directory |
| `POST` | `/upload-image` | Upload an image (returns hosted URL) |

---

## ⚡ Socket.IO Events

The server uses **Flask-SocketIO** with `eventlet` for real-time communication.

### Client → Server
| Event | Payload | Description |
|-------|---------|-------------|
| `join_conversation` | `{conversation_id, user_id}` | Join a chat room and mark messages seen |
| `leave_conversation` | `{conversation_id, user_id}` | Leave a chat room |
| `send_message` | `{conversation_id, sender_id, content, media_url?}` | Send a real-time message |
| `typing` | `{conversation_id, user_id, username}` | Broadcast typing indicator |
| `stop_typing` | `{conversation_id, user_id}` | Stop typing indicator |
| `message_seen` | `{conversation_id, user_id}` | Mark messages as seen |

### Server → Client
| Event | Payload | Description |
|-------|---------|-------------|
| `connected` | `{message}` | Fired on successful connection |
| `joined` | `{conversation_id, user_id}` | Confirms room join |
| `left` | `{conversation_id, user_id}` | Confirms room leave |
| `new_message` | `{message_id, conversation_id, sender_id, username, content, media_url, created_at}` | Broadcasts a new message to the room |
| `user_typing` | `{user_id, username}` | Notifies others of typing |
| `user_stop_typing` | `{user_id}` | Notifies others typing stopped |
| `seen_update` | `{conversation_id, user_id}` | Notifies others messages were seen |

---

## 🛡️ Notes & Best Practices

- **CORS** is enabled globally (`*`) for local development. Restrict origins before deploying to production.
- **Environment Variables**: Credentials are loaded from `.env` via `python-dotenv`. Never commit your `.env` file.
- **No auth tokens**: The current implementation trusts `userid` sent from the client. For production, add JWT-based authentication middleware.
- **Socket.IO**: Uses `eventlet` as the async driver. If you see deprecation warnings, `threading` mode is a no-dependency alternative.
