# Arabic Vocabulary App - Development Plan

## Overview

A personal vocabulary storage application for Arabic words with Danish and English translations. Features a dark mode UI with Arabic-inspired design elements.

### Core Concept
- **Base version ships with only a few starter words** (5-10 common words)
- **Easy word addition**: Simple form to add new words quickly
- **Local persistence**: All added words are saved locally (JSON file) immediately after being added
- **Each word stores**: Arabic text, English translation, and Danish translation
- **Built-in Arabic keyboard**: Virtual keyboard for typing Arabic characters without needing system keyboard setup

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3 + Flask |
| Frontend | HTML, CSS, JavaScript |
| Storage | JSON file (local) |
| Images | Local file storage |

---

## Project Structure

```
x/
├── app.py                 # Flask server & API endpoints
├── data/
│   ├── vocabulary.json    # Word database
│   └── images/            # Uploaded images
├── static/
│   ├── style.css          # Dark mode + Arabic-inspired styling
│   └── app.js             # Frontend logic
├── templates/
│   └── index.html         # Main UI template
├── requirements.txt       # Python dependencies
└── ideas/
    └── plan.md            # This file
```

---

## Data Model

### Vocabulary Entry
```json
{
  "id": "uuid-string",
  "arabic": "كتاب",
  "arabic_diacritics": "كِتَاب",
  "transliteration": "kitaab",
  "danish": "bog",
  "english": "book",
  "tags": ["nouns", "objects"],
  "image": "images/abc123.jpg",
  "notes": "Optional notes about the word",
  "created_at": "2026-01-08T10:00:00Z",
  "updated_at": "2026-01-08T10:00:00Z"
}
```

### Arabic Diacritics (Tashkeel)
The app supports storing Arabic text with and without diacritical marks:
- `arabic` - Base form without vowel marks (for searching/display)
- `arabic_diacritics` - Full form with tashkeel/harakat (فَتْحَة، كَسْرَة، ضَمَّة، سُكُون، شَدَّة)

This allows:
- Easy searching on the base form
- Learning proper pronunciation with diacritics
- Toggle display between forms in the UI

### Database Structure
```json
{
  "words": [...],
  "tags": ["nouns", "verbs", "food", "greetings", ...]
}
```

---

## Features

### Core Features
- [ ] Add new vocabulary entries
- [ ] Edit existing entries
- [ ] Delete entries
- [ ] Upload and display images
- [ ] Create and manage tags
- [ ] Assign multiple tags per word
- [ ] Filter/search by tag
- [ ] Search across all languages
- [ ] RTL text support for Arabic
- [ ] Store Arabic with and without diacritics (tashkeel)
- [ ] Toggle diacritics display on/off
- [ ] **Built-in Arabic virtual keyboard**
- [ ] **Save words to local JSON immediately on add**
- [ ] **Ship with minimal starter vocabulary (5-10 words)**

### Built-in Arabic Keyboard
The app includes a virtual on-screen Arabic keyboard for easy input:
- Full Arabic alphabet (28 letters)
- Common diacritics/tashkeel buttons (فَتْحَة، كَسْرَة، ضَمَّة، سُكُون، شَدَّة)
- Special characters (ء، ة، ى، آ، أ، إ، ؤ، ئ)
- Keyboard toggle button next to Arabic input fields
- Keyboard layout based on standard Arabic keyboard
- Click-to-type functionality
- Backspace and clear buttons
- Optional: number row with Arabic-Indic numerals (٠١٢٣٤٥٦٧٨٩)

### Starter Words (Base Version)
The app ships with a small set of common words:
```json
[
  { "arabic": "مرحبا", "english": "hello", "danish": "hej" },
  { "arabic": "شكرا", "english": "thank you", "danish": "tak" },
  { "arabic": "نعم", "english": "yes", "danish": "ja" },
  { "arabic": "لا", "english": "no", "danish": "nej" },
  { "arabic": "ماء", "english": "water", "danish": "vand" }
]
```

### UI Features
- [ ] Dark mode theme
- [ ] Arabic-inspired geometric patterns/borders
- [ ] Card-based word display
- [ ] Responsive layout
- [ ] Modal forms for add/edit
- [ ] **Virtual Arabic keyboard component**
- [ ] **Quick-add word form (Arabic + English + Danish)**

---

## Design Theme

### Color Palette (Dark Mode + Arabic-inspired)
| Element | Color |
|---------|-------|
| Background | Deep dark blue `#0a0f1a` |
| Card Background | Dark blue-gray `#1a2332` |
| Primary Accent | Gold/amber `#d4a853` |
| Secondary Accent | Teal `#2d9596` |
| Text Primary | Off-white `#e8e6e3` |
| Text Secondary | Muted gray `#8b9bb4` |
| Arabic Text | Gold accent `#d4a853` |
| Borders | Subtle gold `#3d3526` |

### Design Elements
- Geometric patterns inspired by Islamic art (subtle, decorative)
- Ornate borders on cards
- Arabic calligraphy-friendly fonts (Amiri, Scheherazade)
- Subtle star/arabesque decorations
- Smooth transitions and hover effects

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main page |
| GET | `/api/words` | Get all words (with optional filters) |
| POST | `/api/words` | Add new word |
| PUT | `/api/words/<id>` | Update word |
| DELETE | `/api/words/<id>` | Delete word |
| POST | `/api/upload` | Upload image |
| GET | `/api/tags` | Get all tags |
| POST | `/api/tags` | Create new tag |
| DELETE | `/api/tags/<name>` | Delete tag |

---

## Implementation Steps

### Phase 1: Setup
1. Create project structure
2. Set up Flask app with basic routing
3. Create initial JSON data file
4. Add requirements.txt

### Phase 2: Backend
1. Implement word CRUD endpoints
2. Implement tag management
3. Implement image upload/serving
4. Add search/filter functionality

### Phase 3: Frontend
1. Create HTML template with dark theme
2. Style with Arabic-inspired CSS
3. Build JavaScript for API interaction
4. Add form handling for words
5. Implement tag filtering UI
6. Add image upload preview
7. **Build Arabic virtual keyboard component**
8. **Integrate keyboard with Arabic input fields**

### Phase 4: Polish
1. Add loading states
2. Error handling
3. Keyboard shortcuts
4. Responsive design tweaks

---

## Backup Strategy

Simply copy the `data/` folder to backup all vocabulary and images:
```bash
cp -r data/ ~/backup/arabic-vocab-backup-$(date +%Y%m%d)/
```

---

## Running the App

```bash
# Install dependencies (one time)
pip3 install -r requirements.txt

# Run the server
python3 app.py

# Open in browser
open http://localhost:5000
```

---

## Future Ideas (Optional)
- Export to CSV/PDF
- Flashcard practice mode
- Audio pronunciation
- Spaced repetition
- iCloud sync
