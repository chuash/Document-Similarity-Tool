import hmac, logging, os, time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from google import genai
#from pydantic import BaseModel
from typing import Dict, List, Literal

# Load environment variables
if not load_dotenv(".env"):
    pass

# Define variables
#Groq_model = st.secrets['GROQ_MODEL_NAME']                      #os.getenv("GROQ_MODEL_NAME")
#Gemini_model = st.secrets['GEMINI_MODEL_NAME']                  #os.getenv("GEMINI_MODEL_NAME")    
                           

# Set up custom exception class
class MyError(Exception):
    def __init__(self, value):
        self.value = value

    # Defining __str__ so that print() returns this
    def __str__(self):
        return self.value


# Set up shared logger instance for the entire application.
def setup_shared_logger(log_file_name="application.log"):

    # Create the logger with name "shared_app_logger" if it doesn's exist
    logger = logging.getLogger('shared_app_logger')
    # Set the desired logging level
    logger.setLevel(logging.INFO)

    # Prevent adding multiple handlers if setup_shared_logger is called multiple times
    if not logger.handlers:
        # Create a file handler
        file_handler = logging.FileHandler(log_file_name, mode='a')
        file_handler.setLevel(logging.INFO)

        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)

    return logger



