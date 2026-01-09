# عربي Vocabulary - Linux

A native desktop application for learning Arabic vocabulary with Danish and English translations.

## System Requirements

- Ubuntu 20.04+ / Debian 11+ / Fedora 35+ or similar
- 64-bit Linux
- ~100 MB disk space

## Installation

1. Download `ArabicVocabulary-0.2-beta-Linux.tar.gz` from the [Releases page](https://github.com/mikkelhappymates/arabic-vocabulary/releases)
2. Extract the archive:
   ```bash
   tar -xzvf ArabicVocabulary-0.2-beta-Linux.tar.gz
   ```
3. Run the application:
   ```bash
   cd ArabicVocabulary
   ./ArabicVocabulary
   ```

## Optional: Create Desktop Entry

To add the app to your application menu:

```bash
cat > ~/.local/share/applications/arabic-vocabulary.desktop << EOF
[Desktop Entry]
Name=Arabic Vocabulary
Comment=Learn Arabic vocabulary with translations
Exec=/path/to/ArabicVocabulary/ArabicVocabulary
Icon=/path/to/ArabicVocabulary/assets/icon.png
Type=Application
Categories=Education;Languages;
EOF
```

Replace `/path/to/ArabicVocabulary` with the actual path where you extracted the app.

## Data Storage

Your vocabulary is saved locally at:
```
~/Documents/ArabicVocabulary/vocabulary.json
```

This folder is created automatically on first launch.

## Features

- **Arabic Word Storage** - Store Arabic words with transliteration, English, and Danish translations
- **Built-in Arabic Keyboard** - Virtual keyboard with full Arabic alphabet and diacritics
- **Tag System** - Organize words with custom tags
- **Search & Filter** - Find words quickly
- **Dark Mode** - Arabic-inspired dark theme with geometric pattern

## Troubleshooting

### App won't start
Make sure you have the required libraries:
```bash
# Ubuntu/Debian
sudo apt-get install libxcb-xinerama0 libxcb-cursor0 libgl1-mesa-glx libegl1-mesa

# Fedora
sudo dnf install libxcb mesa-libGL mesa-libEGL
```

### Arabic text not displaying correctly
Install Arabic fonts:
```bash
# Ubuntu/Debian
sudo apt-get install fonts-arabeyes fonts-noto-core

# Fedora
sudo dnf install google-noto-sans-arabic-fonts
```

## License

MIT License
