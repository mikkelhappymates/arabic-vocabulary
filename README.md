# عربي Vocabulary

A native desktop application for learning Arabic vocabulary with Danish and English translations.

![PyQt6](https://img.shields.io/badge/PyQt6-6.6.1-green)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows-lightgrey)

## Download

**[Download Latest Release](https://github.com/mikkelhappymates/arabic-vocabulary/releases/latest)**

| Platform | Download |
|----------|----------|
| macOS | `ArabicVocabulary-0.1-beta-Mac.zip` |
| Windows | `ArabicVocabulary-0.1-beta-Windows.zip` |

## Features

- **Arabic Word Storage** - Store Arabic words with transliteration, English, and Danish translations
- **Built-in Arabic Keyboard** - Virtual keyboard with full Arabic alphabet and diacritics (harakat)
- **Tag System** - Organize words with custom tags for easy categorization
- **Search & Filter** - Quickly find words by searching or filtering by tag
- **Local Storage** - All data saved locally in ~/Documents/ArabicVocabulary
- **Dark Mode** - Arabic-inspired dark theme with geometric pattern background
- **Notes** - Add personal notes or example sentences to each word

## Installation

### macOS
1. Download `ArabicVocabulary-0.1-beta-Mac.zip` from [Releases](https://github.com/mikkelhappymates/arabic-vocabulary/releases)
2. Open the DMG and drag the app to Applications
3. On first launch, macOS will block the app (it's not code-signed)
4. Go to **System Settings → Privacy & Security**
5. Scroll down and click **"Open Anyway"** next to the Arabic Vocabulary message
6. Enter your admin password when prompted

### Windows
1. Download `ArabicVocabulary-0.1-beta-Windows.zip` from [Releases](https://github.com/mikkelhappymates/arabic-vocabulary/releases)
2. Run the installer
3. If SmartScreen appears, click "More info" → "Run anyway"
4. Launch from Start Menu or Desktop shortcut

### From Source
1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run:
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
