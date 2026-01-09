import json
import uuid
import datetime

# Helper to get current timestamp
def clean_timestamp():
    return datetime.datetime.utcnow().isoformat() + 'Z'

# Raw data to expand into full JSON objects
raw_words = [
    # Colors
    ("أحمر", "ahmar", "red", "rød", ["colors", "adjectives"]),
    ("أزرق", "azraq", "blue", "blå", ["colors", "adjectives"]),
    ("أخضر", "akhdar", "green", "grøn", ["colors", "adjectives"]),
    ("أصفر", "asfar", "yellow", "gul", ["colors", "adjectives"]),
    ("أسود", "aswad", "black", "sort", ["colors", "adjectives"]),
    ("أبيض", "abyad", "white", "hvid", ["colors", "adjectives"]),
    
    # Numbers
    ("واحد", "wahid", "one", "en", ["numbers"]),
    ("اثنان", "ithnan", "two", "to", ["numbers"]),
    ("ثلاثة", "thalatha", "three", "tre", ["numbers"]),
    ("أربعة", "arba'a", "four", "fire", ["numbers"]),
    ("خمسة", "khamsa", "five", "fem", ["numbers"]),
    ("ستة", "sitta", "six", "seks", ["numbers"]),
    ("سبعة", "sab'a", "seven", "syv", ["numbers"]),
    ("ثمانية", "thamania", "eight", "otte", ["numbers"]),
    ("تسعة", "tis'a", "nine", "ni", ["numbers"]),
    ("عشرة", "ashara", "ten", "ti", ["numbers"]),

    # Family
    ("أب", "ab", "father", "far", ["family"]),
    ("أم", "umm", "mother", "mor", ["family"]),
    ("أخ", "akh", "brother", "bror", ["family"]),
    ("أخت", "ukht", "sister", "søster", ["family"]),
    ("ابن", "ibn", "son", "søn", ["family"]),
    ("بنت", "bint", "daughter", "datter", ["family"]),
    ("جد", "jadd", "grandfather", "bedstefar", ["family"]),
    ("جدة", "jadda", "grandmother", "bedstemor", ["family"]),

    # Time / Days
    ("يوم", "yawm", "day", "dag", ["time"]),
    ("أسبوع", "usbu'", "week", "uge", ["time"]),
    ("شهر", "shahr", "month", "måned", ["time"]),
    ("سنة", "sana", "year", "år", ["time"]),
    ("اليوم", "alyawm", "today", "i dag", ["time"]),
    ("غدا", "ghadan", "tomorrow", "i morgen", ["time"]),
    ("أمس", "ams", "yesterday", "i går", ["time"]),
    
    # Common Objects
    ("كتاب", "kitab", "book", "bog", ["objects", "study"]),
    ("قلم", "qalam", "pen", "pen", ["objects", "study"]),
    ("بيت", "bayt", "house", "hus", ["objects", "places"]),
    ("سيارة", "sayyara", "car", "bil", ["objects", "transport"]),
    ("طاولة", "tawila", "table", "bord", ["objects", "furniture"]),
    ("كرسي", "kursi", "chair", "stol", ["objects", "furniture"]),
    ("باب", "bab", "door", "dør", ["objects"]),
    ("شباك", "shubbak", "window", "vindue", ["objects"]),

    # Animals
    ("قطة", "qitta", "cat", "kat", ["animals"]),
    ("كلب", "kalb", "dog", "hund", ["animals"]),
    ("حصان", "hisan", "horse", "hest", ["animals"]),
    ("عصفور", "asfour", "bird", "fugl", ["animals"]),
    ("سمكة", "samaka", "fish", "fisk", ["animals"]),

    # Nature
    ("شمس", "shams", "sun", "sol", ["nature"]),
    ("قمر", "qamar", "moon", "måne", ["nature"]),
    ("سماء", "sama'", "sky", "himmel", ["nature"]),
    ("أرض", "ard", "earth/ground", "jord", ["nature"]),
    ("بحر", "bahr", "sea", "hav", ["nature"]),
    ("شجرة", "shajara", "tree", "træ", ["nature"]),

    # Adjectives
    ("كبير", "kabir", "big", "stor", ["adjectives"]),
    ("صغير", "saghir", "small", "lille", ["adjectives"]),
    ("جديد", "jadid", "new", "ny", ["adjectives"]),
    ("قديم", "qadim", "old", "gammel", ["adjectives"]),
    ("جميل", "jamil", "beautiful", "shmukh", ["adjectives"]),
    ("سعيد", "sa'id", "happy", "glad", ["adjectives", "emotions"]),
    ("حزين", "hazin", "sad", "trist", ["adjectives", "emotions"]),
]

