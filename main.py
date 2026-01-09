"""
Arabic Vocabulary App - Desktop Application (PyQt6)
A native desktop app for learning Arabic vocabulary with Danish and English translations.
Version: 0.2 Beta
"""

import sys
import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QScrollArea, QFrame,
    QGridLayout, QDialog, QMessageBox, QComboBox, QSizePolicy, QStackedWidget,
    QRadioButton, QButtonGroup, QFileDialog, QCheckBox, QInputDialog
)
from PyQt6.QtCore import Qt, QSize, QPointF
from PyQt6.QtGui import QFont, QColor, QPalette, QPainter, QPen, QBrush, QPainterPath
import math
import random

# Version
VERSION = "0.3 Beta"

# Configuration - Store data in Documents folder
def get_data_dir():
    """Get the data directory in user's Documents folder."""
    documents = Path.home() / "Documents" / "ArabicVocabulary"
    documents.mkdir(parents=True, exist_ok=True)
    return documents

DATA_DIR = get_data_dir()
DATA_FILE = DATA_DIR / "vocabulary.json"

# Arabic keyboard layout
ARABIC_KEYBOARD = [
    ['١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩', '٠'],
    ['ض', 'ص', 'ث', 'ق', 'ف', 'غ', 'ع', 'ه', 'خ', 'ح', 'ج'],
    ['ش', 'س', 'ي', 'ب', 'ل', 'ا', 'ت', 'ن', 'م', 'ك', 'ة'],
    ['ئ', 'ء', 'ؤ', 'ر', 'ى', 'و', 'ز', 'ظ', 'ط', 'ذ', 'د'],
    ['آ', 'أ', 'إ', 'لا'],
]

DIACRITICS = [
    ('َ', 'ـَ'),   # Fatha
    ('ِ', 'ـِ'),   # Kasra
    ('ُ', 'ـُ'),   # Damma
    ('ْ', 'ـْ'),   # Sukun
    ('ّ', 'ـّ'),   # Shadda
    ('ً', 'ـً'),   # Tanwin Fatha
    ('ٍ', 'ـٍ'),   # Tanwin Kasra
    ('ٌ', 'ـٌ'),   # Tanwin Damma
]


class GeometricPatternWidget(QWidget):
    """Widget that draws an Islamic geometric pattern background."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
    def paintEvent(self, event):
        """Draw the geometric pattern."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background - Deep Teal
        painter.fillRect(self.rect(), QColor(6, 44, 48))
        
        # Pattern settings
        cell_size = 140
        
        # Draw repeating pattern
        for x in range(-cell_size, self.width() + cell_size, cell_size):
            for y in range(-cell_size, self.height() + cell_size, cell_size):
                self.draw_strapwork_pattern(painter, x + cell_size // 2, y + cell_size // 2, cell_size)
    
    def draw_strapwork_pattern(self, painter, cx, cy, size):
        """Draw an intricate 8-fold strapwork pattern."""
        radius = size * 0.5
        
        # 8-pointed star points (Rub el Hizb style)
        points = []
        for i in range(16):
            angle = math.pi * i / 8 - math.pi / 8
            # Alternating radii for star points vs clefts
            # Adjusted for a sharper star look similar to the image
            r = radius * 0.85 if i % 2 == 0 else radius * 0.55
            points.append(QPointF(
                cx + r * math.cos(angle),
                cy + r * math.sin(angle)
            ))
            
        # Create the star path
        path = QPainterPath()
        path.moveTo(points[0])
        for i in range(1, 16):
            path.lineTo(points[i])
        path.closeSubpath()
        
        # Draw "Strapwork" Effect
        # 1. Darker backing for depth
        painter.setPen(QPen(QColor(2, 28, 30, 80), 6)) 
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)
        
        # 2. Main Gold line
        painter.setPen(QPen(QColor(212, 170, 80, 40), 2))
        painter.drawPath(path)
        
        # 3. Inner details - A smaller rotated square or circle
        painter.setPen(QPen(QColor(212, 170, 80, 20), 1))
        painter.drawEllipse(QPointF(cx, cy), radius * 0.25, radius * 0.25)
        
        # 4. Connecting lines (grid)
        painter.setPen(QPen(QColor(212, 170, 80, 15), 1))
        rect_r = radius * 0.95
        painter.drawRect(int(cx - rect_r), int(cy - rect_r), int(rect_r * 2), int(rect_r * 2))


class MedallionLogo(QWidget):
    """A custom widget that draws a decorative Islamic medallion."""
    
    def __init__(self, size=64, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        cx, cy = self.width() / 2, self.height() / 2
        radius = min(cx, cy) - 4
        
        # 1. Outer Star (12-pointed)
        path = QPainterPath()
        points = 12
        for i in range(points * 2):
            angle = math.pi * i / points
            r = radius if i % 2 == 0 else radius * 0.8
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)
        path.closeSubpath()
        
        # Fill Green
        painter.fillPath(path, QColor(45, 170, 120))  # Emerald Green
        # Border Gold
        painter.strokePath(path, QPen(QColor(212, 170, 80), 2))
        
        # 2. Inner interlacing lines
        painter.setPen(QPen(QColor(255, 255, 255, 100), 1.5))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QPointF(cx, cy), radius * 0.6, radius * 0.6)
        
        # 3. Center Gold detail
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(212, 170, 80))
        painter.drawEllipse(QPointF(cx, cy), radius * 0.2, radius * 0.2)


# Stylesheet
STYLE = """
QMainWindow, QWidget {
    background-color: #062C30;
    color: #FFFFFF;
    font-family: 'Comic Sans MS', 'Chalkboard SE', 'Comic Neue', sans-serif;
}
QLabel {
    color: #FFFFFF;
}
QLineEdit, QTextEdit, QComboBox {
    background-color: #05363D;
    border: 1px solid #1A5C63;
    border-radius: 8px;
    padding: 8px 12px;
    color: #FFFFFF;
    font-size: 14px;
    min-height: 24px;
}
QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #D4AA50;
    background-color: #08454D;
}
QPushButton {
    background-color: #0E3F45;
    border: 1px solid #D4AA50;
    border-radius: 8px;
    padding: 10px 20px;
    color: #D4AA50;
    font-size: 14px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #1A5C63;
    color: #FFFFFF;
    border-color: #FFFFFF;
}
QPushButton#primaryBtn {
    background-color: #0E3F45;
    border: 2px solid #D4AA50;
    color: #FFFFFF;
    font-weight: bold;
    min-height: 24px;
}
QPushButton#primaryBtn:hover {
    background-color: #1A5C63;
    border-color: #FFFFFF;
    color: #FFFFFF;
}
QPushButton#dangerBtn {
    border: 1px solid #D64541;
    color: #D64541;
}
QPushButton#dangerBtn:hover {
    background-color: #D64541;
    color: #FFFFFF;
}
QScrollArea {
    border: none;
    background-color: transparent;
}
QComboBox {
    padding: 8px;
    border: 1px solid #D4AA50;
    color: #D4AA50;
}
QComboBox::drop-down {
    border: none;
    padding-right: 10px;
}
QComboBox QAbstractItemView {
    background-color: #0E3F45;
    color: #FDF6E3;
    selection-background-color: #1A5C63;
    border: 1px solid #D4AA50;
}
QDialog {
    background-color: #062C30;
}
"""

