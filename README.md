# People Counter API

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-green?logo=fastapi)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-red?logo=opencv)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI%20Server-purple?logo=uvicorn)

## Project Overview

People Counter API is a real-time people counting system built with FastAPI and OpenCV. It processes a video file using background subtraction and contour detection to count moving people, serves the data through REST API endpoints, and stores all count events permanently in a PostgreSQL database.

---

## Tech Stack

- **Python 3.11**  
- **FastAPI** – REST API framework  
- **Uvicorn** – ASGI server for FastAPI (Gunicorn for production)  
- **OpenCV (cv2)** – Video processing, background subtraction, contour detection  
- **PostgreSQL** – Permanent storage for count events  
- **psycopg2-binary** – PostgreSQL connector for Python  
- **python-dotenv** – Secure environment variable management

---

## Project Structure

- `camera.py` – OpenCV thread: captures video, detects and counts moving people, updates shared variables
- `database.py` – PostgreSQL connection and queries (`insert_event`, `get_events`)
- `main.py` – FastAPI app with 3 endpoints, starts camera thread on startup
- `.env` – Stores database credentials securely
- `requirements.txt` – All Python dependencies

---

## How It Works

1. On startup, FastAPI launches OpenCV in a background thread
2. OpenCV reads frames from a video file (`test_video.mp4`)
3. Background subtraction detects moving areas in each frame
4. Contour detection counts each large moving blob as one person
5. Count is updated in a shared variable protected by a threading lock
6. Every time the count changes, it is saved to PostgreSQL
7. FastAPI endpoints read the shared variable and database to serve data

---

## API Endpoints

- `GET /count` – Returns the current live people count from the camera
- `GET /events` – Returns last 50 count readings from in-memory storage
- `GET /db-events` – Returns permanent count history from PostgreSQL

---

## How to Run

1. Clone the repo
2. Create and activate a virtual environment
3. Run `pip install -r requirements.txt`
4. Create a PostgreSQL database called `people_counter_db`
5. Create the `count_events` table:

   ```sql
   CREATE TABLE count_events (
     id SERIAL PRIMARY KEY,
     people_count INTEGER NOT NULL,
     timestamp TIMESTAMP DEFAULT NOW()
   );
   ```
6. Create a `.env` file with:
   ```env
   DB_HOST=your_host
   DB_NAME=people_counter_db
   DB_USER=your_user
   DB_PASSWORD=your_password
   ```
7. Add a video file called `test_video.mp4` to the project folder
8. Run `uvicorn main:app --reload`
9. Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to test all endpoints

---

## Key Concepts

- Python threading to run camera and API server simultaneously
- Threading lock to safely share data between threads
- Background subtraction (MOG2) for motion detection
- Contour detection and area filtering for people counting
- Environment variables for secure credential management
- FastAPI lifespan handler for startup events

---

## Limitations

- Only detects moving people, not stationary ones
- One person can produce multiple contours causing overcounting
- A more accurate approach would use a YOLO deep learning model for proper human detection

---

## License

This project is licensed under the MIT License.
