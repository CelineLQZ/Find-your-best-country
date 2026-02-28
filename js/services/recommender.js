class Recommender {
    constructor(countriesData) {
        this.countriesData = countriesData;
    }

    recommendCountries(preferences) {
        // 基于综合评分 + 用户偏好的简单混合推荐算法
        const rankedCountries = this.countriesData
            .map((country) => ({
                ...country,
                score: this.calculateScore(country, preferences)
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
        // 基础分数：使用综合评分（0-10）
        let baseScore = country.compositeScore || 0;
        
        // 偏好调整乘数（0.8 - 1.2）
        let multiplier = 1.0;

        // 生活成本偏好调整
        if (preferences.livingCosts && country.costLevel) {
            if (preferences.livingCosts === 'low' && country.costLevel < 5) {
                multiplier += 0.15; // 便宜国家 +15%
            } else if (preferences.livingCosts === 'medium' && country.costLevel >= 4 && country.costLevel <= 7) {
                multiplier += 0.1;  // 中等成本 +10%
            } else if (preferences.livingCosts === 'high' && country.costLevel > 7) {
                multiplier += 0.15; // 贵的国家 +15%
            } else {
                multiplier -= 0.1;  // 不符合 -10%
            }
        }

        // 生活质量偏好调整
        if (preferences.educationQuality && country.qualityLevel) {
            if (preferences.educationQuality === 'high' && country.qualityLevel >= 8) {
                multiplier += 0.2; // 高质量国家 +20%
            } else if (preferences.educationQuality === 'medium' && country.qualityLevel >= 6 && country.qualityLevel < 8) {
                multiplier += 0.1;
            } else if (preferences.educationQuality === 'low' && country.qualityLevel < 6) {
                multiplier += 0.05;
            }
        }

        // 安全偏好调整
        if (preferences.safety && country.safetyIndex) {
            if (preferences.safety === 'high' && country.safetyIndex > 70) {
                multiplier += 0.1;
            } else if (preferences.safety === 'medium' && country.safetyIndex >= 50 && country.safetyIndex <= 70) {
                multiplier += 0.05;
            }
        }

        // 医疗偏好调整
        if (preferences.healthcare && country.healthcareIndex) {
            if (preferences.healthcare === 'high' && country.healthcareIndex > 70) {
                multiplier += 0.1;
            } else if (preferences.healthcare === 'medium' && country.healthcareIndex >= 50 && country.healthcareIndex <= 70) {
                multiplier += 0.05;
            }
        }

        // 气候偏好调整
        if (preferences.climate && country.climateIndex) {
            const climateLevel = country.climateIndex / 10; // 归一化到 0-10
            if (preferences.climate === 'tropical' && climateLevel > 7) {
                multiplier += 0.1;
            } else if (preferences.climate === 'temperate' && climateLevel >= 5 && climateLevel <= 7) {
                multiplier += 0.1;
            } else if (preferences.climate === 'cold' && climateLevel < 5) {
                multiplier += 0.1;
            }
        }

        // 环境偏好调整
        if (preferences.environment && country.pollutionIndex) {
            if (preferences.environment === 'clean' && country.pollutionIndex < 50) {
                multiplier += 0.1;
            } else if (preferences.environment === 'moderate' && country.pollutionIndex >= 50 && country.pollutionIndex <= 75) {
                multiplier += 0.05;
            }
        }

        // 最终分数 = 基础分 × 乘数，限制在 0-10
        const finalScore = baseScore * multiplier;
        return Math.min(10, Math.max(0, finalScore));
    }
}

export default Recommender;
