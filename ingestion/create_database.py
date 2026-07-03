# Import relevant libraries
import sqlite3
from pathlib import Path

DB_PATH = Path("documentsDB.db")


def create_database():
    # Set up DB connection
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # create Documents table if absent
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_name TEXT NOT NULL,
        doc_path TEXT NOT NULL UNIQUE,
        doc_type TEXT NOT NULL,
        vendor TEXT NOT NULL
    )
    """)

    # create page text table if absent
    ## need to redo this part, plus also look through what other fields to use based on chatgpt inputs
    
    # create Text chunks table if absent
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        chunk_id TEXT PRIMARY KEY, 
        chunk_text TEXT NOT NULL,           
        doc_id INTEGER NOT NULL,
        section TEXT,
        chunk_page_start INTEGER,
        chunk_page_end INTEGER,
        simhash INTEGER,

        FOREIGN KEY (doc_id)
            REFERENCES documents(doc_id)
            ON DELETE CASCADE
    )
    """)

    # Create Images table if absent
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS images (
        image_id TEXT PRIMARY KEY,
        image_path TEXT NOT NULL,
        doc_id INTEGER NOT NULL,
        page_slide_number INTEGER,
        phash TEXT,

        FOREIGN KEY (doc_id)
            REFERENCES documents(doc_id)
            ON DELETE CASCADE
    )
    """)

    # Check that tables are successfully created
    cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' """)
    results = cursor.fetchall()
    if ('documents',) in results and ('chunks',) in results and ('images',) in results:
        print("Database schema created successfully.")

    conn.commit()
    conn.close()



if __name__ == "__main__":
    create_database()