# Verbs with some grammar structures
verbs = [
    {
        "arabic": "كتب",
        "transliteration": "kataba",
        "english": "he wrote",
        "danish": "han skrev",
        "tags": ["verbs"],
        "grammar": {"group": "كتب - to write", "person": "3rd", "gender": "masculine", "number": "singular", "tense": "past", "form": "Form I"}
    },
    {
        "arabic": "يكتب",
        "transliteration": "yaktubu",
        "english": "he writes",
        "danish": "han skriver",
        "tags": ["verbs"],
        "grammar": {"group": "كتب - to write", "person": "3rd", "gender": "masculine", "number": "singular", "tense": "present", "form": "Form I"}
    },
    {
        "arabic": "أكل",
        "transliteration": "akala",
        "english": "he ate",
        "danish": "han spiste",
        "tags": ["verbs", "food & drink"],
        "grammar": {"group": "أكل - to eat", "person": "3rd", "gender": "masculine", "number": "singular", "tense": "past", "form": "Form I"}
    },
    {
        "arabic": "شرب",
        "transliteration": "shariba",
        "english": "he drank",
        "danish": "han drak",
        "tags": ["verbs", "food & drink"],
        "grammar": {"group": "شرب - to drink", "person": "3rd", "gender": "masculine", "number": "singular", "tense": "past", "form": "Form I"}
    },
        {
        "arabic": "ذهب",
        "transliteration": "zhahaba",
        "english": "he went",
        "danish": "han gik",
        "tags": ["verbs"],
        "grammar": {"group": "ذهب - to go", "person": "3rd", "gender": "masculine", "number": "singular", "tense": "past", "form": "Form I"}
    }
]

# Construct the full list
final_words = []
all_tags = set()
all_groups = set()

# Process simple words
for ar, tr, en, da, tags in raw_words:
    word = {
        "id": str(uuid.uuid4()),
        "arabic": ar,
        "arabic_diacritics": ar, # Simulating diacritics same as base for simplicity if not provided
        "transliteration": tr,
        "english": en,
        "danish": da,
        # Adding random extra languages for testing
        "german": f"[DE] {en}",
        "spanish": f"[ES] {en}",
        "tags": tags,
        "grammar": {},
        "notes": "Imported via test file",
        "created_at": clean_timestamp(),
        "updated_at": clean_timestamp()
    }
    final_words.append(word)
    all_tags.update(tags)

# Process verbs
for v in verbs:
    word = {
        "id": str(uuid.uuid4()),
        "arabic": v["arabic"],
        "arabic_diacritics": v["arabic"],
        "transliteration": v["transliteration"],
        "english": v["english"],
        "danish": v["danish"],
        "tags": v["tags"],
        "grammar": v["grammar"],
        "notes": "Imported verb",
        "created_at": clean_timestamp(),
        "updated_at": clean_timestamp()
    }
    final_words.append(word)
    all_tags.update(v["tags"])
    if "group" in v["grammar"]:
        all_groups.add(v["grammar"]["group"])

output_data = {
    "words": final_words,
    "tags": sorted(list(all_tags)),
    "word_groups": sorted(list(all_groups)),
    "settings": {
        "languages": ["English", "Danish"]
    }
}

filename = "large_vocabulary_test.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print(f"Index successfully generated {len(final_words)} words into {filename}")
