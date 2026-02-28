class Recommender {
    constructor(countriesData) {
        this.countriesData = countriesData;
    }

    recommendCountries(preferences) {
        // Map quiz answers to preference keys
        const mappedPreferences = this.mapQuizAnswers(preferences);
        
        // Score each country based on user preferences
        const rankedCountries = this.countriesData
            .map((country) => ({
                ...country,
                score: this.calculateScore(country, mappedPreferences),
                matchDetails: this.getMatchDetails(country, mappedPreferences)
            }))
            .filter(country => country.score > 0)
            .sort((a, b) => b.score - a.score)
            .map((country, index) => ({
                ...country,
                rank: index + 1
            }));

        return rankedCountries;
    }

    mapQuizAnswers(quizAnswers) {
        // Map quiz question IDs to preference keys
        return {
            education: quizAnswers[1],           // Question 1
            livingCosts: quizAnswers[2],         // Question 2
            jobOpportunities: quizAnswers[3],    // Question 3
            safety: quizAnswers[4],              // Question 4
            healthcare: quizAnswers[5],          // Question 5
            climate: quizAnswers[6]              // Question 6
        };
    }

    calculateScore(country, preferences) {
        let totalScore = 0;
        let maxScore = 0;
        let matchCount = 0;

        // 1. Education quality (25%)
        if (preferences.education && country.education_level) {
            const educationScore = this.getMatchScore(country.education_level, preferences.education);
            totalScore += educationScore * 0.25;
            maxScore += 0.25;
            matchCount++;
        }

        // 2. Living costs (25%) - inverted (lower cost = better match)
        if (preferences.livingCosts && country.cost_level) {
            const costScore = this.getCostMatchScore(country.cost_level, preferences.livingCosts);
            totalScore += costScore * 0.25;
            maxScore += 0.25;
            matchCount++;
        }

        // 3. Job opportunities (20%)
        if (preferences.jobOpportunities && country.economic_opportunity_level) {
            const jobScore = this.getMatchScore(country.economic_opportunity_level, preferences.jobOpportunities);
            totalScore += jobScore * 0.20;
            maxScore += 0.20;
            matchCount++;
        }

        // 4. Safety (15%)
        if (preferences.safety && country.safety_level) {
            const safetyScore = this.getMatchScore(country.safety_level, preferences.safety);
            totalScore += safetyScore * 0.15;
            maxScore += 0.15;
            matchCount++;
        }

        // 5. Healthcare (10%) - skip if data missing
        if (preferences.healthcare && country.healthcare_level) {
            const healthScore = this.getMatchScore(country.healthcare_level, preferences.healthcare);
            totalScore += healthScore * 0.10;
            maxScore += 0.10;
            matchCount++;
        }

        // 6. Climate (5%)
        if (preferences.climate && country.climate_preference) {
            const climateScore = this.getClimateMatchScore(country.climate_preference, preferences.climate);
            totalScore += climateScore * 0.05;
            maxScore += 0.05;
            matchCount++;
        }

        // Only return score if at least 3 preferences matched
        if (matchCount < 3) {
            return 0; // Skip countries with too little data
        }

        // Normalize to 0-10 scale
        return maxScore > 0 ? (totalScore / maxScore) * 10 : 0;
    }

    getMatchScore(countryLevel, preferenceLevel) {
        /**
         * Match scoring for high/medium/low levels
         * Perfect match: 10 points
         * One level difference: 8 points
         * Two level difference: 5 points (still acceptable)
         */
        if (!countryLevel || !preferenceLevel) {
            return 5; // Neutral if data missing
        }

        if (countryLevel === preferenceLevel) {
            return 10; // Perfect match
        }

        // One level difference
        if ((countryLevel === 'high' && preferenceLevel === 'medium') ||
            (countryLevel === 'medium' && preferenceLevel === 'high') ||
            (countryLevel === 'medium' && preferenceLevel === 'low') ||
            (countryLevel === 'low' && preferenceLevel === 'medium')) {
            return 8; // Better than before
        }

        // Two level difference - still acceptable instead of rejecting
        return 5; // Improved from 2
    }

    getCostMatchScore(costLevel, preferenceLevel) {
        /**
         * Special handling for cost preference
         * Lower cost preference wants lower cost level (1-3 ideal)
         * Medium cost preference wants middle numbers (4-7)
         * High cost preference wants higher numbers (8-10)
         */
        if (!costLevel || !preferenceLevel) {
            return 5;
        }

        // If prefer low cost, lower numbers are better
        if (preferenceLevel === 'low') {
            if (costLevel <= 4) return 10;
            if (costLevel <= 6) return 8;
            if (costLevel <= 8) return 5;
            return 2; // High cost when want low
        }

        // If prefer medium cost, middle numbers are better
        if (preferenceLevel === 'medium') {
            if (costLevel >= 4 && costLevel <= 7) return 10;
            if (costLevel >= 3 && costLevel <= 8) return 8;
            if (costLevel >= 2 && costLevel <= 9) return 5;
            return 2;
        }

        // If prefer high cost, higher numbers are better
        if (preferenceLevel === 'high') {
            if (costLevel >= 7) return 10;
            if (costLevel >= 5) return 8;
            if (costLevel >= 3) return 5;
            return 2; // Low cost when want high
        }

        return 5;
    }

    getClimateMatchScore(countryClimate, preferenceClimate) {
        /**
         * Exact match for climate preference
         */
        if (!countryClimate || !preferenceClimate) {
            return 5;
        }

        return countryClimate === preferenceClimate ? 10 : 3;
    }

    getMatchDetails(country, preferences) {
        /**
         * Return matching details for UI display
         */
        return {
            education: {
                country: country.education_level,
                match: this.getMatchScore(country.education_level, preferences.education)
            },
            livingCosts: {
                country: country.cost_level,
                match: this.getCostMatchScore(country.cost_level, preferences.livingCosts)
            },
            jobOpportunities: {
                country: country.economic_opportunity_level,
                match: this.getMatchScore(country.economic_opportunity_level, preferences.jobOpportunities)
            },
            safety: {
                country: country.safety_level,
                match: this.getMatchScore(country.safety_level, preferences.safety)
            },
            healthcare: {
                country: country.healthcare_level,
                match: this.getMatchScore(country.healthcare_level, preferences.healthcare)
            },
            climate: {
                country: country.climate_preference,
                match: this.getClimateMatchScore(country.climate_preference, preferences.climate)
            }
        };
    }
}

export default Recommender;
