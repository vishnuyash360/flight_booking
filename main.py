# Import the app object from app.py
from app import app
from dotenv import load_dotenv
load_dotenv()


# This is for Gunicorn
if __name__ == "__main__":
    # Import models inside app.py handles database setup
    app.run(host="0.0.0.0", port=5010, debug=True)