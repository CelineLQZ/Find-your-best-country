// Quiz questions configuration
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
            { value: "high", label: "High - Luxury living" }
        ]
    },
    {
        id: 3,
        question: "How important are job opportunities for you?",
        type: "single",
        options: [
            { value: "high", label: "Very important - Strong job market" },
            { value: "medium", label: "Somewhat important - Decent opportunities" },
            { value: "low", label: "Not important - Retiring or self-employed" }
        ]
    },
    {
        id: 4,
        question: "What type of climate do you prefer?",
        type: "single",
        options: [
            { value: "tropical", label: "Tropical - Warm and humid" },
            { value: "temperate", label: "Temperate - Mild seasons" },
            { value: "cold", label: "Cold - Cold winters" }
        ]
    },
    {
        id: 5,
        question: "How important is cultural diversity to you?",
        type: "single",
        options: [
            { value: "high", label: "Very important - Multicultural environment" },
            { value: "medium", label: "Somewhat important - Some diversity" },
            { value: "low", label: "Not important - Homogeneous culture" }
        ]
    },
    {
        id: 6,
        question: "What is your ideal population size?",
        type: "single",
        options: [
            { value: "small", label: "Small - Less than 5 million" },
            { value: "medium", label: "Medium - 5-50 million" },
            { value: "large", label: "Large - Over 50 million" }
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
