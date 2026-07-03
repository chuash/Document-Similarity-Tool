# Import relevant libraries
import sqlite3
from pathlib import Path

DB_PATH = Path("sqlite/documentsDB.db")


def create_database():
    # Set up DB connection
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # create Documents table if absent
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        doc_id TEXT PRIMARY KEY,
        doc_name TEXT NOT NULL,
        doc_path TEXT NOT NULL UNIQUE,
        doc_type TEXT NOT NULL,
        vendor_name TEXT NOT NULL
    )
    """)

    # create Pages table if absent
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pages (
        doc_id TEXT NOT NULL,
        page_number INTEGER NOT NULL,
        start_offset INTEGER NOT NULL,
        end_offset INTEGER NOT NULL,
        page_text TEXT,
                   
        PRIMARY KEY (doc_id, page_number),

        FOREIGN KEY (doc_id)
            REFERENCES documents(doc_id)
            ON DELETE CASCADE           
    )
    """)
    
    # create Text chunks table if absent
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        chunk_id TEXT PRIMARY KEY, 
        chunk_text TEXT NOT NULL,           
        doc_id TEXT NOT NULL,
        section TEXT,
        chunk_start INTEGER NOT NULL,
        chunk_end INTEGER NOT NULL,
        page_start INTEGER NOT NULL,
        page_end INTEGER NOT NULL,
        simhash TEXT NOT NULL,

        FOREIGN KEY (doc_id)
            REFERENCES documents(doc_id)
            ON DELETE CASCADE
    )
    """)

    # Create Images table if absent
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS images (
        image_id TEXT PRIMARY KEY,
        image_path TEXT NOT NULL UNIQUE,
        doc_id TEXT NOT NULL,
        page_number INTEGER NOT NULL,
        phash TEXT NOT NULL,

        FOREIGN KEY (doc_id)
            REFERENCES documents(doc_id)
            ON DELETE CASCADE
    )
    """)

    # Create indexes to facilitate database search

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_chunks_doc ON chunks(doc_id)""")
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_images_doc ON images(doc_id)""")

    # Check that tables are successfully created
    cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' """)
    results = cursor.fetchall()
    if ('documents',) in results and ('chunks',) in results and ('images',) in results:
        print("Database schema created successfully.")

    conn.commit()
    conn.close()



if __name__ == "__main__":
    create_database()
