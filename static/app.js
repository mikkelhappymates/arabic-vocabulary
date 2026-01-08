/**
 * Arabic Vocabulary App - Frontend JavaScript
 */

// State
let words = [];
let tags = [];
let selectedTags = [];
let currentEditId = null;
let activeKeyboardTarget = null;

// DOM Elements
const wordsGrid = document.getElementById('wordsGrid');
const emptyState = document.getElementById('emptyState');
const searchInput = document.getElementById('searchInput');
const tagFilter = document.getElementById('tagFilter');
const addWordBtn = document.getElementById('addWordBtn');
const wordModal = document.getElementById('wordModal');
const wordForm = document.getElementById('wordForm');
const modalTitle = document.getElementById('modalTitle');
const closeModal = document.getElementById('closeModal');
const cancelBtn = document.getElementById('cancelBtn');
const arabicKeyboard = document.getElementById('arabicKeyboard');
const closeKeyboard = document.getElementById('closeKeyboard');
const tagsInput = document.getElementById('tagsInput');
const selectedTagsContainer = document.getElementById('selectedTags');

// Form inputs
const wordIdInput = document.getElementById('wordId');
const arabicInput = document.getElementById('arabicInput');
const arabicDiacriticsInput = document.getElementById('arabicDiacriticsInput');
const transliterationInput = document.getElementById('transliterationInput');
const englishInput = document.getElementById('englishInput');
const danishInput = document.getElementById('danishInput');
const notesInput = document.getElementById('notesInput');

// API Functions
async function fetchWords(search = '', tag = '') {
    try {
        let url = '/api/words';
        const params = new URLSearchParams();
        if (search) params.append('search', search);
        if (tag) params.append('tag', tag);
        if (params.toString()) url += '?' + params.toString();
        
        const response = await fetch(url);
        words = await response.json();
        renderWords();
    } catch (error) {
        console.error('Error fetching words:', error);
    }
}

async function fetchTags() {
    try {
        const response = await fetch('/api/tags');
        tags = await response.json();
        renderTagFilter();
        renderTagsDropdown();
    } catch (error) {
        console.error('Error fetching tags:', error);
    }
}

async function saveWord(wordData) {
    try {
        const url = currentEditId ? `/api/words/${currentEditId}` : '/api/words';
        const method = currentEditId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(wordData)
        });
        
        if (response.ok) {
            closeModalHandler();
            fetchWords();
        }
    } catch (error) {
        console.error('Error saving word:', error);
    }
}

async function deleteWord(id) {
    if (!confirm('Are you sure you want to delete this word?')) return;
    
    try {
        const response = await fetch(`/api/words/${id}`, { method: 'DELETE' });
        if (response.ok) {
            fetchWords();
        }
    } catch (error) {
        console.error('Error deleting word:', error);
    }
}

// Render Functions
function renderWords() {
    if (words.length === 0) {
        wordsGrid.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }
    
    emptyState.style.display = 'none';
    wordsGrid.innerHTML = words.map(word => `
        <div class="word-card" data-id="${word.id}">
            <div class="word-arabic">${word.arabic_diacritics || word.arabic}</div>
            ${word.transliteration ? `<div class="word-transliteration">${word.transliteration}</div>` : ''}
            <div class="word-translations">
                <div class="word-translation">
                    <span class="translation-lang">EN</span>
                    <span class="translation-text">${word.english}</span>
                </div>
                <div class="word-translation">
                    <span class="translation-lang">DA</span>
                    <span class="translation-text">${word.danish}</span>
                </div>
            </div>
            ${word.tags && word.tags.length > 0 ? `
                <div class="word-tags">
                    ${word.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
            ` : ''}
            <div class="word-actions">
                <button class="btn btn-sm btn-secondary" onclick="editWord('${word.id}')">Edit</button>
                <button class="btn btn-sm btn-danger" onclick="deleteWord('${word.id}')">Delete</button>
            </div>
        </div>
    `).join('');
}

function renderTagFilter() {
    tagFilter.innerHTML = '<option value="">All Tags</option>' +
        tags.map(tag => `<option value="${tag}">${tag}</option>`).join('');
}

function renderTagsDropdown() {
    tagsInput.innerHTML = '<option value="">Select a tag...</option>' +
        tags.map(tag => `<option value="${tag}">${tag}</option>`).join('');
}

function renderSelectedTags() {
    selectedTagsContainer.innerHTML = selectedTags.map(tag => `
        <span class="selected-tag">
            ${tag}
            <button type="button" onclick="removeSelectedTag('${tag}')">&times;</button>
        </span>
    `).join('');
}

// Modal Functions
function openModal(editMode = false) {
    wordModal.classList.add('active');
    modalTitle.textContent = editMode ? 'Edit Word' : 'Add New Word';
    if (!editMode) {
        resetForm();
    }
}

function closeModalHandler() {
    wordModal.classList.remove('active');
    hideKeyboard();
    resetForm();
}

function resetForm() {
    wordForm.reset();
    currentEditId = null;
    selectedTags = [];
    renderSelectedTags();
}

function editWord(id) {
    const word = words.find(w => w.id === id);
    if (!word) return;
    
    currentEditId = id;
    wordIdInput.value = id;
    arabicInput.value = word.arabic || '';
    arabicDiacriticsInput.value = word.arabic_diacritics || '';
    transliterationInput.value = word.transliteration || '';
    englishInput.value = word.english || '';
    danishInput.value = word.danish || '';
    notesInput.value = word.notes || '';
    selectedTags = [...(word.tags || [])];
    renderSelectedTags();
    
    openModal(true);
}

// Tag Functions
function addSelectedTag(tag) {
    if (tag && !selectedTags.includes(tag)) {
        selectedTags.push(tag);
        renderSelectedTags();
    }
    tagsInput.value = '';
}

function removeSelectedTag(tag) {
    selectedTags = selectedTags.filter(t => t !== tag);
    renderSelectedTags();
}

// Arabic Keyboard Functions
function showKeyboard(targetId) {
    activeKeyboardTarget = document.getElementById(targetId);
    arabicKeyboard.classList.add('active');
    
    // Update toggle button states
    document.querySelectorAll('.keyboard-toggle').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.target === targetId);
    });
}

