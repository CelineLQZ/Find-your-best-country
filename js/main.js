// Main application file
import { loadCountries } from './utils/dataLoader.js';
import Recommender from './services/recommender.js';
import QuizManager, { quizQuestions } from './quiz.js';
import { renderCountryCards } from './components/ui.js';

let quizManager;
let recommender;
let countries = [];

document.addEventListener('DOMContentLoaded', async () => {
    // Load countries data
    countries = await loadCountries();
    recommender = new Recommender(countries);
    quizManager = new QuizManager();

    // Initialize event listeners
    initializeEventListeners();
});

function initializeEventListeners() {
    const startQuizBtn = document.getElementById('start-quiz-btn');
    const nextBtn = document.getElementById('next-btn');
    const prevBtn = document.getElementById('prev-btn');
    const finishBtn = document.getElementById('finish-btn');
    const retakeQuizBtn = document.getElementById('retake-quiz-btn');

    startQuizBtn.addEventListener('click', startQuiz);
    nextBtn.addEventListener('click', nextQuestion);
    prevBtn.addEventListener('click', previousQuestion);
    finishBtn.addEventListener('click', finishQuiz);
    retakeQuizBtn.addEventListener('click', retakeQuiz);
}

function startQuiz() {
    quizManager.reset();
    showPage('quiz-page');
    renderQuestion();
}

function renderQuestion() {
    const question = quizManager.getCurrentQuestion();
    const optionsContainer = document.getElementById('options-container');
    const questionText = document.getElementById('question-text');
    const progressFill = document.getElementById('progress-fill');
    const currentQuestionSpan = document.getElementById('current-question');

    // Update progress
    progressFill.style.width = quizManager.getProgress() + '%';
    currentQuestionSpan.textContent = quizManager.currentQuestion + 1;

    // Update question text
    questionText.textContent = question.question;

    // Clear and render options
    optionsContainer.innerHTML = '';

    question.options.forEach((option) => {
        const optionDiv = document.createElement('div');
        optionDiv.className = 'option';

        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = `question-${question.id}`;
        radio.value = option.value;
        radio.id = `option-${option.value}`;

        // Check if this answer was previously selected
        if (quizManager.answers[question.id] === option.value) {
            radio.checked = true;
        }

        const label = document.createElement('label');
        label.htmlFor = `option-${option.value}`;
        label.textContent = option.label;

        radio.addEventListener('change', () => {
            quizManager.setAnswer(question.id, option.value);
            updateNavigationButtons();
        });

        optionDiv.appendChild(radio);
        optionDiv.appendChild(label);
        optionsContainer.appendChild(optionDiv);
    });

    updateNavigationButtons();
}

function updateNavigationButtons() {
    const nextBtn = document.getElementById('next-btn');
    const prevBtn = document.getElementById('prev-btn');
    const finishBtn = document.getElementById('finish-btn');
    const currentQuestion = quizManager.getCurrentQuestion();
    const isAnswered = quizManager.answers[currentQuestion.id] !== undefined;

    // Update previous button visibility
    if (quizManager.isFirstQuestion()) {
        prevBtn.style.display = 'none';
    } else {
        prevBtn.style.display = 'block';
    }

    // Update next/finish button visibility and state
    if (quizManager.isLastQuestion()) {
        nextBtn.style.display = 'none';
        finishBtn.style.display = 'block';
        finishBtn.disabled = !isAnswered;
    } else {
        nextBtn.style.display = 'block';
        finishBtn.style.display = 'none';
        nextBtn.disabled = !isAnswered;
    }
}

function nextQuestion() {
    if (quizManager.nextQuestion()) {
        renderQuestion();
    }
}

function previousQuestion() {
    if (quizManager.previousQuestion()) {
        renderQuestion();
    }
}

function finishQuiz() {
    const preferences = convertAnswersToPreferences(quizManager.getAnswers());
    const recommendations = recommender.recommendCountries(preferences);
    
    renderCountryCards(recommendations);
    showPage('results-page');
}

function convertAnswersToPreferences(answers) {
    return {
        educationQuality: answers[1],
        livingCosts: answers[2],
        jobOpportunities: answers[3],
        climate: answers[4],
        culturalDiversity: answers[5],
        populationSize: answers[6]
    };
}

function retakeQuiz() {
    startQuiz();
}

function showPage(pageId) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });

    // Show selected page
    document.getElementById(pageId).classList.add('active');

    // Scroll to top
    window.scrollTo(0, 0);
}
