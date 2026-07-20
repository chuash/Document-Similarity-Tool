# Import relevant libraries
import sqlite3
from pathlib import Path
from typing import Dict, List
from utils import MyError, setup_shared_logger

# Set up the shared logger
logger = setup_shared_logger()

# Declare database path
DB_PATH = Path("sqlite") / "documentsDB.db"
# Create the database directory if it doesn't exist
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    """
    Sets up the database connection
    """
    try:
    # Set up DB connection
        conn = sqlite3.connect(DB_PATH)
    # Ensures that foreign key relationships are actually enforced
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except (Exception, BaseException) as e:
        raise MyError(f"Error connecting to database: {e}")


def create_database(conn:sqlite3.Connection):
    """
    Creates the database tables if they are not in existence
    """
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
        page_start_offset INTEGER NOT NULL,
        page_end_offset INTEGER NOT NULL,
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

        FOREIGN KEY (doc_id, page_number)
            REFERENCES pages(doc_id, page_number)
            ON DELETE CASCADE
    )
    """)

    # Create indexes to facilitate database search
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_chunks_doc ON chunks(doc_id)""")
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_images_doc ON images(doc_id)""")

    conn.commit()
    conn.close()

    logger.info(f"Database successfully created or already in existence")


def insert_documents(conn:sqlite3.Connection, documents:List[Dict]):
    """
    Adding the discovered documents into the database
    """
    try:
        conn.executemany(
            """
            INSERT INTO documents
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (
                    d["doc_id"],
                    d["doc_name"],
                    d["doc_path"],
                    d["doc_type"],
                    d["vendor_name"],
                )
                for d in documents
            ],
        )

        logger.info(f"{len(documents)} documents successfully inserted into database")
    
    except(Exception, BaseException) as e:
        raise MyError(f"Error inserting documents into database: {e}")


def insert_pages(conn:sqlite3.Connection, pages:List[Dict]):
    """
    Adding the extracted page text and metadata into the database
    """
    try:
        conn.executemany(
            """
            INSERT INTO pages
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (
                    p["doc_id"],
                    p["page_number"],
                    p["page_start_offset"],
                    p["page_end_offset"],
                    p["page_text"],
                )
                for p in pages
            ],
        )
    
        logger.info(f"{len(pages)} pages of information successfully inserted into database")
    
    except(Exception, BaseException) as e:
        raise MyError(f"Error inserting page information into database: {e}")


def insert_chunks(conn:sqlite3.Connection, chunks:List[Dict]):
    """
    Adding the text chunks into the database
    """
    try:
        conn.executemany(
            """
            INSERT INTO chunks
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    c["chunk_id"],
                    c["chunk_text"],
                    c["doc_id"],
                    c["section"],
                    c["chunk_start"],
                    c["chunk_end"],
                    c["page_start"],
                    c["page_end"],
                    c["simhash"],
                )
                for c in chunks
            ],
        )

        logger.info(f"{len(chunks)} text chunks successfully inserted into database")
    
    except(Exception, BaseException) as e:
        raise MyError(f"Error inserting text chunks into database: {e}")


def insert_images(conn:sqlite3.Connection, images:List[Dict]):
    """
    Adding the extracted images into the database
    """
    try:
        conn.executemany(
            """
            INSERT INTO images
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (
                    i["image_id"],
                    i["image_path"],
                    i["doc_id"],
                    i["page_number"],
                    i["phash"],
                )
                for i in images
            ],
        )
    
        logger.info(f"{len(images)} extracted images successfully inserted into database")
    
    except(Exception, BaseException) as e:
        raise MyError(f"Error inserting extracted images into database: {e}")


if __name__ == "__main__":
    pass
