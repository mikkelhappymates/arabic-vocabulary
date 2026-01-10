/**
 * Arabic Vocabulary App - Frontend JavaScript
 * Version 0.5.0 - Full Feature Web App
 */

// State
let words = [];
let tags = [];
let wordGroups = [];
let selectedTags = [];
let currentEditId = null;
let activeKeyboardTarget = null;
let settings = {
    languages: ['English', 'Danish'],
    custom_languages: [],
    available_languages: []
};

// DOM Elements
const wordsGrid = document.getElementById('wordsGrid');
const emptyState = document.getElementById('emptyState');
const searchInput = document.getElementById('searchInput');
const tagFilter = document.getElementById('tagFilter');
const wordGroupFilter = document.getElementById('wordGroupFilter');
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
const wordGroupInput = document.getElementById('wordGroupInput');

// Grammar inputs
const grammarPerson = document.getElementById('grammarPerson');
const grammarNumber = document.getElementById('grammarNumber');
const grammarGender = document.getElementById('grammarGender');
const grammarTense = document.getElementById('grammarTense');
const grammarForm = document.getElementById('grammarForm');

// API Functions
async function fetchWords(search = '', tag = '', wordGroup = '') {
    try {
        let url = '/api/words';
        const params = new URLSearchParams();
        if (search) params.append('search', search);
        if (tag) params.append('tag', tag);
        if (params.toString()) url += '?' + params.toString();
        
        const response = await fetch(url);
        words = await response.json();
        
        // Client-side word group filter
        if (wordGroup) {
            words = words.filter(w => w.word_group === wordGroup);
        }
        
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
        renderQuizTagFilter();
    } catch (error) {
        console.error('Error fetching tags:', error);
    }
}

async function fetchWordGroups() {
    try {
        const response = await fetch('/api/word-groups');
        wordGroups = await response.json();
        renderWordGroupFilter();
        renderWordGroupsList();
    } catch (error) {
        console.error('Error fetching word groups:', error);
    }
}

