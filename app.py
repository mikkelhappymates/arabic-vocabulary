"""
Arabic Vocabulary App - Flask Backend
"""
import json
import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'vocabulary.json')
IMAGES_FOLDER = os.path.join(os.path.dirname(__file__), 'data', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Ensure images folder exists
os.makedirs(IMAGES_FOLDER, exist_ok=True)


def load_data():
    """Load vocabulary data from JSON file."""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"words": [], "tags": []}


def save_data(data):
    """Save vocabulary data to JSON file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Routes
@app.route('/')
def index():
    """Serve main page."""
    return render_template('index.html')


@app.route('/api/words', methods=['GET'])
def get_words():
    """Get all words with optional filtering."""
    data = load_data()
    words = data.get('words', [])
    
    # Filter by tag if provided
    tag = request.args.get('tag')
    if tag:
        words = [w for w in words if tag in w.get('tags', [])]
    
    # Search filter
    search = request.args.get('search', '').lower()
    if search:
        words = [w for w in words if 
                 search in w.get('arabic', '').lower() or
                 search in w.get('danish', '').lower() or
                 search in w.get('english', '').lower() or
                 search in w.get('transliteration', '').lower()]
    
    return jsonify(words)


@app.route('/api/words', methods=['POST'])
def add_word():
    """Add a new word."""
    data = load_data()
    word_data = request.json
    
    now = datetime.utcnow().isoformat() + 'Z'
    new_word = {
        "id": str(uuid.uuid4()),
        "arabic": word_data.get('arabic', ''),
        "arabic_diacritics": word_data.get('arabic_diacritics', ''),
        "transliteration": word_data.get('transliteration', ''),
        "danish": word_data.get('danish', ''),
        "english": word_data.get('english', ''),
        "tags": word_data.get('tags', []),
        "image": word_data.get('image'),
        "notes": word_data.get('notes', ''),
        "created_at": now,
        "updated_at": now
    }
    
    data['words'].append(new_word)
    save_data(data)
    
    return jsonify(new_word), 201


@app.route('/api/words/<word_id>', methods=['PUT'])
def update_word(word_id):
    """Update an existing word."""
    data = load_data()
    word_data = request.json
    
    for i, word in enumerate(data['words']):
        if word['id'] == word_id:
            now = datetime.utcnow().isoformat() + 'Z'
            data['words'][i].update({
                "arabic": word_data.get('arabic', word['arabic']),
                "arabic_diacritics": word_data.get('arabic_diacritics', word.get('arabic_diacritics', '')),
                "transliteration": word_data.get('transliteration', word.get('transliteration', '')),
                "danish": word_data.get('danish', word['danish']),
                "english": word_data.get('english', word['english']),
                "tags": word_data.get('tags', word.get('tags', [])),
                "image": word_data.get('image', word.get('image')),
                "notes": word_data.get('notes', word.get('notes', '')),
                "updated_at": now
            })
            save_data(data)
            return jsonify(data['words'][i])
    
    return jsonify({"error": "Word not found"}), 404


@app.route('/api/words/<word_id>', methods=['DELETE'])
def delete_word(word_id):
    """Delete a word."""
    data = load_data()
    
    for i, word in enumerate(data['words']):
        if word['id'] == word_id:
            deleted = data['words'].pop(i)
            save_data(data)
            return jsonify({"message": "Word deleted", "word": deleted})
    
    return jsonify({"error": "Word not found"}), 404


@app.route('/api/tags', methods=['GET'])
def get_tags():
    """Get all tags."""
    data = load_data()
    return jsonify(data.get('tags', []))


@app.route('/api/tags', methods=['POST'])
def add_tag():
    """Add a new tag."""
    data = load_data()
    tag_name = request.json.get('name', '').strip().lower()
    
    if not tag_name:
        return jsonify({"error": "Tag name is required"}), 400
    
    if tag_name not in data['tags']:
        data['tags'].append(tag_name)
        save_data(data)
    
    return jsonify({"name": tag_name}), 201


@app.route('/api/tags/<tag_name>', methods=['DELETE'])
def delete_tag(tag_name):
    """Delete a tag."""
    data = load_data()
    
    if tag_name in data['tags']:
        data['tags'].remove(tag_name)
        # Also remove tag from all words
        for word in data['words']:
            if tag_name in word.get('tags', []):
                word['tags'].remove(tag_name)
        save_data(data)
        return jsonify({"message": "Tag deleted"})
    
    return jsonify({"error": "Tag not found"}), 404


@app.route('/api/upload', methods=['POST'])
def upload_image():
    """Upload an image."""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(IMAGES_FOLDER, filename)
        file.save(filepath)
        return jsonify({"filename": filename, "path": f"/images/{filename}"}), 201
    
    return jsonify({"error": "File type not allowed"}), 400


@app.route('/images/<filename>')
def serve_image(filename):
    """Serve uploaded images."""
    return send_from_directory(IMAGES_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