function hideKeyboard() {
    arabicKeyboard.classList.remove('active');
    activeKeyboardTarget = null;
    
    document.querySelectorAll('.keyboard-toggle').forEach(btn => {
        btn.classList.remove('active');
    });
}

function insertCharacter(char) {
    if (!activeKeyboardTarget) return;
    
    const start = activeKeyboardTarget.selectionStart;
    const end = activeKeyboardTarget.selectionEnd;
    const value = activeKeyboardTarget.value;
    
    activeKeyboardTarget.value = value.slice(0, start) + char + value.slice(end);
    activeKeyboardTarget.selectionStart = activeKeyboardTarget.selectionEnd = start + char.length;
    activeKeyboardTarget.focus();
}

function backspace() {
    if (!activeKeyboardTarget) return;
    
    const start = activeKeyboardTarget.selectionStart;
    const end = activeKeyboardTarget.selectionEnd;
    const value = activeKeyboardTarget.value;
    
    if (start === end && start > 0) {
        activeKeyboardTarget.value = value.slice(0, start - 1) + value.slice(end);
        activeKeyboardTarget.selectionStart = activeKeyboardTarget.selectionEnd = start - 1;
    } else if (start !== end) {
        activeKeyboardTarget.value = value.slice(0, start) + value.slice(end);
        activeKeyboardTarget.selectionStart = activeKeyboardTarget.selectionEnd = start;
    }
    activeKeyboardTarget.focus();
}

// Event Listeners
addWordBtn.addEventListener('click', () => openModal(false));
closeModal.addEventListener('click', closeModalHandler);
cancelBtn.addEventListener('click', closeModalHandler);

document.querySelector('.modal-overlay').addEventListener('click', closeModalHandler);

wordForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const wordData = {
        arabic: arabicInput.value,
        arabic_diacritics: arabicDiacriticsInput.value,
        transliteration: transliterationInput.value,
        english: englishInput.value,
        danish: danishInput.value,
        notes: notesInput.value,
        tags: selectedTags
    };
    
    saveWord(wordData);
});

searchInput.addEventListener('input', (e) => {
    fetchWords(e.target.value, tagFilter.value);
});

tagFilter.addEventListener('change', (e) => {
    fetchWords(searchInput.value, e.target.value);
});

tagsInput.addEventListener('change', (e) => {
    addSelectedTag(e.target.value);
});

// Keyboard toggle buttons
document.querySelectorAll('.keyboard-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
        const targetId = btn.dataset.target;
        if (activeKeyboardTarget && activeKeyboardTarget.id === targetId) {
            hideKeyboard();
        } else {
            showKeyboard(targetId);
        }
    });
});

// Keyboard key clicks
document.querySelectorAll('.key[data-char]').forEach(key => {
    key.addEventListener('click', () => {
        insertCharacter(key.dataset.char);
    });
});

document.getElementById('keyboardBackspace').addEventListener('click', backspace);
closeKeyboard.addEventListener('click', hideKeyboard);

// Close keyboard on escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        if (arabicKeyboard.classList.contains('active')) {
            hideKeyboard();
        } else if (wordModal.classList.contains('active')) {
            closeModalHandler();
        }
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    fetchWords();
    fetchTags();
});
