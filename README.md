# FastAPI Gitflow

This repository demonstrates an enhanced FastAPI service that combines advanced Git workflows with a robust REST API implementation. The project not only includes a basic greeting API (`/hello` and conditionally `/goodbye`), but also a complete CRUD resource (`/messages`) with GET, POST, PUT, PATCH, and DELETE methods.

The project is designed to illustrate:
- Advanced FastAPI features using Pydantic models and environment-based feature flags.
- A full set of HTTP methods for CRUD operations.
- Best practices in Git workflows (feature branching, merging, fast-forward merges, and rebasing).
- Dependency and virtual environment management with [Poetry](https://python-poetry.org/).
- Automated testing with `pytest` and continuous integration via GitHub Actions.
- Interactive API documentation via Swagger UI and ReDoc.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
  - [Using Poetry](#using-poetry)
  - [Local Virtual Environment (Optional)](#local-virtual-environment-optional)
- [Running the Application](#running-the-application)
  - [Using `poetry run`](#using-poetry-run)
  - [Activating the Virtual Environment](#activating-the-virtual-environment)
- [API Endpoints](#api-endpoints)
  - [/hello Endpoint](#hello-endpoint)
  - [/goodbye Endpoint](#goodbye-endpoint)
  - [/messages CRUD Resource](#messages-crud-resource)
- [Running Tests](#running-tests)
- [Git & GitHub Workflow](#git--github-workflow)
- [GitHub Actions Workflow](#github-actions-workflow)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project is built using [FastAPI](https://fastapi.tiangolo.com/) and demonstrates:

- A REST API with greeting endpoints and a complete CRUD resource.
- Feature flags that control endpoint availability and behavior using environment variables.
- Advanced Git techniques, including feature branching, merging, fast-forward merges, and rebasing.
- Dependency management and virtual environment handling with Poetry.
- Automated testing with `pytest` and CI configured through GitHub Actions.
- Automatically generated interactive API documentation (Swagger UI and ReDoc).

## Features

- **`/hello` Endpoint:**  
  - Returns a greeting message.
  - Supports a custom `name` parameter (defaulting to "Kraken") and a `formal` query parameter.
  - Honors a global feature flag (`FEATURE_FORMAL_GREETING`) for enforcing a formal greeting.

- **`/goodbye` Endpoint:**  
  - Returns a farewell message.
  - Controlled by the `FEATURE_GOODBYE` flag (disabled when set to `False`).

- **`/messages` CRUD Resource:**  
  - **GET /messages:** List all messages.
  - **GET /messages/{message_id}:** Retrieve a specific message.
  - **POST /messages:** Create a new message (assigns an auto-incremented ID).
  - **PUT /messages/{message_id}:** Fully update an existing message.
  - **PATCH /messages/{message_id}:** Partially update an existing message.
  - **DELETE /messages/{message_id}:** Delete a message (returns HTTP 204 on success).

- **Automated Testing and CI:**  
  - Extensive test scenarios covering all endpoints.
  - Continuous integration configured with GitHub Actions.

- **Dependency Management with Poetry:**  
  - Uses Poetry for dependency installation, virtual environment handling, and packaging.
  - Optionally configure a local virtual environment for easier activation.

## Project Structure

A typical directory layout for this project is:

```
GIT-FASTAPI/
├── .github/
│   └── workflows/
│       └── test.yml           # GitHub Actions workflow file for running tests
├── api/                       # Package containing application code
│   ├── __init__.py
│   └── main.py                # FastAPI application instance
├── tests/                     # Unit tests (e.g., test_main.py)
├── pyproject.toml             # Poetry configuration file
├── poetry.lock                # Dependency lock file (generated by Poetry)
└── README.md                  # Project documentation (this file)
```

## Installation & Setup

### Using Poetry

This project uses [Poetry](https://python-poetry.org/) for dependency management. To install Poetry, follow the official installation instructions. For example:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

After installing Poetry, clone the repository and install the dependencies:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/fastapi-gitflow-enhanced.git
   cd fastapi-gitflow-enhanced
   ```

2. **Install Dependencies:**

   ```bash
   poetry install
   ```

   This command will create a virtual environment (by default in Poetry’s cache) and install all required dependencies defined in `pyproject.toml`.

### Local Virtual Environment (Optional)

If you prefer having a virtual environment inside your project directory:
1. **Configure Poetry to Create a Local Environment:**

   ```bash
   poetry config virtualenvs.in-project true
   poetry install
   ```

   This creates a `.venv` folder in your project root.

## Running the Application

You can run the FastAPI application using Uvicorn either by using `poetry run` (recommended) or by activating the virtual environment manually.

### Using `poetry run`

This method executes your command within the Poetry-managed virtual environment:

```bash
poetry run uvicorn api.main:app --reload
```

- Here, `api.main:app` specifies that Uvicorn should load the `app` instance from the `main.py` module inside the `api` package.
- The `--reload` flag enables hot reloading for development.

### Activating the Virtual Environment

If you prefer an interactive shell with your environment activated, follow these steps:

1. **If Using a Local Environment (`.venv`):**

   On Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   (If you encounter an execution policy error, run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` first.)

2. **If Your Environment Is Managed by Poetry (Global Cache):**

   Run the following command to get the path:

   ```bash
   poetry env info --path
   ```

   Then activate it manually using PowerShell (adjust the path accordingly):

   ```powershell
   & 'C:\Users\mccat\AppData\Local\pypoetry\Cache\virtualenvs\git-fastapi-XXXXXX-py3.10\Scripts\Activate.ps1'
   ```

   *Note: Using `poetry run` is generally simpler and avoids manual activation.*

## API Endpoints

### /hello Endpoint

- **Method:** GET  
- **Description:** Returns a greeting message.
- **Query Parameters:**
  - `name` (optional): Customizes the greeting (default: "Kraken").
  - `formal` (optional): When set to `True`, returns a formal greeting ("Good day").
- **Example:**
  - Request: `/hello?name=Alice&formal=True`
  - Response:
    ```json
    { "message": "Good day Alice" }
    ```

### /goodbye Endpoint

- **Method:** GET  
- **Description:** Returns a farewell message.
- **Note:** Only available if the `FEATURE_GOODBYE` flag is enabled.
- **Query Parameters:**
  - `name` (optional): Customizes the farewell (default: "world").
- **Example:**
  - Request: `/goodbye?name=Alice`
  - Response:
    ```json
    { "message": "Goodbye Alice" }
    ```

### /messages CRUD Resource

This resource supports full CRUD operations:

- **GET /messages:**  
  - **Description:** Lists all messages.
  - **Response:** An array of message objects.

- **GET /messages/{message_id}:**  
  - **Description:** Retrieves a message by its ID.
  - **Response:** A single message object.

- **POST /messages:**  
  - **Description:** Creates a new message.
  - **Request Body Example:**
    ```json
    { "content": "Hello world!" }
    ```
  - **Response:** The created message with an assigned ID.

- **PUT /messages/{message_id}:**  
  - **Description:** Fully updates an existing message.
  - **Request Body Example:**
    ```json
    { "content": "Updated complete message" }
    ```
  - **Response:** The updated message.

- **PATCH /messages/{message_id}:**  
  - **Description:** Partially updates an existing message.
  - **Request Body Example:**
    ```json
    { "content": "Partially updated message" }
    ```
  - **Response:** The updated message.

- **DELETE /messages/{message_id}:**  
  - **Description:** Deletes a message.
  - **Response:** HTTP 204 (No Content) on success.

## Running Tests

The test suite uses `pytest` and FastAPI's TestClient. To run all tests locally:

```bash
poetry run pytest
```

This command runs tests in the `tests` directory and reports the results.

## Git & GitHub Workflow

### Feature Branching & Gitflow

- **Feature Branches:**  
  Develop new features on isolated branches (e.g., `feature/messages-crud`, `feature/goodbye`):
  ```bash
  git checkout -b feature/messages-crud
  ```

- **Merging:**  
  Merge completed features into `main` with a merge commit:
  ```bash
  git checkout main
  git merge feature/messages-crud
  ```

- **Fast-Forward Merges:**  
  If no changes exist in `main` since branching:
  ```bash
  git checkout main
  git merge --ff feature/messages-crud
  ```

- **Rebasing:**  
  If `main` has new commits, rebase your feature branch:
  ```bash
  git checkout feature/messages-crud
  git rebase main
  ```

### GitHub Repository Management

- **Pull Requests:**  
  Create pull requests to merge feature branches into `main`, ensuring code review and automated testing.
- **Using Tools:**  
  Tools like GitKraken can help visualize branches, manage merges, and perform interactive rebases.

## GitHub Actions Workflow

The project includes a CI pipeline defined in `.github/workflows/test.yml`. This workflow:

1. **Trigger Events:**
   - Runs on pushes to `main`.
   - Runs on pull requests targeting `main`.

2. **Job Execution:**
   - Uses Ubuntu runners with Python 3.8, 3.9, and 3.10.
   - Checks out code, sets up the Python environment, installs dependencies via Poetry, and runs tests with `pytest`.

Refer to the [GitHub Actions workflow file](.github/workflows/test.yml) for the full configuration.

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI:**  
  View at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for a fully interactive API explorer.
- **ReDoc:**  
  View at [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) for a detailed documentation view.

## Contributing

Contributions are welcome. Please follow these steps:

1. **Fork the repository.**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit your changes.**
4. **Push your branch and open a pull request** for review.

Ensure your changes follow our code style and include relevant tests.

