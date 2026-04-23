# LMSK Scraper API

A modular, OOP-based Flask REST API for managing Moodle LMS data, including calendar events, courses, sections, and activities.

## Project Architecture

The project follows a modular structure to ensure separation of concerns and maintainability:

- **`main.py`**: Entry point. Orchestrates the Flask application using the `LMSKApi` class.
- **`models.py`**: Defines the SQLAlchemy database schema and relationships.
- **`repository.py`**: Implements the Repository Pattern, encapsulating all database operations and business logic.
- **`database.py`**: Holds the shared `SQLAlchemy` instance to avoid circular imports.

## Getting Started

### Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended)

### Installation & Running
1. Clone the repository.
2. Install dependencies and run the server:
   ```bash
   uv run main.py
   ```
   The server will start at `http://127.0.0.1:5000`.

## API Endpoints

### 1. General
- **GET `/`**: Welcome message.

### 2. Courses (with Nested Sections & Activities)
- **GET `/lmsk/course`**: Retrieve all courses.
- **GET `/lmsk/course/<id>`**: Retrieve a course by ID (includes nested sections and activities).
- **POST `/lmsk/course`**: Create one or more courses.
- **PUT `/lmsk/course/<id>`**: Update course details.
- **DELETE `/lmsk/course/<id>`**: Delete a course and all its related data (cascading).

### 3. Sections
- **GET `/lmsk/section`**: Retrieve all sections.
- **POST `/lmsk/section`**: Create a section linked to a `course_id`.

### 4. Activities
- **GET `/lmsk/activity`**: Retrieve all activities.
- **POST `/lmsk/activity`**: Create an activity linked to a `course_id` and `section_id`.

### 5. Calendar Events (ICS)
- **GET `/lmsk/calender`**: Retrieve all calendar events.
- **POST `/lmsk/calender`**: Create calendar events (checks for duplicate `uid`).

### 6. Timeline Events
- **GET `/lmsk/event`**: Retrieve all timeline events.
- **POST `/lmsk/event`**: Create timeline events.

### 7. Metadata
- **GET `/lmsk/metadata`**: Retrieve all scraping metadata.
- **POST `/lmsk/metadata`**: Save new scraping metadata.

## Data Models

### Metadata
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer | Primary Key |
| `scraped_at` | String | ISO timestamp of the scrape |
| `source` | String | Source URL of the data |

### Event (Timeline)
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer | Primary Key |
| `name` | String | Name of the event |
| `url` | String | Link to the event |
| `course_name`| String | Name of the course |
| `due_date` | String | Due date string |

### Calendar (ICS)
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer | Primary Key |
| `uid` | String | Unique Identifier (from ICS) |
| `summary` | String | Event summary |
| `description`| Text | Event description |
| `dt_start` | String | Start time |
| `dt_end` | String | End time |

### Course
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer | Primary Key |
| `name` | String | Short name (e.g., STAT 1213) |
| `full_name` | String | Detailed name |

### Section
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer | Primary Key |
| `course_id` | Integer | Foreign Key to Course |
| `title` | String | Section title |

### Activity
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer | Primary Key |
| `course_id` | Integer | Foreign Key to Course |
| `section_id` | Integer | Foreign Key to Section |
| `activity_name`| String | Name of the activity |
| `activity_type`| String | Type (resource, assignment, etc.) |
| `resource_url` | String | Moodle URL |

## Database
The API uses SQLite (`lmsk.db`) stored in the `instance/` folder. Relationships are configured with `cascade delete`, meaning deleting a course will automatically remove its sections and activities.