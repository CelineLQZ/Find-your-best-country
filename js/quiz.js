// Quiz questions configuration - aligned with dataset metrics
export const quizQuestions = [
    {
        id: 1,
        question: "What is your priority for education quality?",
        type: "single",
        options: [
            { value: "high", label: "High - World-class education system" },
            { value: "medium", label: "Medium - Good education quality" },
            { value: "low", label: "Low - Basic education quality" }
        ]
    },
    {
        id: 2,
        question: "What is your preferred living cost level?",
        type: "single",
        options: [
            { value: "low", label: "Low - Budget-friendly living" },
            { value: "medium", label: "Medium - Comfortable living" },
            { value: "high", label: "High - Higher cost of living" }
        ]
    },
    {
        id: 3,
        question: "How important are job opportunities for you?",
        type: "single",
        options: [
            { value: "high", label: "High - Strong job market needed" },
            { value: "medium", label: "Medium - Decent opportunities" },
            { value: "low", label: "Low - Not a major priority" }
        ]
    },
    {
        id: 4,
        question: "How important is safety and security?",
        type: "single",
        options: [
            { value: "high", label: "High - Very safe environment" },
            { value: "medium", label: "Medium - Reasonably safe" },
            { value: "low", label: "Low - Not a major concern" }
        ]
    },
    {
        id: 5,
        question: "How important is healthcare quality?",
        type: "single",
        options: [
            { value: "high", label: "High - Excellent healthcare system" },
            { value: "medium", label: "Medium - Adequate healthcare" },
            { value: "low", label: "Low - Not a major priority" }
        ]
    },
    {
        id: 6,
        question: "What type of climate do you prefer?",
        type: "single",
        options: [
            { value: "tropical", label: "Tropical - Warm and humid" },
            { value: "temperate", label: "Temperate - Mild seasons" },
            { value: "cold", label: "Cold - Cold winters" }
        ]
    }
];

class QuizManager {
    constructor() {
        this.currentQuestion = 0;
        this.answers = {};
        this.totalQuestions = quizQuestions.length;
    }

    getCurrentQuestion() {
        return quizQuestions[this.currentQuestion];
    }

    getProgress() {
        return ((this.currentQuestion + 1) / this.totalQuestions) * 100;
    }

    setAnswer(questionId, answer) {
        this.answers[questionId] = answer;
    }

    getAnswers() {
        return this.answers;
    }

    nextQuestion() {
        if (this.currentQuestion < this.totalQuestions - 1) {
            this.currentQuestion++;
            return true;
        }
        return false;
    }

    previousQuestion() {
        if (this.currentQuestion > 0) {
            this.currentQuestion--;
            return true;
        }
        return false;
    }

    isLastQuestion() {
        return this.currentQuestion === this.totalQuestions - 1;
    }

    isFirstQuestion() {
        return this.currentQuestion === 0;
    }

    reset() {
        this.currentQuestion = 0;
        this.answers = {};
    }
}

export default QuizManager;
