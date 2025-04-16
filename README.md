ToDo Full Stack App (React + FastAPI)

Overview:
A simple full-stack app to manage to-do tasks using FastAPI for the backend and React for the frontend.

Features:
Add, update, delete todos

Filter by completed/pending

SQLite backend via SQLAlchemy

API Endpoints (FastAPI)
1. GET /todos

Description: Retrieves all todo items.

Request Body: None

Response: Returns a list of all todo objects.

2. POST /todos

Description: Creates a new todo item.

Request Body: JSON with the following fields:

title: string (required)

description: string (optional)

Response: Returns the created todo object.

3. PUT /todos/{id}

Description: Updates an existing todo by its ID.

Request Body: JSON with any of the following fields to update:

title

description

completed

Response: Returns the updated todo object.

4. DELETE /todos/{id}

Description: Deletes the todo with the specified ID.

Request Body: None

Response: A success message confirming deletion.

5. GET /todos/filter/{status}

Description: Filters todos by completion status.

Path Parameter: status can be either completed or pending

Request Body: None

Response: Returns a list of filtered todos based on the given status.
