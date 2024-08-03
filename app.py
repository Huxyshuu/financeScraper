from waitress import serve
from main import app  # Import your Flask app instance from app.py
import webbrowser
import time

if __name__ == '__main__':
    print("Hosting the app on http://localhost:6969")
    time.sleep(2)  # Delay to ensure Flask has started
    webbrowser.open('http://localhost:6969/')
    serve(app, host='0.0.0.0', port=6969)