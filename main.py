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
    QGridLayout, QDialog, QMessageBox, QComboBox, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize, QPointF
from PyQt6.QtGui import QFont, QColor, QPalette, QPainter, QPen, QBrush, QPainterPath
import math

# Version
VERSION = "0.5"

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
            "notes": "Common greeting"
        },
        {
            "id": "2", 
            "arabic": "شكرا",
            "transliteration": "shukran",
            "english": "thank you",
            "danish": "tak",
            "tags": ["greetings"],
            "notes": ""
        },
        {
            "id": "3",
            "arabic": "نعم",
            "transliteration": "na'am",
            "english": "yes",
            "danish": "ja",
            "tags": ["basics"],
            "notes": ""
        },
        {
            "id": "4",
            "arabic": "لا",
            "transliteration": "la",
            "english": "no", 
            "danish": "nej",
            "tags": ["basics"],
            "notes": ""
        },
        {
            "id": "5",
            "arabic": "ماء",
            "transliteration": "maa'",
            "english": "water",
            "danish": "vand",
            "tags": ["food & drink"],
            "notes": ""
        }
    ],
    "tags": ["greetings", "basics", "food & drink"]
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


class WordCard(QFrame):
    """A card displaying a single vocabulary word."""
    
    def __init__(self, word, on_edit, on_delete):
        super().__init__()
        self.word = word
        self.on_edit = on_edit
        self.on_delete = on_delete
        
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
        arabic_label.setStyleSheet("color: #D4AA50; font-family: 'Amiri', 'Arial';")
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
        
        # English
        en_row = QHBoxLayout()
        en_label = QLabel("EN")
        en_label.setStyleSheet("color: #38B2AC; font-weight: bold; font-size: 11px;")
        en_label.setFixedWidth(30)
        en_row.addWidget(en_label)
        en_text = QLabel(word.get('english', ''))
        en_row.addWidget(en_text)
        en_row.addStretch()
        trans_layout.addLayout(en_row)
        
        # Danish
        da_row = QHBoxLayout()
        da_label = QLabel("DA")
        da_label.setStyleSheet("color: #38B2AC; font-weight: bold; font-size: 11px;")
        da_label.setFixedWidth(30)
        da_row.addWidget(da_label)
        da_text = QLabel(word.get('danish', ''))
        da_row.addWidget(da_text)
        da_row.addStretch()
        trans_layout.addLayout(da_row)
        
        layout.addWidget(trans_frame)
        
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


class AddEditDialog(QDialog):
    """Dialog for adding or editing a word."""
    
    def __init__(self, parent, word=None, tags=None, on_save=None):
        super().__init__(parent)
        self.word = word or {}
        self.all_tags = tags or []
        self.on_save_callback = on_save
        self.selected_tags = list(self.word.get('tags', []))
        self.keyboard = None
        
        self.setWindowTitle("Edit Word" if word else "Add New Word")
        self.setFixedSize(500, 720)
        self.setStyleSheet(STYLE)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Arabic input
        layout.addWidget(QLabel("Arabic *"))
        arabic_row = QHBoxLayout()
        self.arabic_entry = QLineEdit(self.word.get('arabic', ''))
        self.arabic_entry.setFont(QFont('Arial', 18))
        self.arabic_entry.setStyleSheet("color: #D4AA50; font-family: 'Amiri', 'Arial';")
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
        self.diacritics_entry.setStyleSheet("color: #D4AA50; font-family: 'Amiri', 'Arial';")
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
        
        # English
        layout.addWidget(QLabel("English *"))
        self.english_entry = QLineEdit(self.word.get('english', ''))
        layout.addWidget(self.english_entry)
        
        # Danish
        layout.addWidget(QLabel("Danish *"))
        self.danish_entry = QLineEdit(self.word.get('danish', ''))
        layout.addWidget(self.danish_entry)
        
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
        self.notes_entry.setMaximumHeight(80)
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
        english = self.english_entry.text().strip()
        danish = self.danish_entry.text().strip()
        
        if not arabic or not english or not danish:
            QMessageBox.warning(self, "Error", "Arabic, English, and Danish are required.")
            return
        
        now = datetime.utcnow().isoformat() + 'Z'
        word_data = {
            'id': self.word.get('id', str(uuid.uuid4())),
            'arabic': arabic,
            'arabic_diacritics': self.diacritics_entry.text().strip(),
            'transliteration': self.transliteration_entry.text().strip(),
            'english': english,
            'danish': danish,
            'tags': self.selected_tags,
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
        self.filtered_words = self.data['words']
        
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
        logo_arabic.setFont(QFont('Amiri', 32)) 
        logo_arabic.setStyleSheet("color: #D4AA50; font-family: 'Amiri', 'Arial';")
        logo_layout.addWidget(logo_arabic)
        
        logo_text = QLabel("Vocabulary")
        logo_text.setFont(QFont('Comic Sans MS', 22))
        logo_text.setStyleSheet("color: #A0C4C8; letter-spacing: 1px; font-family: 'Comic Sans MS', 'Chalkboard SE';")
        logo_layout.addWidget(logo_text)
        logo_layout.addStretch()
        
        header_layout.addLayout(logo_layout)
        
        # Add button
        add_btn = QPushButton("+ Add Word")
        add_btn.setObjectName("primaryBtn")
        add_btn.clicked.connect(self.add_word)
        header_layout.addWidget(add_btn)
        
        main_layout.addWidget(header)
        
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
        
        # Tag filter
        self.tag_filter = QComboBox()
        self.tag_filter.setFixedWidth(150)
        self.tag_filter.addItem("All Tags")
        self.tag_filter.addItems(self.data.get('tags', []))
        self.tag_filter.currentTextChanged.connect(self.filter_words)
        toolbar_layout.addWidget(self.tag_filter)
        
        toolbar_layout.addStretch()
        main_layout.addWidget(toolbar)
        
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
        
        main_layout.addWidget(content_area)
    
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
        
        # Add word cards in grid (2 columns)
        for idx, word in enumerate(self.filtered_words):
            row = idx // 2
            col = idx % 2
            card = WordCard(word, self.edit_word, self.delete_word)
            self.words_layout.addWidget(card, row, col)
    
    def filter_words(self):
        """Filter words based on search and tag."""
        search = self.search_entry.text().lower()
        tag = self.tag_filter.currentText()
        
        self.filtered_words = self.data['words']
        
        if tag and tag != "All Tags":
            self.filtered_words = [
                w for w in self.filtered_words
                if tag in w.get('tags', [])
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
        dialog = AddEditDialog(
            self,
            tags=self.data.get('tags', []),
            on_save=self.save_word
        )
        dialog.exec()
    
    def edit_word(self, word):
        """Open dialog to edit a word."""
        dialog = AddEditDialog(
            self,
            word=word,
            tags=self.data.get('tags', []),
            on_save=self.save_word
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
        
        # Update the tag filter dropdown
        self.tag_filter.clear()
        self.tag_filter.addItem("All Tags")
        self.tag_filter.addItems(self.data.get('tags', []))
        
        save_data(self.data)
        self.filter_words()
    
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
            self.filter_words()


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
