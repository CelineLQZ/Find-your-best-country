class Recommender {
    constructor(countriesData) {
        this.countriesData = countriesData;
    }

    recommendCountries(preferences) {
        // Score each country based on user preferences
        const rankedCountries = this.countriesData
            .map((country, index) => ({
                ...country,
                score: this.calculateScore(country, preferences),
                rank: index + 1
            }))
            .filter(country => country.score > 0)
            .sort((a, b) => b.score - a.score)
            .map((country, index) => ({
                ...country,
                rank: index + 1
            }));

        return rankedCountries;
    }

    calculateScore(country, preferences) {
        let score = 0;
        let matchCount = 0;

        // Education Quality scoring (0-25 points)
        if (preferences.educationQuality) {
            const educationMap = { low: 3, medium: 6, high: 9 };
            const preferredScore = educationMap[preferences.educationQuality];
            if (country.educationQuality >= preferredScore) {
                score += 25;
                matchCount++;
            } else {
                score += Math.max(0, (country.educationQuality / preferredScore) * 25);
            }
        }

        // Living Costs scoring (0-25 points)
        if (preferences.livingCosts) {
            const costMap = { low: 3, medium: 5, high: 8 };
            const preferredCost = costMap[preferences.livingCosts];
            if (preferences.livingCosts === 'low' && country.livingCosts <= preferredCost) {
                score += 25;
                matchCount++;
            } else if (preferences.livingCosts === 'medium' && country.livingCosts >= 4 && country.livingCosts <= 6) {
                score += 25;
                matchCount++;
            } else if (preferences.livingCosts === 'high' && country.livingCosts >= 6) {
                score += 25;
                matchCount++;
            } else {
                score += 10;
            }
        }

        // Job Opportunities scoring (0-25 points)
        if (preferences.jobOpportunities) {
            const jobMap = { low: 3, medium: 6, high: 9 };
            const preferredJob = jobMap[preferences.jobOpportunities];
            if (country.jobOpportunities >= preferredJob) {
                score += 25;
                matchCount++;
            } else {
                score += Math.max(0, (country.jobOpportunities / preferredJob) * 25);
            }
        }

        // Cultural Diversity scoring (0-12.5 points)
        if (preferences.culturalDiversity) {
            const diversityScore = {
                high: 9,
                medium: 6,
                low: 3
            };
            if (country.culturalDiversity >= diversityScore[preferences.culturalDiversity]) {
                score += 12.5;
                matchCount++;
            }
        }

        // Climate preference scoring (0-12.5 points)
        if (preferences.climate && country.climate === preferences.climate) {
            score += 12.5;
            matchCount++;
        }

        return Math.round(score);
    }
}

export default Recommender;
