# FastAPI Project

> ### **`FastAPI is a Python based modern and beginner friendly framework for building web API's and backend services in no time.`**

## Project Setup with Virtual Environment

### 1. Create and activate virtual environment:
```bash
python -m venv fastapi_env
fastapi_env\Scripts\Activate.ps1  # On Windows PowerShell
# or
fastapi_env\Scripts\activate.bat  # On Windows Command Prompt
```

### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. To run a FastAPI app:

`uvicorn main:app --reload`

The API will be available at:
- Main application: http://127.0.0.1:8000
- Interactive API docs: http://127.0.0.1:8000/docs
- Alternative API docs: http://127.0.0.1:8000/redoc

### FastAPI CLI (Alternative method)

1. CLI installation: ```pip install "fastapi[standard]"`
2. Running your app: `fastapi dev file.py`

## Key Concepts

1. Path parameter and query parameter  
   **Query parameter**: Query parameter is a key-value pair which describes more about a path parameter or url.
2. What is CURL
3. What is response header

> POST method is used for creating something or giving/submitting data to the database.

### Request body

A request body is data sent by the client to your API.

## Deactivating Virtual Environment

To deactivate the virtual environment:
```bash
deactivate
```
