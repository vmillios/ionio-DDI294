# Simple Flask API with Authentication and Swagger

This project is a simple Flask-based REST API that demonstrates how to create endpoints, manage a SQLite database, implement token-based authentication, and document the API with Swagger UI.

## Features

- **Flask REST API**: A lightweight and modular web framework.
- **SQLite Database**: A self-contained, serverless database for customer data.
- **Token-Based Authentication**: A simple authentication layer to protect endpoints.
- **Swagger UI**: Interactive API documentation for easy testing and exploration.
- **YAML Configuration**: Centralized configuration for application settings.

## Project Structure

```
.
├── .venv/
├── __pycache__/
├── auth.py
├── config.yaml
├── customers.db
├── db_init.py
├── main.py
├── requirements.txt
└── swagger/
    └── get_customer_by_id.yml
```

- **`main.py`**: The main application file containing the Flask app and API endpoints.
- **`auth.py`**: The authentication decorator and logic.
- **`db_init.py`**: The database initialization script.
- **`config.yaml`**: The configuration file for application settings.
- **`customers.db`**: The SQLite database file.
- **`requirements.txt`**: The list of Python dependencies.
- **`swagger/`**: The directory for Swagger documentation files.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python main.py
    ```

The application will be running at `http://127.0.0.1:5000`.

## API Endpoints

- **`GET /`**: A simple "Hello" endpoint.
- **`GET /customer/<id>`**: Get customer data by ID (requires authentication).
- **`POST /search_customer`**: Search for a customer by email (requires authentication).
- **`GET /apidocs`**: Swagger UI for API documentation.

## Authentication

To access protected endpoints, you need to provide an `Authorization` header with a bearer token:

```
Authorization: Bearer <your_token>
```

The default token is `mysecrettoken`, but you can change it in `config.yaml`.

## Configuration

The `config.yaml` file contains the following settings:

- **`db_name`**: The name of the SQLite database file.
- **`debug`**: The debug mode for the Flask application.
- **`host`**: The host for the Flask application.
- **`port`**: The port for the Flask application.
- **`auth_token`**: The authentication token for the API.

You can modify these settings as needed.
