
# ABC Sports Centre - Public Activity Enrollment App

This project is a full-stack web application for ABC Sports Centre, allowing the public to browse and enroll in various sports and wellness activities. The app consists of a Python FastAPI backend and a React frontend.

## Features
- Browse available activities and featured activities
- Enroll in activities by providing your email
- Modern, elegant UI
- Responsive design

## Project Structure

- `backend/` — Python FastAPI backend API
- `frontend/` — React frontend app

## Installation & Setup

### 1. Backend (Python/FastAPI)

1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install fastapi uvicorn pydantic
   ```
3. Run the backend server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### 2. Frontend (React)

1. Navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Set the backend API URL in `.env` (for Codespaces or remote):
   ```env
   REACT_APP_API_URL=https://<your-codespace-backend-url>
   ```
   For local development, you can omit this or set to `http://localhost:8000`.
4. Start the frontend app:
   ```bash
   npm start
   ```

## Usage

1. Open the frontend app in your browser (usually http://localhost:3000 or your Codespaces URL).
2. Browse featured and available activities.
3. Enroll in an activity by entering your email and selecting an activity.

## Notes
- Ensure the backend is running and accessible from the frontend (check port forwarding in Codespaces).
- The backend stores enrollments in memory (for demo purposes).

## License
MIT