async function fetchSettings() {
    try {
        const response = await fetch('/api/settings');
        settings = await response.json();
    } catch (error) {
        console.error('Error fetching settings:', error);
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
            fetchWordGroups(); // Refresh word groups in case a new one was added
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
    wordsGrid.innerHTML = words.map(word => {
        // Build grammar info string
        const grammarParts = [];
        if (word.grammar) {
            if (word.grammar.form) grammarParts.push(word.grammar.form);
            if (word.grammar.tense) grammarParts.push(word.grammar.tense);
            if (word.grammar.person) grammarParts.push(word.grammar.person);
            if (word.grammar.number) grammarParts.push(word.grammar.number);
            if (word.grammar.gender) grammarParts.push(word.grammar.gender);
        }
        const grammarInfo = grammarParts.join(' · ');
        
        return `
        <div class="word-card" data-id="${word.id}">
            <div class="word-main">
                <div class="word-arabic">${word.arabic_diacritics || word.arabic}</div>
                ${word.transliteration ? `<div class="word-transliteration">${word.transliteration}</div>` : ''}
                ${grammarInfo ? `<div class="word-grammar">${grammarInfo}</div>` : ''}
            </div>
            
            <div class="word-info">
                <div class="word-translation">
                    <span class="lang-label">EN</span>
                    <span class="lang-text">${word.english}</span>
                </div>
                <div class="word-translation">
                    <span class="lang-label">DA</span>
                    <span class="lang-text">${word.danish}</span>
                </div>
                
                ${word.word_group ? `
                    <div class="word-group-badge">
                        <span class="group-icon">📂</span>
                        ${word.word_group}
                    </div>
                ` : ''}
                
                ${word.tags && word.tags.length > 0 ? `
                    <div class="word-tags">
                        ${word.tags.map(tag => `<span class="tag-pill">${tag}</span>`).join('')}
                    </div>
                ` : ''}
            </div>

            <div class="word-actions">
                <button class="btn-icon-only" onclick="editWord('${word.id}')" title="Edit">
                    ✏️
                </button>
                <button class="btn-icon-only delete-btn" onclick="deleteWord('${word.id}')" title="Delete">
                    🗑️
                </button>
            </div>
        </div>
    `}).join('');
}

function renderTagFilter() {
    tagFilter.innerHTML = '<option value="">All Tags</option>' +
        tags.map(tag => `<option value="${tag}">${tag}</option>`).join('');
}

function renderWordGroupFilter() {
    wordGroupFilter.innerHTML = '<option value="">All Groups</option>' +
        wordGroups.map(group => `<option value="${group}">${group}</option>`).join('');
}

function renderWordGroupsList() {
    const datalist = document.getElementById('wordGroupsList');
    if (datalist) {
        datalist.innerHTML = wordGroups.map(group => `<option value="${group}">`).join('');
    }
}

function renderTagsDropdown() {
    tagsInput.innerHTML = '<option value="">Select a tag...</option>' +
        tags.map(tag => `<option value="${tag}">${tag}</option>`).join('');
}

function renderQuizTagFilter() {
    const quizTagFilter = document.getElementById('quizTagFilter');
    if (quizTagFilter) {
        quizTagFilter.innerHTML = '<option value="">All Words</option>' +
            tags.map(tag => `<option value="${tag}">${tag}</option>`).join('');
    }
}

function renderSelectedTags() {
    selectedTagsContainer.innerHTML = selectedTags.map(tag => `
        <span class="tag-badge">
            ${tag}
            <button type="button" style="border:none;background:none;font-weight:bold;cursor:pointer;color:inherit;font-size:1.2em;line-height:1;" onclick="removeSelectedTag('${tag}')">&times;</button>
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
    
    // Reset grammar fields
    if (grammarPerson) grammarPerson.value = '';
    if (grammarNumber) grammarNumber.value = '';
    if (grammarGender) grammarGender.value = '';
    if (grammarTense) grammarTense.value = '';
    if (grammarForm) grammarForm.value = '';
    if (wordGroupInput) wordGroupInput.value = '';
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
    wordGroupInput.value = word.word_group || '';
    
    // Set grammar fields
    if (word.grammar) {
        if (grammarPerson) grammarPerson.value = word.grammar.person || '';
        if (grammarNumber) grammarNumber.value = word.grammar.number || '';
        if (grammarGender) grammarGender.value = word.grammar.gender || '';
        if (grammarTense) grammarTense.value = word.grammar.tense || '';
        if (grammarForm) grammarForm.value = word.grammar.form || '';
    }
    
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

document.querySelector('#wordModal .modal-overlay').addEventListener('click', closeModalHandler);

wordForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    // Collect grammar data
    const grammar = {};
    if (grammarPerson && grammarPerson.value) grammar.person = grammarPerson.value;
    if (grammarNumber && grammarNumber.value) grammar.number = grammarNumber.value;
    if (grammarGender && grammarGender.value) grammar.gender = grammarGender.value;
    if (grammarTense && grammarTense.value) grammar.tense = grammarTense.value;
    if (grammarForm && grammarForm.value) grammar.form = grammarForm.value;
    
    const wordData = {
        arabic: arabicInput.value,
        arabic_diacritics: arabicDiacriticsInput.value,
        transliteration: transliterationInput.value,
        english: englishInput.value,
        danish: danishInput.value,
        notes: notesInput.value,
        tags: selectedTags,
        word_group: wordGroupInput ? wordGroupInput.value : '',
        grammar: grammar
    };
    
    // Add word group to the list if it's new
    if (wordData.word_group && !wordGroups.includes(wordData.word_group)) {
        fetch('/api/word-groups', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: wordData.word_group })
        });
    }
    
    saveWord(wordData);
});

searchInput.addEventListener('input', (e) => {
    fetchWords(e.target.value, tagFilter.value, wordGroupFilter.value);
});

tagFilter.addEventListener('change', (e) => {
    fetchWords(searchInput.value, e.target.value, wordGroupFilter.value);
});

wordGroupFilter.addEventListener('change', (e) => {
    fetchWords(searchInput.value, tagFilter.value, e.target.value);
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
        } else if (quizModal.classList.contains('active')) {
            quizModal.classList.remove('active');
        } else if (settingsModal.classList.contains('active')) {
            settingsModal.classList.remove('active');
        } else if (importModal.classList.contains('active')) {
            importModal.classList.remove('active');
        }
    }
});

// --- Export Function ---
document.getElementById('exportBtn').addEventListener('click', () => {
    window.location.href = '/api/export';
});

// --- Import Function ---
const importModal = document.getElementById('importModal');
const importBtn = document.getElementById('importBtn');
const closeImportModal = document.getElementById('closeImportModal');
const cancelImportBtn = document.getElementById('cancelImportBtn');
const confirmImportBtn = document.getElementById('confirmImportBtn');
const importFileInput = document.getElementById('importFileInput');
const mergeImportCheckbox = document.getElementById('mergeImportCheckbox');

importBtn.addEventListener('click', () => {
    importModal.classList.add('active');
});

closeImportModal.addEventListener('click', () => {
    importModal.classList.remove('active');
    importFileInput.value = '';
});

cancelImportBtn.addEventListener('click', () => {
    importModal.classList.remove('active');
    importFileInput.value = '';
});

document.querySelector('#importModal .modal-overlay').addEventListener('click', () => {
    importModal.classList.remove('active');
});

confirmImportBtn.addEventListener('click', async () => {
    const file = importFileInput.files[0];
    if (!file) {
        alert('Please select a file to import.');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    const merge = mergeImportCheckbox.checked;
    const url = '/api/import' + (merge ? '?merge=true' : '');
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            alert(`Import successful! ${result.word_count} words now in database.`);
            importModal.classList.remove('active');
            importFileInput.value = '';
            fetchWords();
            fetchTags();
            fetchWordGroups();
        } else {
            alert('Import failed: ' + result.error);
        }
    } catch (error) {
        console.error('Import error:', error);
        alert('Import failed: ' + error.message);
    }
});

// --- Settings Function ---
const settingsModal = document.getElementById('settingsModal');
const settingsBtn = document.getElementById('settingsBtn');
const closeSettingsModal = document.getElementById('closeSettingsModal');
const saveSettingsBtn = document.getElementById('saveSettingsBtn');
const languageCheckboxes = document.getElementById('languageCheckboxes');
const customLanguageInput = document.getElementById('customLanguageInput');
const addCustomLanguageBtn = document.getElementById('addCustomLanguageBtn');
const customLanguagesList = document.getElementById('customLanguagesList');

let tempSelectedLanguages = [];
let tempCustomLanguages = [];

settingsBtn.addEventListener('click', async () => {
    await fetchSettings();
    tempSelectedLanguages = [...settings.languages];
    tempCustomLanguages = [...(settings.custom_languages || [])];
    renderLanguageCheckboxes();
    renderCustomLanguages();
    settingsModal.classList.add('active');
});

closeSettingsModal.addEventListener('click', () => {
    settingsModal.classList.remove('active');
});

document.querySelector('#settingsModal .modal-overlay').addEventListener('click', () => {
    settingsModal.classList.remove('active');
});

function renderLanguageCheckboxes() {
    const allLanguages = [...(settings.available_languages || []), ...tempCustomLanguages];
    languageCheckboxes.innerHTML = allLanguages.map(lang => `
        <label class="checkbox-label">
            <input type="checkbox" value="${lang}" 
                ${tempSelectedLanguages.includes(lang) ? 'checked' : ''}
                onchange="toggleLanguage('${lang}', this.checked)">
            <span>${lang}</span>
        </label>
    `).join('');
}

function toggleLanguage(lang, checked) {
    if (checked) {
        if (tempSelectedLanguages.length >= 2) {
            alert('You can only select up to 2 languages.');
            renderLanguageCheckboxes();
            return;
        }
        tempSelectedLanguages.push(lang);
    } else {
        tempSelectedLanguages = tempSelectedLanguages.filter(l => l !== lang);
    }
}

function renderCustomLanguages() {
    customLanguagesList.innerHTML = tempCustomLanguages.map(lang => `
        <span class="tag-badge">
            ${lang}
            <button type="button" style="border:none;background:none;font-weight:bold;cursor:pointer;color:inherit;font-size:1.2em;line-height:1;" 
                onclick="removeCustomLanguage('${lang}')">&times;</button>
        </span>
    `).join('');
}

function removeCustomLanguage(lang) {
    tempCustomLanguages = tempCustomLanguages.filter(l => l !== lang);
    tempSelectedLanguages = tempSelectedLanguages.filter(l => l !== lang);
    renderCustomLanguages();
    renderLanguageCheckboxes();
}

addCustomLanguageBtn.addEventListener('click', () => {
    const lang = customLanguageInput.value.trim();
    if (lang && !tempCustomLanguages.includes(lang) && !settings.available_languages.includes(lang)) {
        tempCustomLanguages.push(lang);
        renderCustomLanguages();
        renderLanguageCheckboxes();
        customLanguageInput.value = '';
    }
});

saveSettingsBtn.addEventListener('click', async () => {
    try {
        const response = await fetch('/api/settings', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                languages: tempSelectedLanguages,
                custom_languages: tempCustomLanguages
            })
        });
        
        if (response.ok) {
            settings = await response.json();
            settingsModal.classList.remove('active');
            alert('Settings saved!');
        }
    } catch (error) {
        console.error('Error saving settings:', error);
        alert('Failed to save settings.');
    }
});

// --- Quiz Logic ---
let quizQuestions = [];
let currentQuestionIndex = 0;
let quizScore = 0;
let quizMode = 'ar-en'; // 'ar-en' or 'en-ar'

const quizModal = document.getElementById('quizModal');
const quizStartView = document.getElementById('quizStartView');
const quizGameView = document.getElementById('quizGameView');
const quizResultView = document.getElementById('quizResultView');
const quizProgress = document.getElementById('quizProgress');
const quizCounter = document.getElementById('quizCounter');
const quizQuestionWord = document.getElementById('quizQuestionWord');
const quizOptions = document.getElementById('quizOptions');
const quizFeedback = document.getElementById('quizFeedback');
const nextQuestionBtn = document.getElementById('nextQuestionBtn');
const feedbackTitle = document.getElementById('feedbackTitle');
const feedbackText = document.getElementById('feedbackText');
const quizTagFilter = document.getElementById('quizTagFilter');

// Buttons
document.getElementById('quizBtn').addEventListener('click', () => {
    quizModal.classList.add('active');
    showQuizStart();
});

document.getElementById('closeQuizModal').addEventListener('click', () => {
    quizModal.classList.remove('active');
});

document.querySelector('#quizModal .modal-overlay').addEventListener('click', () => {
    quizModal.classList.remove('active');
});

document.querySelectorAll('.quiz-mode-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.quiz-mode-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        quizMode = btn.dataset.mode;
    });
});

document.getElementById('startQuizBtn').addEventListener('click', startQuiz);
document.getElementById('restartQuizBtn').addEventListener('click', startQuiz);
nextQuestionBtn.addEventListener('click', nextQuestion);

function showQuizStart() {
    quizStartView.style.display = 'block';
    quizGameView.style.display = 'none';
    quizResultView.style.display = 'none';
}

function startQuiz() {
    // Filter words by selected tag
    const selectedTag = quizTagFilter ? quizTagFilter.value : '';
    let pool = words;
    
    if (selectedTag) {
        pool = words.filter(w => w.tags && w.tags.includes(selectedTag));
    }
    
    if (pool.length < 4) {
        alert('You need at least 4 words' + (selectedTag ? ' with that tag' : '') + ' to start a quiz!');
        return;
    }
    
    // Shuffle and pick up to 10
    const questionCount = Math.min(10, pool.length);
    quizQuestions = [...pool].sort(() => 0.5 - Math.random()).slice(0, questionCount);
    currentQuestionIndex = 0;
    quizScore = 0;
    
    quizStartView.style.display = 'none';
    quizResultView.style.display = 'none';
    quizGameView.style.display = 'block';
    
    showQuestion();
}

function showQuestion() {
    const question = quizQuestions[currentQuestionIndex];
    const total = quizQuestions.length;
    
    // Update progress
    const progress = ((currentQuestionIndex) / total) * 100;
    quizProgress.style.width = `${progress}%`;
    quizCounter.textContent = `${currentQuestionIndex + 1} / ${total}`;
    
    // Reset View
    quizFeedback.style.display = 'none';
    quizOptions.innerHTML = '';
    
    // Set Question Word
    if (quizMode === 'ar-en') {
        quizQuestionWord.textContent = question.arabic_diacritics || question.arabic;
        quizQuestionWord.classList.add('rtl');
    } else {
        quizQuestionWord.textContent = question.english;
        quizQuestionWord.classList.remove('rtl');
    }
    
    // Generate Options
    let options = [question];
    
    // Add 3 distractors from the filtered pool or all words
    const distractorPool = quizQuestions.length >= 4 ? quizQuestions : words;
    const distractors = distractorPool.filter(w => w.id !== question.id)
                             .sort(() => 0.5 - Math.random())
                             .slice(0, 3);
    options = [...options, ...distractors].sort(() => 0.5 - Math.random());
    
    options.forEach(opt => {
        const btn = document.createElement('div');
        btn.className = 'quiz-option';
        
        let text = '';
        if (quizMode === 'ar-en') {
            text = opt.english;
        } else {
            text = opt.arabic_diacritics || opt.arabic;
        }
        
        btn.textContent = text;
        btn.onclick = () => checkAnswer(opt.id, question.id, btn);
        quizOptions.appendChild(btn);
    });
}

function checkAnswer(selectedId, correctId, btnElement) {
    // Disable all options
    const allOptions = document.querySelectorAll('.quiz-option');
    allOptions.forEach(opt => opt.style.pointerEvents = 'none');
    
    const isCorrect = selectedId === correctId;
    
    if (isCorrect) {
        btnElement.classList.add('correct');
        quizScore++;
        
        quizFeedback.className = 'quiz-feedback correct';
        feedbackTitle.textContent = 'Correct!';
        feedbackText.textContent = '';
    } else {
        btnElement.classList.add('wrong');
        
        // Highlight correct option
        allOptions.forEach(opt => {
            const question = quizQuestions[currentQuestionIndex];
            const correctText = quizMode === 'ar-en' ? question.english : (question.arabic_diacritics || question.arabic);
            if (opt.textContent === correctText) {
                opt.classList.add('correct');
            }
        });
        
        quizFeedback.className = 'quiz-feedback wrong';
        feedbackTitle.textContent = 'Incorrect';
        const question = quizQuestions[currentQuestionIndex];
        const correctText = quizMode === 'ar-en' ? question.english : (question.arabic_diacritics || question.arabic);
        feedbackText.textContent = `Correct answer: ${correctText}`;
    }
    
    quizFeedback.style.display = 'flex';
}

function nextQuestion() {
    currentQuestionIndex++;
    if (currentQuestionIndex < quizQuestions.length) {
        showQuestion();
    } else {
        showResults();
    }
}

function showResults() {
    quizGameView.style.display = 'none';
    quizResultView.style.display = 'block';
    
    const percentage = Math.round((quizScore / quizQuestions.length) * 100);
    document.getElementById('resultScore').textContent = `${percentage}%`;
    
    let msg = 'Keep practicing!';
    if (percentage === 100) msg = 'Perfect Score! 🎉';
    else if (percentage >= 80) msg = 'Great Job! 👏';
    else if (percentage >= 50) msg = 'Good effort! 💪';
    
    document.getElementById('resultMessage').textContent = msg;
}

// --- Theme Toggle ---
const themeToggle = document.getElementById('themeToggle');

function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.setAttribute('data-theme', 'dark');
        updateThemeIcon('dark');
    }
}

function updateThemeIcon(theme) {
    if (themeToggle) {
        themeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

if (themeToggle) {
    themeToggle.addEventListener('click', toggleTheme);
}

// Initialize theme on page load
initTheme();

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    fetchWords();
    fetchTags();
    fetchWordGroups();
    fetchSettings();
});