# Default starter words for new installations
DEFAULT_DATA = {
    "words": [
        {
            "id": "1",
            "arabic": "مرحبا",
            "transliteration": "marhaba",
            "english": "hello",
            "danish": "hej",
            "tags": ["greetings"],
            "notes": "Common greeting",
            "grammar": {}
        },
        {
            "id": "2", 
            "arabic": "شكرا",
            "transliteration": "shukran",
            "english": "thank you",
            "danish": "tak",
            "tags": ["greetings"],
            "notes": "",
            "grammar": {}
        },
        {
            "id": "3",
            "arabic": "نعم",
            "transliteration": "na'am",
            "english": "yes",
            "danish": "ja",
            "tags": ["basics"],
            "notes": "",
            "grammar": {}
        },
        {
            "id": "4",
            "arabic": "لا",
            "transliteration": "la",
            "english": "no", 
            "danish": "nej",
            "tags": ["basics"],
            "notes": "",
            "grammar": {}
        },
        {
            "id": "5",
            "arabic": "ماء",
            "transliteration": "maa'",
            "english": "water",
            "danish": "vand",
            "tags": ["food & drink"],
            "notes": "",
            "grammar": {}
        }
    ],
    "tags": ["greetings", "basics", "food & drink"],
    "word_groups": [],
    "settings": {
        "languages": ["English", "Danish"]
    }
}

# Grammar options
GRAMMAR_OPTIONS = {
    "person": ["", "1st", "2nd", "3rd"],
    "number": ["", "singular", "dual", "plural"],
    "gender": ["", "masculine", "feminine"],
    "tense": ["", "past", "present", "future", "imperative"],
    "form": ["", "Form I", "Form II", "Form III", "Form IV", "Form V", "Form VI", "Form VII", "Form VIII", "Form IX", "Form X"]
}


def load_data():
    """Load vocabulary data from JSON file."""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create default data for new installations
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()


