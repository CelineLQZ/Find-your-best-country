class Recommender {
    constructor(countriesData) {
        this.countriesData = countriesData;
    }

    recommendCountries(preferences) {
        const rankedCountries = this.countriesData
            .map(country => ({
                name: country.name,
                score: this.calculateScore(country, preferences)
            }))
            .filter(country => country.score > 0)
            .sort((a, b) => b.score - a.score);

        return rankedCountries;
    }

    calculateScore(country, preferences) {
        let score = 0;

        if (preferences.educationQuality && country.educationQuality >= preferences.educationQuality) {
            score += 1;
        }
        if (preferences.livingCost && country.livingCost <= preferences.livingCost) {
            score += 1;
        }
        if (preferences.jobOpportunities && country.jobOpportunities >= preferences.jobOpportunities) {
            score += 1;
        }
        if (preferences.culture && country.culture.includes(preferences.culture)) {
            score += 1;
        }

        return score;
    }
}

export default Recommender;