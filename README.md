# Mood Board Backend

## Overview
A minimal **FastAPI** backend that serves random inspirational quotes and evaluates typing test results. The service provides two endpoints:

- `GET /quote` – Returns a random quote.
- `POST /submit` – Accepts the original quote, the user‑typed text, and the elapsed time, then calculates **WPM** (words per minute) and **accuracy**.

The application is containerised with Docker and includes a full CI/CD pipeline (Gitleaks, Trivy, Ruff linting/formatting, and Pytest) powered by GitHub Actions.

## Features
- Random quote generator
- Typing test score calculation (WPM & accuracy)
- Comprehensive unit tests with `pytest`
- Code linting and auto‑formatting using **Ruff**
- Containerisation via **Docker**
- Security scanning with **Trivy** and secret scanning with **Gitleaks**

## Tech Stack
- **Python 3.13**
- **FastAPI** – web framework
- **Pydantic** – data validation
- **Uvicorn** – ASGI server (development)
- **Ruff** – linter & formatter
- **Pytest** – testing framework
- **Docker** – containerisation
- **GitHub Actions** – CI/CD

## Prerequisites
- Windows 10/11 with PowerShell (or any terminal)
- [Python 3.13](https://www.python.org/downloads/release/python-3.13.0/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop) (optional, for container execution)
- `git` (for version control)

## Project Structure
```
 mood-board-backend/
 ├─ .github/                # GitHub Actions workflows
 │   └─ workflows/
 │       └─ continuous-integration.yml
 ├─ tests/                  # Unit tests
 │   └─ test_main.py
 ├─ main.py                # FastAPI application
 ├─ Dockerfile              # Docker image definition
 ├─ requirements.txt       # Pin‑exact dependencies (generated via pip freeze)
 ├─ pyproject.toml          # Ruff configuration
 └─ README.md              # This file
```

## Setup (Local Development)
1. **Clone the repository**
   ```powershell
   git clone <repository‑url>
   cd mood-board-backend
   ```
2. **Create and activate a virtual environment**
   ```powershell
   python -m venv .venv
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
   & .\.venv\Scripts\Activate.ps1
   ```
3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```
4. **Run the API locally**
   ```powershell
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
   Open `http://127.0.0.1:8000` in your browser or use an API client (e.g., Postman).

## Docker Usage
Build and run the container:
```bash
# Build the image
docker build -t mood-board-backend:latest .

# Run the container
docker run -p 8000:8000 mood-board-backend:latest
```
The API will be reachable at `http://localhost:8000`.

## Linting & Formatting
Ruff is configured in `pyproject.toml`. To check code style:
```powershell
ruff check .
```
To automatically fix issues and format code:
```powershell
ruff check --fix .
ruff format .
```

## Testing
Run the test suite with:
```powershell
pytest -q
```
All tests should pass, confirming the correctness of the endpoints.

## CI/CD Pipeline
The repository includes a GitHub Actions workflow (`.github/workflows/continuous-integration.yml`) that runs the following jobs on each push:
- **Gitleaks** – scans for secrets.
- **Trivy** – scans the Docker image for vulnerabilities.
- **Ruff** – linting and formatting checks.
- **Pytest** – unit test execution.
The pipeline fails if any job reports issues, ensuring code quality and security.

## Contributing
Contributions are welcome! Please:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Ensure the code passes linting (`ruff`) and all tests (`pytest`).
4. Open a Pull Request with a clear description.

## License
This project is released under the **MIT License**. See the `LICENSE` file for details.