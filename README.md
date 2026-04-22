# LMSK Scraper API

A Flask-based REST API for managing Moodle LMS calendar events scraped from various sources.

## Getting Started

### Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended)

### Installation & Running
1. Clone the repository
2. Install dependencies and run the server:
   ```bash
   uv run main.py
   ```
   The server will start at `http://127.0.0.1:5000`.

## API Endpoints

### 1. General
- **GET `/`**
  - Description: Welcome message.
  - Response: `{"message": "Welcome to fasnet LMS Scraper.!"}`

### 2. Calendar Events

- **GET `/lmsk/calender`**
  - Description: Retrieve all calendar events.
  - Response: Array of Calendar objects.

- **GET `/lmsk/calender/<id>`**
  - Description: Retrieve a single calendar event by its database ID.
  - Response: Calendar object or 404 error.

- **POST `/lmsk/calender`**
  - Description: Create one or more calendar events.
  - Request Body: A single Calendar object OR a list of Calendar objects.
  - Response: The created object(s) with 201 status.

- **PUT `/lmsk/calender/<id>`**
  - Description: Update an existing calendar event.
  - Request Body: JSON with fields to update.
  - Response: The updated Calendar object.

- **DELETE `/lmsk/calender/<id>`**
  - Description: Delete a calendar event.
  - Response: Success message.

## Data Model

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer | Primary Key (auto-generated) |
| `uid` | String | Unique Identifier (required) |
| `summary` | String | Event title/summary |
| `description` | Text | Detailed description |
| `last_modified` | String | Timestamp of last modification |
| `dt_stamp` | String | Creation timestamp |
| `dt_start` | String | Event start time |
| `dt_end` | String | Event end time |
| `categories` | String | Event categories (e.g. Course name) |

## Database
The API uses SQLite (`lmsk.db`) stored in the `instance/` folder. The tables are automatically created on first run.