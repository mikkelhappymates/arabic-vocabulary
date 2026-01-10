"""
Arabic Vocabulary App - Flask Backend
Version 0.5.1 - Full Feature Web App
"""
import json
import os
import sys
import shutil
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration - Use AppData for user data when running as frozen executable
def get_data_dir():
    """Get the appropriate data directory based on how the app is running."""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable - use AppData
        appdata = os.environ.get('APPDATA', os.path.expanduser('~'))
        data_dir = os.path.join(appdata, 'ArabicVocabulary')
        
        # Copy default data if it doesn't exist yet
        bundled_data = os.path.join(os.path.dirname(sys.executable), '_internal', 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)
            # Copy vocabulary.json and settings.json if they exist in bundle
            for filename in ['vocabulary.json', 'settings.json']:
                bundled_file = os.path.join(bundled_data, filename)
                if os.path.exists(bundled_file):
                    shutil.copy2(bundled_file, os.path.join(data_dir, filename))
        
        return data_dir
    else:
        # Running from source - use local data folder
        return os.path.join(os.path.dirname(__file__), 'data')

DATA_DIR = get_data_dir()
DATA_FILE = os.path.join(DATA_DIR, 'vocabulary.json')
SETTINGS_FILE = os.path.join(DATA_DIR, 'settings.json')
IMAGES_FOLDER = os.path.join(DATA_DIR, 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Available languages
AVAILABLE_LANGUAGES = [
    "English", "Danish", "Swedish", "Norwegian", "German", 
    "French", "Spanish", "Italian", "Dutch", "Portuguese",
    "Russian", "Turkish", "Urdu", "Indonesian", "Malay"
]

# Grammar options
GRAMMAR_OPTIONS = {
    "person": ["", "1st Person", "2nd Person", "3rd Person"],
    "number": ["", "Singular", "Dual", "Plural"],
    "gender": ["", "Masculine", "Feminine"],
    "tense": ["", "Past", "Present", "Future", "Imperative"],
    "form": ["", "Form I", "Form II", "Form III", "Form IV", "Form V", 
             "Form VI", "Form VII", "Form VIII", "Form IX", "Form X"]
}

# Ensure folders exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMAGES_FOLDER, exist_ok=True)


def load_data():
    """Load vocabulary data from JSON file."""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"words": [], "tags": [], "word_groups": []}


def save_data(data):
    """Save vocabulary data to JSON file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_settings():
    """Load settings from JSON file."""
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "languages": ["English", "Danish"],
            "custom_languages": []
        }


def save_settings(settings):
    """Save settings to JSON file."""
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


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
        "word_group": word_data.get('word_group', ''),
        "grammar": word_data.get('grammar', {}),
        "translations": word_data.get('translations', {}),
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
                "word_group": word_data.get('word_group', word.get('word_group', '')),
                "grammar": word_data.get('grammar', word.get('grammar', {})),
                "translations": word_data.get('translations', word.get('translations', {})),
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


@app.route('/api/export', methods=['GET'])
def export_data():
    """Export vocabulary data as JSON."""
    data = load_data()
    return jsonify(data)


@app.route('/api/import', methods=['POST'])
def import_data():
    """Import vocabulary data from JSON file."""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.endswith('.json'):
        return jsonify({"error": "Only JSON files are allowed"}), 400
    
    try:
        content = file.read().decode('utf-8')
        imported_data = json.loads(content)
        
        # Validate structure
        if 'words' not in imported_data:
            return jsonify({"error": "Invalid format: missing 'words' array"}), 400
        
        # Merge or replace based on query param
        merge = request.args.get('merge', 'false').lower() == 'true'
        
        if merge:
            current_data = load_data()
            existing_ids = {w['id'] for w in current_data['words']}
            
            for word in imported_data.get('words', []):
                if word.get('id') not in existing_ids:
                    current_data['words'].append(word)
            
            # Merge tags
            for tag in imported_data.get('tags', []):
                if tag not in current_data.get('tags', []):
                    current_data.setdefault('tags', []).append(tag)
            
            # Merge word groups
            for group in imported_data.get('word_groups', []):
                if group not in current_data.get('word_groups', []):
                    current_data.setdefault('word_groups', []).append(group)
            
            save_data(current_data)
            return jsonify({"message": "Data merged successfully", "word_count": len(current_data['words'])})
        else:
            save_data(imported_data)
            return jsonify({"message": "Data imported successfully", "word_count": len(imported_data.get('words', []))})
        
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON file"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Get app settings."""
    settings = load_settings()
    return jsonify({
        **settings,
        "available_languages": AVAILABLE_LANGUAGES,
        "grammar_options": GRAMMAR_OPTIONS
    })


@app.route('/api/settings', methods=['PUT'])
def update_settings():
    """Update app settings."""
    settings_data = request.json
    
    current_settings = load_settings()
    
    # Update languages (max 2)
    if 'languages' in settings_data:
        languages = settings_data['languages'][:2]  # Max 2 languages
        current_settings['languages'] = languages
    
    # Update custom languages
    if 'custom_languages' in settings_data:
        current_settings['custom_languages'] = settings_data['custom_languages']
    
    save_settings(current_settings)
    return jsonify(current_settings)


@app.route('/api/word-groups', methods=['GET'])
def get_word_groups():
    """Get all word groups."""
    data = load_data()
    return jsonify(data.get('word_groups', []))


@app.route('/api/word-groups', methods=['POST'])
def add_word_group():
    """Add a new word group."""
    data = load_data()
    group_name = request.json.get('name', '').strip()
    
    if not group_name:
        return jsonify({"error": "Group name is required"}), 400
    
    if 'word_groups' not in data:
        data['word_groups'] = []
    
    if group_name not in data['word_groups']:
        data['word_groups'].append(group_name)
        save_data(data)
    
    return jsonify({"name": group_name}), 201


if __name__ == '__main__':
    app.run(debug=True, port=5000)
