import psycopg2
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def insert_event(people_count):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO count_events (people_count) VALUES (%s)",
        (people_count,)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_events():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, people_count, timestamp FROM count_events ORDER BY timestamp DESC LIMIT 50"
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    events = []
    for row in rows:
        events.append({
            "id": row[0],
            "people_count": row[1],
            "timestamp": str(row[2])
        })
    return events
