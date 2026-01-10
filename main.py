import webview
import threading
import sys
import os
import json
from app import app, load_data

class Api:
    def __init__(self, window):
        self.window = window
    
    def save_export(self, data):
        """Save exported data using native file dialog."""
        result = self.window.create_file_dialog(
            webview.SAVE_DIALOG,
            save_filename='vocabulary.json',
            file_types=('JSON Files (*.json)',)
        )
        if result:
            filepath = result if isinstance(result, str) else result[0]
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        return False

def start_server():
    """Starts the Flask server."""
    # Run the app without the reloader to avoid thread issues
    app.run(port=5000, use_reloader=False)

if __name__ == '__main__':
    # Start the Flask server in a separate thread
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    # Create window
    window = webview.create_window(
        "Arabic Vocabulary", 
        "http://127.0.0.1:5000",
        width=1024,
        height=768,
        resizable=True
    )
    
    # Expose API to JavaScript
    window.expose(Api(window).save_export)

    # Start the webview GUI
    webview.start()
