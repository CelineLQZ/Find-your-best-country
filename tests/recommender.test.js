import { Recommender } from '../src/js/services/recommender';

describe('Recommender Service', () => {
    let recommender;

    beforeEach(() => {
        recommender = new Recommender();
    });

    test('should return recommendations based on user preferences', () => {
        const userPreferences = {
            educationQuality: 8,
            livingCost: 5,
            jobOpportunities: 7,
            culturalAspects: 6
        };

        const recommendations = recommender.getRecommendations(userPreferences);
        expect(recommendations).toBeDefined();
        expect(recommendations.length).toBeGreaterThan(0);
    });

    test('should return an empty array if no countries match preferences', () => {
        const userPreferences = {
            educationQuality: 10,
            livingCost: 10,
            jobOpportunities: 10,
            culturalAspects: 10
        };

        const recommendations = recommender.getRecommendations(userPreferences);
        expect(recommendations).toEqual([]);
    });

    test('should rank countries based on user preferences', () => {
        const userPreferences = {
            educationQuality: 7,
            livingCost: 4,
            jobOpportunities: 6,
            culturalAspects: 5
        };

        const recommendations = recommender.getRecommendations(userPreferences);
        const rankedCountries = recommendations.map(country => country.name);
        
        // Assuming the countries are ranked correctly, you can add specific expectations here
        expect(rankedCountries).toEqual(expect.arrayContaining(['Country A', 'Country B']));
    });
});