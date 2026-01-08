# عربي Vocabulary

A native desktop application for learning Arabic vocabulary with Danish and English translations.

![PyQt6](https://img.shields.io/badge/PyQt6-6.6.1-green)
![Python](https://img.shields.io/badge/Python-3.9+-blue)

## Features

- **Arabic Word Storage** - Store Arabic words with transliteration, English, and Danish translations
- **Built-in Arabic Keyboard** - Virtual keyboard with full Arabic alphabet and diacritics (harakat)
- **Tag System** - Organize words with custom tags for easy categorization
- **Search & Filter** - Quickly find words by searching or filtering by tag
- **Local Storage** - All data saved locally in JSON format
- **Dark Mode** - Arabic-inspired dark theme with geometric pattern background
- **Notes** - Add personal notes or example sentences to each word

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python3 main.py
```

### Adding Words

1. Click the **+ Add Word** button
2. Enter the Arabic word (use the keyboard icon to open the virtual Arabic keyboard)
3. Add transliteration, English and Danish translations
4. Select or create tags to categorize the word
5. Click **Save**

### Arabic Keyboard

The built-in Arabic keyboard includes:
- Full Arabic alphabet
- Numbers (٠-٩)
- Diacritics/Harakat: Fatha (َ), Kasra (ِ), Damma (ُ), Sukun (ْ), Shadda (ّ), Tanwin

### Managing Words

- **Edit** - Click the ✏️ Edit button on any word card
- **Delete** - Click the 🗑️ Delete button to remove a word
- **Search** - Use the search bar to find words
- **Filter** - Use the tag dropdown to filter by category

## Data Storage

Vocabulary data is stored in `data/vocabulary.json`. The file is created automatically on first run with some starter words.

## Project Structure

```
x/
├── main.py              # Main application
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── data/
    └── vocabulary.json  # Word database
```

## License

MIT License - Feel free to use and modify as needed.
