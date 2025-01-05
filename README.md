# Real-Time Chat Application

A real-time chat application built using **FastAPI**, **WebSockets**, and **PostgreSQL**. This project demonstrates the use of WebSockets for real-time communication and incorporates features like user authentication, chat rooms, and persistent message storage.

## Features

- User registration and authentication
- Multiple chat rooms
- Real-time messaging using WebSockets
- Persistent message storage in a PostgreSQL database
- Responsive frontend with **HTML**, **CSS**, and **JavaScript**

## Project Structure

```plaintext
chat-app/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── auth.py
│   ├── websocket.py
│   └── templates/
│       ├── index.html
│   └── static/
│       ├── style.css
│       └── script.js
├── requirements.txt
├── .env
```

### Explanation of Key Directories and Files

- **`main.py`**: Entry point for the application. Sets up the routes, static files, and WebSocket endpoints.
- **`models.py`**: Defines the database models for users, chat rooms, and messages.
- **`schemas.py`**: Contains Pydantic schemas for data validation.
- **`database.py`**: Configures the PostgreSQL database connection using SQLAlchemy.
- **`auth.py`**: Handles user authentication and registration.
- **`websocket.py`**: Manages WebSocket connections and real-time messaging.
- **`templates/`**: Contains HTML templates for the frontend.
- **`static/`**: Stores CSS and JavaScript files.

---

## Prerequisites

Before starting, make sure you have:

- **Python 3.9+**
- **PostgreSQL**
- **Node.js** (optional, if you want to extend frontend capabilities)

---

## Installation and Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/lunatic-bot/chat-app.git
   cd chat-app

   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt

   ```

4. **Set Up the Database**

   - Create a PostgreSQL database.
   - Update the .env file with your database credentials:

   ```bash
   DATABASE_URL=postgresql://user:password@localhost/chat_db
   ```

5. **Run the application**

   ```bash
   uvicorn app.main:app --reload

   ```

6. **Access the Application Open your browser and navigate to http://127.0.0.1:8000.**

## Technologies Used

- **FastAPI**: Backend framework for building APIs and handling WebSockets.
- **SQLAlchemy**: ORM for database interaction.
- **PostgreSQL**: Database for storing user and chat data.
- **HTML, CSS, JavaScript**: Frontend for the chat interface.
- **WebSockets**: For real-time, bi-directional communication.

## Future Improvements

- User authentication with OAuth2.
- Adding private messaging between users.
- Advanced chat features like file sharing and emojis.
- Deploying the application using Docker.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.

## Contact

For any queries or feedback, feel free to reach out via atalbajpai771@gmail.com.
