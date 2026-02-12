\# Job Tracker API



A production-style RESTful API built with FastAPI + SQLAlchemy and persistent SQLite storage.



\## Features

\- Create / list / update (PATCH) / delete jobs (CRUD)

\- Filter jobs by status: `GET /jobs?status=Interview`

\- Clean architecture: schemas + CRUD layer + dependency injection

\- Swagger UI: http://127.0.0.1:8000/docs



\## Tech Stack

\- FastAPI

\- SQLAlchemy ORM

\- SQLite

\- Pydantic



\## Run Locally (Windows)

```bash

\# (optional) activate venv

.\\.venv\\Scripts\\Activate.ps1



pip install -r requirements.txt

uvicorn main:app --reload

Open:

http://127.0.0.1:8000/docs



\## API Example Flow



1\. POST /jobs

2\. GET /jobs

3\. PATCH /jobs/{job\_id}

4\. GET /jobs?status=Interview

5\. DELETE /jobs/{job\_id}





