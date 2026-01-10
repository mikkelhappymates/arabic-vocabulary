import webview
import threading
import sys
import os
from app import app

def start_server():
    """Starts the Flask server."""
    # Run the app without the reloader to avoid thread issues
    app.run(port=5000, use_reloader=False)

if __name__ == '__main__':
    # Start the Flask server in a separate thread
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    # Create a full-screen-ish window
    webview.create_window(
        "Arabic Vocabulary", 
        "http://127.0.0.1:5000",
        width=1024,
        height=768,
        resizable=True
    )

    # Start the webview GUI
    webview.start()