def save_data(data):
    """Save vocabulary data to JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class ArabicKeyboard(QDialog):
    """Floating Arabic keyboard dialog."""
    
    def __init__(self, parent, target_entry):
        super().__init__(parent)
        self.target_entry = target_entry
        self.setWindowTitle("Arabic Keyboard")
        self.setFixedSize(850, 420)
        self.setStyleSheet("background-color: #062C30;")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        # Letter rows
        for row in ARABIC_KEYBOARD:
            row_layout = QHBoxLayout()
            row_layout.setSpacing(4)
            for char in row:
                btn = QPushButton(char)
                btn.setFixedSize(65, 55)
                btn.setFont(QFont('Arial', 26))
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #0E3F45;
                        color: #FDF6E3;
                        border-radius: 8px;
                        border: 1px solid #1A5C63;
                    }
                    QPushButton:hover {
                        background-color: #1A5C63;
                        color: #D4AA50;
                        border-color: #D4AA50;
                    }
                """)
                btn.clicked.connect(lambda checked, c=char: self.insert_char(c))
                row_layout.addWidget(btn)
            row_layout.addStretch()
            layout.addLayout(row_layout)
        
        # Space and backspace row
        space_row = QHBoxLayout()
        space_row.setSpacing(4)
        
        space_btn = QPushButton("Space")
        space_btn.setFixedSize(120, 40)
        space_btn.clicked.connect(lambda: self.insert_char(' '))
        space_row.addWidget(space_btn)
        
        backspace_btn = QPushButton("⌫ Backspace")
        backspace_btn.setFixedSize(120, 40)
        backspace_btn.clicked.connect(self.backspace)
        space_row.addWidget(backspace_btn)
        
        space_row.addStretch()
        layout.addLayout(space_row)
        
        # Diacritics row
        diac_label = QLabel("Tashkeel (diacritics):")
        diac_label.setStyleSheet("color: #8b9bb4; font-size: 14px;")
        layout.addWidget(diac_label)
        
        diac_row = QHBoxLayout()
        diac_row.setSpacing(4)
        for char, display in DIACRITICS:
            btn = QPushButton(display)
            btn.setFixedSize(70, 65)
            btn.setFont(QFont('Arial', 38))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #0E3F45;
                    color: #D4AA50;
                    border-radius: 8px;
                    border: 1px solid #1A5C63;
                }
                QPushButton:hover {
                    background-color: #1A5C63;
                    border-color: #D4AA50;
                }
            """)
            btn.clicked.connect(lambda checked, c=char: self.insert_char(c))
            diac_row.addWidget(btn)
        diac_row.addStretch()
        layout.addLayout(diac_row)
    
    def insert_char(self, char):
        """Insert character at cursor position."""
        if self.target_entry:
            cursor_pos = self.target_entry.cursorPosition()
            text = self.target_entry.text()
            new_text = text[:cursor_pos] + char + text[cursor_pos:]
            self.target_entry.setText(new_text)
            self.target_entry.setCursorPosition(cursor_pos + len(char))
            self.target_entry.setFocus()
    
    def backspace(self):
        """Delete character before cursor."""
        if self.target_entry:
            cursor_pos = self.target_entry.cursorPosition()
            if cursor_pos > 0:
                text = self.target_entry.text()
                new_text = text[:cursor_pos-1] + text[cursor_pos:]
                self.target_entry.setText(new_text)
                self.target_entry.setCursorPosition(cursor_pos - 1)
            self.target_entry.setFocus()


class SettingsWidget(QWidget):
    """Widget for application settings."""
    
    def __init__(self, data, on_save, on_import):
        super().__init__()
        self.data = data
        self.on_save = on_save
        self.on_import = on_import
        self.available_langs = ["English", "Danish", "German", "Spanish", "Russian", "Italian"]
        self.checkboxes = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        # Title
        title = QLabel("⚙️ Settings")
        title.setFont(QFont('Comic Sans MS', 24))
        title.setStyleSheet("color: #D4AA50;")
        layout.addWidget(title)
        
        # --- Data Management Section ---
        data_group = QFrame()
        data_group.setStyleSheet("""
            QFrame {
                background-color: #05363D;
                border: 1px solid #1A5C63;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        data_layout = QVBoxLayout(data_group)
        
        data_label = QLabel("Data Management")
        data_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        data_label.setStyleSheet("color: #D4AA50; border: none;")
        data_layout.addWidget(data_label)
        
        export_btn = QPushButton("📤 Export Vocabulary (JSON)")
        export_btn.clicked.connect(self.export_json)
        data_layout.addWidget(export_btn)
        
        import_btn = QPushButton("📥 Import Vocabulary (JSON)")
        import_btn.clicked.connect(self.import_json)
        data_layout.addWidget(import_btn)
        
        layout.addWidget(data_group)
        
        # --- Language Selection Section ---
        lang_group = QFrame()
        lang_group.setStyleSheet("""
            QFrame {
                background-color: #05363D;
                border: 1px solid #1A5C63;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        lang_layout = QVBoxLayout(lang_group)
        
        lang_label = QLabel("Active Languages")
        lang_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        lang_label.setStyleSheet("color: #D4AA50; border: none;")
        lang_layout.addWidget(lang_label)
        
        desc_label = QLabel("Select up to 2 languages to display:")
        desc_label.setStyleSheet("color: #A0C4C8; border: none;")
        lang_layout.addWidget(desc_label)
        
        # Checkboxes
        self.lang_container = QWidget()
        self.lang_container.setStyleSheet("border: none; background: transparent;")
        self.lang_grid = QGridLayout(self.lang_container)
        
        current_langs = self.data.get('settings', {}).get('languages', ["English", "Danish"])
        
        # Combine default available langs with any custom ones present in settings
        all_langs_to_show = sorted(list(set(self.available_langs + current_langs)))
        
        for idx, lang in enumerate(all_langs_to_show):
            cb = QCheckBox(lang)
            cb.setStyleSheet("color: #FDF6E3; spacing: 8px;")
            if lang in current_langs:
                cb.setChecked(True)
            cb.stateChanged.connect(self.check_selection_limit)
            self.checkboxes[lang] = cb
            self.lang_grid.addWidget(cb, idx // 2, idx % 2)
            
        lang_layout.addWidget(self.lang_container)
        
        # Add Custom Language
        add_lang_btn = QPushButton("+ Add Custom Language")
        add_lang_btn.setFixedWidth(200)
        add_lang_btn.clicked.connect(self.add_custom_language)
        lang_layout.addWidget(add_lang_btn)
        
        # Save Languages Button
        save_lang_btn = QPushButton("Save Language Preferences")
        save_lang_btn.setObjectName("primaryBtn")
        save_lang_btn.clicked.connect(self.save_languages)
        lang_layout.addWidget(save_lang_btn)
        
        layout.addWidget(lang_group)
        layout.addStretch()
    
    def check_selection_limit(self):
        """Ensure max 2 languages are selected."""
        selected = [cb for cb in self.checkboxes.values() if cb.isChecked()]
        if len(selected) > 2:
            sender = self.sender()
            sender.setChecked(False)
            QMessageBox.warning(self, "Limit Reached", "You can select a maximum of 2 languages.")
    
    def add_custom_language(self):
        """Add a custom language to the list."""
        lang, ok = QInputDialog.getText(self, "Add Language", "Language Name:")
        if ok and lang:
            lang = lang.strip().title()
            if lang and lang not in self.checkboxes:
                cb = QCheckBox(lang)
                cb.setStyleSheet("color: #FDF6E3; spacing: 8px;")
                cb.setChecked(True) # Auto-select new language
                cb.stateChanged.connect(self.check_selection_limit)
                
                # Check limit before adding if we are auto-selecting
                selected_count = sum(1 for c in self.checkboxes.values() if c.isChecked())
                if selected_count >= 2:
                     cb.setChecked(False)
                
                self.checkboxes[lang] = cb
                count = self.lang_grid.count()
                self.lang_grid.addWidget(cb, count // 2, count % 2)
    
    def save_languages(self):
        """Save the selected languages to settings."""
        selected = [lang for lang, cb in self.checkboxes.items() if cb.isChecked()]
        
        if not selected:
             QMessageBox.warning(self, "Error", "Please select at least one language.")
             return
             
        if 'settings' not in self.data:
            self.data['settings'] = {}
        
        self.data['settings']['languages'] = selected
        
        # Persist changes
        self.on_save(self.data)
        QMessageBox.information(self, "Success", "Language preferences saved! Restart or navigate away to see changes.")

    def export_json(self):
        """Export data."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Vocabulary", 
            str(Path.home() / "vocabulary_export.json"), 
            "JSON Files (*.json)"
        )
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            QMessageBox.information(self, "Success", f"Data exported to {file_path}")
            
    def import_json(self):
        """Import data."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Vocabulary", 
            str(Path.home()), 
            "JSON Files (*.json)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    new_data = json.load(f)
                
                if self.on_import(new_data):
                    QMessageBox.information(self, "Success", "Vocabulary imported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import file: {str(e)}")


class WordCard(QFrame):
    """A card displaying a single vocabulary word."""
    
    def __init__(self, word, on_edit, on_delete, languages=None):
        super().__init__()
        self.word = word
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.languages = languages or ["English", "Danish"]
        
        self.setStyleSheet("""
            WordCard {
                background-color: #0E3F45;
                border-radius: 16px;
                border: 1px solid #1A5C63;
                padding: 15px;
            }
        """)
        self.setMinimumWidth(350)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Arabic text
        arabic_text = word.get('arabic_diacritics') or word.get('arabic', '')
        arabic_label = QLabel(arabic_text)
        arabic_label.setFont(QFont('Arial', 32))
        arabic_label.setStyleSheet("color: #D4AA50; font-family: 'Arial';")
        arabic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(arabic_label)
        
        # Transliteration
        if word.get('transliteration'):
            trans_label = QLabel(word['transliteration'])
            trans_label.setStyleSheet("color: #A0C4C8; font-style: italic;")
            trans_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(trans_label)
        
        # Translations frame
        trans_frame = QFrame()
        trans_frame.setStyleSheet("background-color: #05363D; border-radius: 8px; padding: 10px;")
        trans_layout = QVBoxLayout(trans_frame)
        trans_layout.setSpacing(5)
        
        # Dynamic Languages
        for lang in self.languages:
            lang_key = lang.lower()
            lang_code = lang[:2].upper()
            
            row = QHBoxLayout()
            label = QLabel(lang_code)
            label.setStyleSheet("color: #38B2AC; font-weight: bold; font-size: 11px;")
            label.setFixedWidth(30)
            row.addWidget(label)
            
            text = QLabel(word.get(lang_key, ''))
            row.addWidget(text)
            row.addStretch()
            trans_layout.addLayout(row)
        
        layout.addWidget(trans_frame)
        
        # Grammar info (if any is set)
        grammar = word.get('grammar', {})
        grammar_parts = []
        if grammar.get('group'):
            grammar_parts.append(f"Group: {grammar['group']}")
        for key in ['person', 'number', 'gender', 'tense', 'form']:
            if grammar.get(key):
                grammar_parts.append(grammar[key])
        
        if grammar_parts:
            grammar_label = QLabel(' • '.join(grammar_parts))
            grammar_label.setStyleSheet("""
                color: #A0C4C8;
                font-size: 11px;
                font-style: italic;
                padding: 5px;
                background-color: #05363D;
                border-radius: 4px;
            """)
            grammar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(grammar_label)
        
        # Tags
        if word.get('tags'):
            tags_layout = QHBoxLayout()
            for tag in word['tags']:
                tag_label = QLabel(tag)
                tag_label.setStyleSheet("""
                    background-color: #062C30;
                    color: #D4AA50;
                    padding: 3px 8px;
                    border-radius: 4px;
                    font-size: 11px;
                    border: 1px solid #1A5C63;
                """)
                tags_layout.addWidget(tag_label)
            tags_layout.addStretch()
            layout.addLayout(tags_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        edit_btn = QPushButton("Edit")
        edit_btn.setFixedWidth(80)
        edit_btn.clicked.connect(lambda: self.on_edit(self.word))
        btn_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Delete")
        delete_btn.setObjectName("dangerBtn")
        delete_btn.setFixedWidth(80)
        delete_btn.clicked.connect(lambda: self.on_delete(self.word['id']))
        btn_layout.addWidget(delete_btn)
        
        layout.addLayout(btn_layout)


class QuizCard(QFrame):
    """A card for quiz mode - shows word with hidden field to guess."""
    
    def __init__(self, word, quiz_mode, on_check, keyboard_ref):
        super().__init__()
        self.word = word
        self.quiz_mode = quiz_mode  # 'arabic' or 'translation'
        self.on_check = on_check
        self.keyboard_ref = keyboard_ref
        self.revealed = False
        
        self.setStyleSheet("""
            QuizCard {
                background-color: #0E3F45;
                border-radius: 16px;
                border: 1px solid #1A5C63;
                padding: 15px;
            }
        """)
        self.setMinimumWidth(320)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        if quiz_mode == 'arabic':
            # Show English/Danish, hide Arabic
            # English
            en_label = QLabel(f"EN: {word.get('english', '')}")
            en_label.setStyleSheet("color: #A0C4C8; font-size: 16px;")
            en_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(en_label)
            
            # Danish
            da_label = QLabel(f"DA: {word.get('danish', '')}")
            da_label.setStyleSheet("color: #A0C4C8; font-size: 16px;")
            da_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(da_label)
            
            # Input for Arabic
            layout.addWidget(QLabel("Write in Arabic:"))
            input_row = QHBoxLayout()
            self.answer_entry = QLineEdit()
            self.answer_entry.setFont(QFont('Arial', 18))
            self.answer_entry.setStyleSheet("font-family: 'Arial'; text-align: right;")
            self.answer_entry.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.answer_entry.returnPressed.connect(self.check_answer)
            input_row.addWidget(self.answer_entry)
            
            kb_btn = QPushButton("⌨")
            kb_btn.setFixedSize(40, 40)
            kb_btn.clicked.connect(lambda: self.show_keyboard(self.answer_entry))
            input_row.addWidget(kb_btn)
            layout.addLayout(input_row)
            
            self.correct_answer = word.get('arabic', '')
            
        else:  # translation mode
            # Show Arabic, hide English/Danish
            arabic_text = word.get('arabic_diacritics') or word.get('arabic', '')
            arabic_label = QLabel(arabic_text)
            arabic_label.setFont(QFont('Arial', 28))
            arabic_label.setStyleSheet("color: #D4AA50; font-family: 'Arial';")
            arabic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(arabic_label)
            
            if word.get('transliteration'):
                trans_label = QLabel(word['transliteration'])
                trans_label.setStyleSheet("color: #A0C4C8; font-style: italic;")
                trans_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(trans_label)
            
            # Input for English
            layout.addWidget(QLabel("Write in English:"))
            self.en_entry = QLineEdit()
            self.en_entry.returnPressed.connect(self.check_answer)
            layout.addWidget(self.en_entry)
            
            # Input for Danish
            layout.addWidget(QLabel("Write in Danish:"))
            self.da_entry = QLineEdit()
            self.da_entry.returnPressed.connect(self.check_answer)
            layout.addWidget(self.da_entry)
            
            self.correct_en = word.get('english', '').lower()
            self.correct_da = word.get('danish', '').lower()
        
        # Result label (hidden initially)
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("font-size: 14px; padding: 5px;")
        self.result_label.hide()
        layout.addWidget(self.result_label)
        
        # Check button
        self.check_btn = QPushButton("Check Answer")
        self.check_btn.clicked.connect(self.check_answer)
        layout.addWidget(self.check_btn)
    
    def show_keyboard(self, target):
        """Show Arabic keyboard."""
        if self.keyboard_ref:
            self.keyboard_ref(target)
    
    def check_answer(self):
        """Check if the answer is correct."""
        if self.revealed:
            return
            
        self.revealed = True
        correct = False
        
        if self.quiz_mode == 'arabic':
            user_answer = self.answer_entry.text().strip()
            # Compare ignoring diacritics for leniency
            correct = user_answer == self.correct_answer or self.normalize_arabic(user_answer) == self.normalize_arabic(self.correct_answer)
            
            if correct:
                self.result_label.setText("✓ Correct!")
                self.result_label.setStyleSheet("color: #2ECC71; font-size: 14px; font-weight: bold;")
            else:
                self.result_label.setText(f"✗ Answer: {self.correct_answer}")
                self.result_label.setStyleSheet("color: #E74C3C; font-size: 14px; font-weight: bold;")
        else:
            # Translation mode check
            results = []
            all_correct = True
            
            # Check English/Danish explicitly if they were the target fields
            # But the card might have been built dynamically. 
            # Revert to simpler logic: 
            # We need to know WHICH fields were presented in the UI to check them.
            # Assuming the standard fields `en_entry` and `da_entry` exist for backward compat
            # or we need to refactor QuizCard completely for dynamic langs.
            
            # For this iteration, let's keep the hardcoded English/Danish in QuizCard for now 
            # or safer: skip quiz refactor for dynamic languages in this step since the user 
            # didn't explicitly ask for dynamic quiz languages yet, mainly "select desired languages" for display.
            # However, to avoid breakage if fields are missing:
            
            user_en = getattr(self, 'en_entry', QLineEdit()).text().strip().lower()
            user_da = getattr(self, 'da_entry', QLineEdit()).text().strip().lower()
            
            en_correct = user_en == self.correct_en
            da_correct = user_da == self.correct_da
            
            if en_correct and da_correct:
                self.result_label.setText("✓ Both correct!")
                self.result_label.setStyleSheet("color: #2ECC71; font-size: 14px; font-weight: bold;")
                correct = True
            elif en_correct:
                self.result_label.setText(f"EN ✓ | DA ✗ ({self.correct_da})")
                self.result_label.setStyleSheet("color: #F39C12; font-size: 14px; font-weight: bold;")
            elif da_correct:
                self.result_label.setText(f"EN ✗ ({self.correct_en}) | DA ✓")
                self.result_label.setStyleSheet("color: #F39C12; font-size: 14px; font-weight: bold;")
            else:
                self.result_label.setText(f"EN: {self.correct_en} | DA: {self.correct_da}")
                self.result_label.setStyleSheet("color: #E74C3C; font-size: 14px; font-weight: bold;")
        
        self.result_label.show()
        self.check_btn.setEnabled(False)
        self.check_btn.setText("Answered")
        
        if self.on_check:
            self.on_check(correct)
    
    def normalize_arabic(self, text):
        """Normalize Arabic text by removing diacritics."""
        diacritics = 'ًٌٍَُِّْ'
        return ''.join(c for c in text if c not in diacritics)


class QuizWidget(QWidget):
    """Widget for the quiz/game mode."""
    
    def __init__(self, data, get_keyboard_func):
        super().__init__()
        self.data = data
        self.get_keyboard = get_keyboard_func
        self.quiz_words = []
        self.score = 0
        self.total = 0
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("📝 Quiz Mode")
        title.setFont(QFont('Comic Sans MS', 24))
        title.setStyleSheet("color: #D4AA50;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Settings panel
        settings_frame = QFrame()
        settings_frame.setStyleSheet("""
            QFrame {
                background-color: #05363D;
                border-radius: 12px;
                border: 1px solid #1A5C63;
                padding: 15px;
            }
        """)
        settings_layout = QVBoxLayout(settings_frame)
        
        # Tag selection
        tag_row = QHBoxLayout()
        tag_row.addWidget(QLabel("Filter by tag:"))
        self.quiz_tag_combo = QComboBox()
        self.quiz_tag_combo.setFixedWidth(180)
        self.quiz_tag_combo.addItem("All Words")
        self.quiz_tag_combo.addItems(self.data.get('tags', []))
        tag_row.addWidget(self.quiz_tag_combo)
        tag_row.addStretch()
        settings_layout.addLayout(tag_row)
        
        # Quiz mode selection
        mode_row = QHBoxLayout()
        mode_row.addWidget(QLabel("Quiz type:"))
        
        self.mode_group = QButtonGroup(self)
        self.arabic_mode = QRadioButton("Guess Arabic")
        self.arabic_mode.setChecked(True)
        self.arabic_mode.setStyleSheet("color: #A0C4C8;")
        self.mode_group.addButton(self.arabic_mode)
        mode_row.addWidget(self.arabic_mode)
        
        self.trans_mode = QRadioButton("Guess English/Danish")
        self.trans_mode.setStyleSheet("color: #A0C4C8;")
        self.mode_group.addButton(self.trans_mode)
        mode_row.addWidget(self.trans_mode)
        
        mode_row.addStretch()
        settings_layout.addLayout(mode_row)
        
        layout.addWidget(settings_frame)
        
        # Start button
        self.start_btn = QPushButton("Start Quiz (10 words)")
        self.start_btn.setObjectName("primaryBtn")
        self.start_btn.clicked.connect(self.start_quiz)
        layout.addWidget(self.start_btn)
        
        # Score display
        self.score_label = QLabel("")
        self.score_label.setStyleSheet("color: #A0C4C8; font-size: 16px;")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.score_label)
        
        # Quiz cards scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        
        self.quiz_container = QWidget()
        self.quiz_container.setStyleSheet("background: transparent;")
        self.quiz_layout = QVBoxLayout(self.quiz_container)
        self.quiz_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.quiz_layout.setSpacing(15)
        
        scroll_area.setWidget(self.quiz_container)
        layout.addWidget(scroll_area)
    
    def update_tags(self, tags):
        """Update available tags."""
        current = self.quiz_tag_combo.currentText()
        self.quiz_tag_combo.clear()
        self.quiz_tag_combo.addItem("All Words")
        self.quiz_tag_combo.addItems(tags)
        idx = self.quiz_tag_combo.findText(current)
        if idx >= 0:
            self.quiz_tag_combo.setCurrentIndex(idx)
    
    def start_quiz(self):
        """Start a new quiz."""
        # Clear previous quiz
        while self.quiz_layout.count():
            item = self.quiz_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Filter words by tag
        tag = self.quiz_tag_combo.currentText()
        if tag == "All Words":
            available = self.data['words']
        else:
            available = [w for w in self.data['words'] if tag in w.get('tags', [])]
        
        if not available:
            self.score_label.setText("No words available for this tag!")
            return
        
        # Select up to 10 random words
        self.quiz_words = random.sample(available, min(10, len(available)))
        self.score = 0
        self.total = len(self.quiz_words)
        self.answered = 0
        
        quiz_mode = 'arabic' if self.arabic_mode.isChecked() else 'translation'
        self.score_label.setText(f"Score: 0/{self.total}")
        
        # Create quiz cards
        for word in self.quiz_words:
            card = QuizCard(word, quiz_mode, self.on_answer_checked, self.get_keyboard)
            self.quiz_layout.addWidget(card)
        
        self.start_btn.setText("Restart Quiz")
    
    def on_answer_checked(self, correct):
        """Called when an answer is checked."""
        self.answered += 1
        if correct:
            self.score += 1
        
        self.score_label.setText(f"Score: {self.score}/{self.total}")
        
        if self.answered >= self.total:
            percentage = int(self.score / self.total * 100)
            if percentage >= 80:
                emoji = "🎉"
            elif percentage >= 50:
                emoji = "👍"
            else:
                emoji = "📚"
            self.score_label.setText(f"{emoji} Final Score: {self.score}/{self.total} ({percentage}%)")


class AddEditDialog(QDialog):
    """Dialog for adding or editing a word."""
    
    def __init__(self, parent, word=None, tags=None, on_save=None, languages=None):
        super().__init__(parent)
        self.word = word or {}
        self.all_tags = tags or []
        self.on_save_callback = on_save
        self.languages = languages or ["English", "Danish"]
        self.selected_tags = list(self.word.get('tags', []))
        self.keyboard = None
        self.lang_entries = {}
        
        self.setWindowTitle("Edit Word" if word else "Add New Word")
        self.setFixedSize(550, 850)
        self.setStyleSheet(STYLE)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Arabic input
        layout.addWidget(QLabel("Arabic *"))
        arabic_row = QHBoxLayout()
        self.arabic_entry = QLineEdit(self.word.get('arabic', ''))
        self.arabic_entry.setFont(QFont('Arial', 18))
        self.arabic_entry.setStyleSheet("color: #D4AA50; font-family: 'Arial';")
        self.arabic_entry.setAlignment(Qt.AlignmentFlag.AlignRight)
        arabic_row.addWidget(self.arabic_entry)
        
        kb_btn = QPushButton("⌨️")
        kb_btn.setFixedWidth(45)
        kb_btn.clicked.connect(lambda: self.show_keyboard(self.arabic_entry))
        arabic_row.addWidget(kb_btn)
        layout.addLayout(arabic_row)
        
        # Arabic with diacritics
        layout.addWidget(QLabel("Arabic with Diacritics (optional)"))
        diac_row = QHBoxLayout()
        self.diacritics_entry = QLineEdit(self.word.get('arabic_diacritics', ''))
        self.diacritics_entry.setFont(QFont('Arial', 18))
        self.diacritics_entry.setStyleSheet("color: #D4AA50; font-family: 'Arial';")
        self.diacritics_entry.setAlignment(Qt.AlignmentFlag.AlignRight)
        diac_row.addWidget(self.diacritics_entry)
        
        kb_btn2 = QPushButton("⌨️")
        kb_btn2.setFixedWidth(45)
        kb_btn2.clicked.connect(lambda: self.show_keyboard(self.diacritics_entry))
        diac_row.addWidget(kb_btn2)
        layout.addLayout(diac_row)
        
        # Transliteration
        layout.addWidget(QLabel("Transliteration (optional)"))
        self.transliteration_entry = QLineEdit(self.word.get('transliteration', ''))
        layout.addWidget(self.transliteration_entry)
        
        # Dynamic Languages
        for lang in self.languages:
            lang_key = lang.lower()
            layout.addWidget(QLabel(f"{lang} *"))
            entry = QLineEdit(self.word.get(lang_key, ''))
            layout.addWidget(entry)
            self.lang_entries[lang_key] = entry
        
        # Grammar section
        grammar_label = QLabel("Grammar (for verb conjugations)")
        grammar_label.setStyleSheet("color: #D4AA50; font-weight: bold; margin-top: 10px;")
        layout.addWidget(grammar_label)
        
        grammar = self.word.get('grammar', {})
        
        # Word group (to link conjugations)
        group_row = QHBoxLayout()
        group_row.addWidget(QLabel("Word Group:"))
        self.group_entry = QLineEdit(grammar.get('group', ''))
        self.group_entry.setPlaceholderText("e.g., 'كتب - to write' (links related forms)")
        group_row.addWidget(self.group_entry)
        layout.addLayout(group_row)
        
        # Grammar dropdowns row 1
        grammar_row1 = QHBoxLayout()
        
        grammar_row1.addWidget(QLabel("Person:"))
        self.person_combo = QComboBox()
        self.person_combo.addItems(GRAMMAR_OPTIONS["person"])
        self.person_combo.setCurrentText(grammar.get('person', ''))
        self.person_combo.setFixedWidth(80)
        grammar_row1.addWidget(self.person_combo)
        
        grammar_row1.addWidget(QLabel("Number:"))
        self.number_combo = QComboBox()
        self.number_combo.addItems(GRAMMAR_OPTIONS["number"])
        self.number_combo.setCurrentText(grammar.get('number', ''))
        self.number_combo.setFixedWidth(90)
        grammar_row1.addWidget(self.number_combo)
        
        grammar_row1.addWidget(QLabel("Gender:"))
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(GRAMMAR_OPTIONS["gender"])
        self.gender_combo.setCurrentText(grammar.get('gender', ''))
        self.gender_combo.setFixedWidth(100)
        grammar_row1.addWidget(self.gender_combo)
        
        grammar_row1.addStretch()
        layout.addLayout(grammar_row1)
        
        # Grammar dropdowns row 2
        grammar_row2 = QHBoxLayout()
        
        grammar_row2.addWidget(QLabel("Tense:"))
        self.tense_combo = QComboBox()
        self.tense_combo.addItems(GRAMMAR_OPTIONS["tense"])
        self.tense_combo.setCurrentText(grammar.get('tense', ''))
        self.tense_combo.setFixedWidth(100)
        grammar_row2.addWidget(self.tense_combo)
        
        grammar_row2.addWidget(QLabel("Form:"))
        self.form_combo = QComboBox()
        self.form_combo.addItems(GRAMMAR_OPTIONS["form"])
        self.form_combo.setCurrentText(grammar.get('form', ''))
        self.form_combo.setFixedWidth(100)
        grammar_row2.addWidget(self.form_combo)
        
        grammar_row2.addStretch()
        layout.addLayout(grammar_row2)
        
        # Tags
        tags_label = QLabel("Tags (select existing or add new)")
        layout.addWidget(tags_label)
        self.tags_layout = QHBoxLayout()
        self.render_selected_tags()
        layout.addLayout(self.tags_layout)
        
        # Existing tags dropdown
        self.tag_combo = QComboBox()
        self.tag_combo.addItem("Select existing tag...")
        self.tag_combo.addItems(self.all_tags)
        self.tag_combo.currentTextChanged.connect(self.add_existing_tag)
        layout.addWidget(self.tag_combo)
        
        # New tag input
        new_tag_row = QHBoxLayout()
        self.new_tag_entry = QLineEdit()
        self.new_tag_entry.setPlaceholderText("Type new tag name...")
        self.new_tag_entry.returnPressed.connect(self.add_new_tag)
        new_tag_row.addWidget(self.new_tag_entry)
        
        add_tag_btn = QPushButton("+ Add Tag")
        add_tag_btn.setFixedWidth(100)
        add_tag_btn.clicked.connect(self.add_new_tag)
        new_tag_row.addWidget(add_tag_btn)
        layout.addLayout(new_tag_row)
        
        # Notes
        layout.addWidget(QLabel("Notes (optional)"))
        self.notes_entry = QTextEdit()
        self.notes_entry.setMaximumHeight(60)
        self.notes_entry.setText(self.word.get('notes', ''))
        layout.addWidget(self.notes_entry)
        
        layout.addStretch()
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save Word")
        save_btn.setObjectName("primaryBtn")
        save_btn.clicked.connect(self.save)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
    
    def render_selected_tags(self):
        """Render selected tags."""
        # Clear existing
        while self.tags_layout.count():
            item = self.tags_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        for tag in self.selected_tags:
            tag_frame = QFrame()
            tag_frame.setStyleSheet("background-color: #0E3F45; border-radius: 4px; border: 1px solid #1A5C63;")
            tag_layout = QHBoxLayout(tag_frame)
            tag_layout.setContentsMargins(8, 4, 4, 4)
            tag_layout.setSpacing(5)
            
            tag_label = QLabel(tag)
            tag_label.setStyleSheet("color: #D4AA50; font-size: 12px;")
            tag_layout.addWidget(tag_label)
            
            remove_btn = QPushButton("×")
            remove_btn.setFixedSize(20, 20)
            remove_btn.setStyleSheet("color: #D4AA50; font-size: 14px; padding: 0; border: none; background: transparent;")
            remove_btn.clicked.connect(lambda checked, t=tag: self.remove_tag(t))
            tag_layout.addWidget(remove_btn)
            
            self.tags_layout.addWidget(tag_frame)
        
        self.tags_layout.addStretch()
    
    def add_existing_tag(self, tag):
        """Add existing tag to selected tags."""
        if tag and tag != "Select existing tag..." and tag not in self.selected_tags:
            self.selected_tags.append(tag)
            self.render_selected_tags()
        if hasattr(self, 'tag_combo'):
            self.tag_combo.setCurrentIndex(0)
    
    def add_new_tag(self):
        """Add a new custom tag."""
        tag = self.new_tag_entry.text().strip().lower()
        if tag and tag not in self.selected_tags:
            self.selected_tags.append(tag)
            # Also add to the dropdown for future use
            if tag not in self.all_tags:
                self.all_tags.append(tag)
                self.tag_combo.addItem(tag)
            self.render_selected_tags()
        self.new_tag_entry.clear()
    
    def remove_tag(self, tag):
        """Remove tag from selected tags."""
        if tag in self.selected_tags:
            self.selected_tags.remove(tag)
            self.render_selected_tags()
    
    def show_keyboard(self, target_entry):
        """Show Arabic keyboard."""
        if self.keyboard:
            self.keyboard.target_entry = target_entry
            self.keyboard.show()
            self.keyboard.raise_()
        else:
            self.keyboard = ArabicKeyboard(self, target_entry)
            self.keyboard.show()
    
    def save(self):
        """Save the word."""
        arabic = self.arabic_entry.text().strip()
        
        # Validate dynamic language fields
        lang_values = {}
        for lang_key, entry in self.lang_entries.items():
            val = entry.text().strip()
            if not val:
                 QMessageBox.warning(self, "Error", f"{lang_key.title()} is required.")
                 return
            lang_values[lang_key] = val
        
        if not arabic:
            QMessageBox.warning(self, "Error", "Arabic is required.")
            return
        
        now = datetime.utcnow().isoformat() + 'Z'
        
        # Build grammar data
        grammar_data = {
            'group': self.group_entry.text().strip(),
            'person': self.person_combo.currentText(),
            'number': self.number_combo.currentText(),
            'gender': self.gender_combo.currentText(),
            'tense': self.tense_combo.currentText(),
            'form': self.form_combo.currentText()
        }
        
        word_data = {
            'id': self.word.get('id', str(uuid.uuid4())),
            'arabic': arabic,
            'arabic_diacritics': self.diacritics_entry.text().strip(),
            'transliteration': self.transliteration_entry.text().strip(),
            **lang_values,
            'tags': self.selected_tags,
            'grammar': grammar_data,
            'notes': self.notes_entry.toPlainText().strip(),
            'created_at': self.word.get('created_at', now),
            'updated_at': now
        }
        
        if self.on_save_callback:
            self.on_save_callback(word_data)
        
        if self.keyboard:
            self.keyboard.close()
        self.accept()


class ArabicVocabularyApp(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Arabic Vocabulary - {VERSION}")
        self.setMinimumSize(900, 700)
        self.setStyleSheet(STYLE)
        
        # Data
        self.data = load_data()
        
        # Ensure 'settings' key exists for legacy data
        if 'settings' not in self.data:
            self.data['settings'] = {"languages": ["English", "Danish"]}
            
        self.filtered_words = self.data['words']
        self.keyboard = None
        
        self.setup_ui()
        self.refresh_words()
    
    def setup_ui(self):
        """Set up the main UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QFrame()
        header.setStyleSheet("background-color: #05363D; border-bottom: 2px solid #D4AA50;")
        header.setFixedHeight(80)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(25, 15, 25, 15)
        
        # Logo
        logo_layout = QHBoxLayout()
        
        # Medallion Icon
        self.medallion = MedallionLogo(size=56)
        logo_layout.addWidget(self.medallion)
        logo_layout.addSpacing(12)
        
        logo_arabic = QLabel("عربي")
        logo_arabic.setFont(QFont('Arial', 32)) 
        logo_arabic.setStyleSheet("color: #D4AA50; font-family: 'Arial';")
        logo_layout.addWidget(logo_arabic)
        
        logo_text = QLabel("Vocabulary")
        logo_text.setFont(QFont('Comic Sans MS', 22))
        logo_text.setStyleSheet("color: #A0C4C8; letter-spacing: 1px; font-family: 'Comic Sans MS', 'Chalkboard SE';")
        logo_layout.addWidget(logo_text)
        logo_layout.addStretch()
        
        header_layout.addLayout(logo_layout)
        
        # Add button
        self.add_btn = QPushButton("+ Add Word")
        self.add_btn.setObjectName("primaryBtn")
        self.add_btn.clicked.connect(self.add_word)
        header_layout.addWidget(self.add_btn)
        
        main_layout.addWidget(header)
        
        # Main content area (sidebar + content)
        content_wrapper = QHBoxLayout()
        content_wrapper.setSpacing(0)
        content_wrapper.setContentsMargins(0, 0, 0, 0)
        
        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("""
            QFrame {
                background-color: #05363D;
                border-right: 1px solid #1A5C63;
            }
        """)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(10)
        
        # Mode buttons
        self.library_btn = QPushButton("📚 Library")
        self.library_btn.setStyleSheet("""
            QPushButton {
                background-color: #D4AA50;
                color: #062C30;
                font-weight: bold;
                padding: 15px;
                border-radius: 8px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #E5BB61;
            }
        """)
        self.library_btn.clicked.connect(lambda: self.switch_mode('library'))
        sidebar_layout.addWidget(self.library_btn)
        
        self.quiz_btn = QPushButton("📝 Quiz")
        self.quiz_btn.setStyleSheet("""
            QPushButton {
                background-color: #0E3F45;
                color: #A0C4C8;
                font-weight: bold;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #1A5C63;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #1A5C63;
                color: #FFFFFF;
            }
        """)
        self.quiz_btn.clicked.connect(lambda: self.switch_mode('quiz'))
        sidebar_layout.addWidget(self.quiz_btn)
        
        self.settings_btn = QPushButton("⚙️ Settings")
        self.settings_btn.setStyleSheet("""
            QPushButton {
                background-color: #0E3F45;
                color: #A0C4C8;
                font-weight: bold;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #1A5C63;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #1A5C63;
                color: #FFFFFF;
            }
        """)
        self.settings_btn.clicked.connect(lambda: self.switch_mode('settings'))
        sidebar_layout.addWidget(self.settings_btn)
        
        sidebar_layout.addStretch()
        
        content_wrapper.addWidget(self.sidebar)
        
        # Toggle sidebar button (outside sidebar so it stays visible)
        self.toggle_btn = QPushButton("◀")
        self.toggle_btn.setFixedSize(24, 60)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #05363D;
                color: #D4AA50;
                border: 1px solid #1A5C63;
                border-left: none;
                border-radius: 0px 8px 8px 0px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1A5C63;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        content_wrapper.addWidget(self.toggle_btn)
        
        # Stacked widget for different modes
        self.stack = QStackedWidget()
        
        # Library page (original content)
        library_page = QWidget()
        library_layout = QVBoxLayout(library_page)
        library_layout.setSpacing(0)
        library_layout.setContentsMargins(0, 0, 0, 0)
        
        # Toolbar
        toolbar = QFrame()
        toolbar.setStyleSheet("background-color: #062C30;")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(25, 15, 25, 15)
        
        # Search
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("Search words...")
        self.search_entry.setFixedWidth(300)
        self.search_entry.textChanged.connect(self.filter_words)
        toolbar_layout.addWidget(self.search_entry)
        
        # Keyboard button
        self.kb_btn = QPushButton("⌨️")
        self.kb_btn.setFixedSize(40, 40)
        self.kb_btn.clicked.connect(lambda: self.show_keyboard(self.search_entry))
        toolbar_layout.addWidget(self.kb_btn)
        
        # Tag filter
        self.tag_filter = QComboBox()
        self.tag_filter.setFixedWidth(150)
        self.tag_filter.addItem("All Tags")
        self.tag_filter.addItems(self.data.get('tags', []))
        self.tag_filter.currentTextChanged.connect(self.filter_words)
        toolbar_layout.addWidget(self.tag_filter)
        
        # Group filter
        self.group_filter = QComboBox()
        self.group_filter.setFixedWidth(180)
        self.group_filter.addItem("All Word Groups")
        self.update_group_filter()
        self.group_filter.currentTextChanged.connect(self.filter_words)
        toolbar_layout.addWidget(self.group_filter)
        
        toolbar_layout.addStretch()
        library_layout.addWidget(toolbar)
        
        # Content area with geometric pattern background
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Pattern background (drawn behind content)
        self.pattern_bg = GeometricPatternWidget(content_area)
        
        # Words scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("QScrollArea { background: transparent; } QScrollArea > QWidget > QWidget { background: transparent; }")
        
        self.words_container = QWidget()
        self.words_container.setStyleSheet("background: transparent;")
        self.words_layout = QGridLayout(self.words_container)
        self.words_layout.setSpacing(15)
        self.words_layout.setContentsMargins(25, 15, 25, 25)
        self.words_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        scroll_area.setWidget(self.words_container)
        content_layout.addWidget(scroll_area)
        
        library_layout.addWidget(content_area)
        
        self.stack.addWidget(library_page)  # Index 0: Library
        
        # Quiz page
        self.quiz_widget = QuizWidget(self.data, self.show_keyboard)
        self.stack.addWidget(self.quiz_widget)  # Index 1: Quiz
        
        # Settings page
        self.settings_widget = SettingsWidget(
            self.data, 
            on_save=self.save_settings_data,
            on_import=self.import_data
        )
        self.stack.addWidget(self.settings_widget) # Index 2: Settings
        
        content_wrapper.addWidget(self.stack)
        
        # Add content wrapper to main layout
        content_widget = QWidget()
        content_widget.setLayout(content_wrapper)
        main_layout.addWidget(content_widget)
        
        self.sidebar_visible = True
        self.current_mode = 'library'
    
    def toggle_sidebar(self):
        """Toggle sidebar visibility."""
        if self.sidebar_visible:
            self.sidebar.hide()
            self.toggle_btn.setText("▶")
            self.sidebar_visible = False
        else:
            self.sidebar.show()
            self.toggle_btn.setText("◀")
            self.sidebar_visible = True
    
    def switch_mode(self, mode):
        """Switch between library, quiz, and settings mode."""
        self.current_mode = mode
        
        # Reset styles
        inactive_style = """
            QPushButton {
                background-color: #0E3F45;
                color: #A0C4C8;
                font-weight: bold;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #1A5C63;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #1A5C63;
                color: #FFFFFF;
            }
        """
        active_style = """
            QPushButton {
                background-color: #D4AA50;
                color: #062C30;
                font-weight: bold;
                padding: 15px;
                border-radius: 8px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #E5BB61;
            }
        """
        
        self.library_btn.setStyleSheet(inactive_style)
        self.quiz_btn.setStyleSheet(inactive_style)
        self.settings_btn.setStyleSheet(inactive_style)
        
        # Configure UI based on mode
        if mode == 'library':
            self.stack.setCurrentIndex(0)
            self.add_btn.show()
            self.library_btn.setStyleSheet(active_style)
        elif mode == 'quiz':
            self.stack.setCurrentIndex(1)
            self.add_btn.hide()
            self.quiz_btn.setStyleSheet(active_style)
            self.quiz_widget.update_tags(self.data.get('tags', []))
        elif mode == 'settings':
            self.stack.setCurrentIndex(2)
            self.add_btn.hide()
            self.settings_btn.setStyleSheet(active_style)
    
    def show_keyboard(self, target_entry):
        """Show Arabic keyboard."""
        if hasattr(self, 'keyboard') and self.keyboard:
            self.keyboard.target_entry = target_entry
            self.keyboard.show()
            self.keyboard.raise_()
        else:
            self.keyboard = ArabicKeyboard(self, target_entry)
            self.keyboard.show()
    
    def resizeEvent(self, event):
        """Handle window resize to update pattern background."""
        super().resizeEvent(event)
        if hasattr(self, 'pattern_bg'):
            # Get the content area (parent of pattern_bg)
            content_area = self.pattern_bg.parent()
            if content_area:
                self.pattern_bg.setGeometry(content_area.rect())
    
    def refresh_words(self):
        """Refresh the words display."""
        # Clear existing
        while self.words_layout.count():
            item = self.words_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not self.filtered_words:
            empty_label = QLabel("📚\n\nNo words found.\nAdd your first word!")
            empty_label.setStyleSheet("color: #A0C4C8; font-size: 16px; font-weight: 500;")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.words_layout.addWidget(empty_label, 0, 0, 1, 2)
            return
        
        # Get active languages
        languages = self.data.get('settings', {}).get('languages', ["English", "Danish"])
        
        # Add word cards in grid (2 columns)
        for idx, word in enumerate(self.filtered_words):
            row = idx // 2
            col = idx % 2
            card = WordCard(word, self.edit_word, self.delete_word, languages)
            self.words_layout.addWidget(card, row, col)
    
    def filter_words(self, *args):
        """Filter words based on search, tag, and word group."""
        search = self.search_entry.text().lower()
        tag = self.tag_filter.currentText()
        group = self.group_filter.currentText()
        
        self.filtered_words = self.data['words']
        
        if tag and tag != "All Tags":
            self.filtered_words = [
                w for w in self.filtered_words
                if tag in w.get('tags', [])
            ]
        
        if group and group != "All Word Groups":
            self.filtered_words = [
                w for w in self.filtered_words
                if w.get('grammar', {}).get('group', '') == group
            ]
        
        if search:
            self.filtered_words = [
                w for w in self.filtered_words
                if search in w.get('arabic', '').lower()
                or search in w.get('english', '').lower()
                or search in w.get('danish', '').lower()
                or search in w.get('transliteration', '').lower()
            ]
        
        self.refresh_words()
    
    def add_word(self):
        """Open dialog to add a new word."""
        languages = self.data.get('settings', {}).get('languages', ["English", "Danish"])
        dialog = AddEditDialog(
            self,
            tags=self.data.get('tags', []),
            on_save=self.save_word,
            languages=languages
        )
        dialog.exec()
    
    def edit_word(self, word):
        """Open dialog to edit a word."""
        languages = self.data.get('settings', {}).get('languages', ["English", "Danish"])
        dialog = AddEditDialog(
            self,
            word=word,
            tags=self.data.get('tags', []),
            on_save=self.save_word,
            languages=languages
        )
        dialog.exec()
    
    def save_word(self, word_data):
        """Save a word."""
        existing_idx = None
        for idx, w in enumerate(self.data['words']):
            if w['id'] == word_data['id']:
                existing_idx = idx
                break
        
        if existing_idx is not None:
            self.data['words'][existing_idx] = word_data
        else:
            self.data['words'].append(word_data)
        
        # Also save any new tags to the tags list
        for tag in word_data.get('tags', []):
            if tag not in self.data.get('tags', []):
                if 'tags' not in self.data:
                    self.data['tags'] = []
                self.data['tags'].append(tag)
        
        # Update word groups
        group = word_data.get('grammar', {}).get('group', '')
        if group and group not in self.data.get('word_groups', []):
            if 'word_groups' not in self.data:
                self.data['word_groups'] = []
            self.data['word_groups'].append(group)
        
        # Update the tag filter dropdown
        self.tag_filter.clear()
        self.tag_filter.addItem("All Tags")
        self.tag_filter.addItems(self.data.get('tags', []))
        
        # Update the group filter dropdown
        self.update_group_filter()
        
        save_data(self.data)
        self.filter_words()
    
    def update_group_filter(self):
        """Update the word group filter dropdown."""
        current = self.group_filter.currentText()
        self.group_filter.clear()
        self.group_filter.addItem("All Word Groups")
        # Collect all unique groups from words
        groups = set()
        for word in self.data.get('words', []):
            group = word.get('grammar', {}).get('group', '')
            if group:
                groups.add(group)
        for g in self.data.get('word_groups', []):
            groups.add(g)
        self.group_filter.addItems(sorted(groups))
        # Restore selection if still valid
        index = self.group_filter.findText(current)
        if index >= 0:
            self.group_filter.setCurrentIndex(index)
    
    def delete_word(self, word_id):
        """Delete a word."""
        reply = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete this word?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.data['words'] = [w for w in self.data['words'] if w['id'] != word_id]
            save_data(self.data)
            self.update_group_filter()
            self.filter_words()


    def save_settings_data(self, data):
        """Save updated settings and refresh UI."""
        self.data = data
        save_data(self.data)
        # Refresh word cards to show new languages
        self.refresh_words()
        
    def import_data(self, new_data):
        """Import vocabulary from another file."""
        if not new_data or 'words' not in new_data:
            return False
            
        current_ids = {w['id'] for w in self.data['words']}
        added_count = 0
        
        # Merge words
        for word in new_data['words']:
            if word['id'] not in current_ids:
                self.data['words'].append(word)
                current_ids.add(word['id'])
                added_count += 1
            else:
                # Optional: Update existing word? For now skipping duplicates.
                pass
                
        # Merge tags
        for tag in new_data.get('tags', []):
            if tag not in self.data['tags']:
                self.data['tags'].append(tag)
                
        # Merge groups
        for group in new_data.get('word_groups', []):
            if 'word_groups' not in self.data:
                self.data['word_groups'] = []
            if group not in self.data['word_groups']:
                self.data['word_groups'].append(group)
        
        save_data(self.data)
        self.refresh_words()
        self.update_group_filter()
        QMessageBox.information(self, "Import Complete", f"Added {added_count} new words.")
        return True


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Dark palette - Arabic Theme
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor('#062C30'))
    palette.setColor(QPalette.ColorRole.WindowText, QColor('#FDF6E3'))
    palette.setColor(QPalette.ColorRole.Base, QColor('#05363D'))
    palette.setColor(QPalette.ColorRole.Text, QColor('#FDF6E3'))
    palette.setColor(QPalette.ColorRole.Button, QColor('#0E3F45'))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor('#FDF6E3'))
    palette.setColor(QPalette.ColorRole.Highlight, QColor('#D4AA50'))
    app.setPalette(palette)
    
    window = ArabicVocabularyApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
