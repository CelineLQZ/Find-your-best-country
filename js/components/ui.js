export function renderCountryCards(countries) {
    const resultsContainer = document.getElementById('results-container');
    resultsContainer.innerHTML = '';

    if (countries.length === 0) {
        resultsContainer.innerHTML = '<p>No countries match your preferences.</p>';
        return;
    }

    countries.forEach((country, index) => {
        const card = createCountryCard(country);
        resultsContainer.appendChild(card);
    });
}

function createCountryCard(country) {
    const card = document.createElement('div');
    card.className = 'country-card';

    const header = document.createElement('div');
    header.className = 'country-card-header';
    header.innerHTML = `
        <h3>${country.name}</h3>
        <span class="rank-badge">Rank #${country.rank}</span>
    `;

    const body = document.createElement('div');
    body.className = 'country-card-body';

    const scoreDisplay = document.createElement('div');
    scoreDisplay.className = 'score-display';
    scoreDisplay.innerHTML = `
        <div class="score-number">${country.score}%</div>
        <div class="score-label">Match Score</div>
    `;

    const infoDiv = document.createElement('div');
    infoDiv.className = 'country-info';

    const info = [
        { label: 'Education Quality', value: formatScore(country.educationQuality) },
        { label: 'Living Cost', value: formatCost(country.livingCosts) },
        { label: 'Job Opportunities', value: formatScore(country.jobOpportunities) },
        { label: 'Cultural Diversity', value: formatScore(country.culturalDiversity) }
    ];

    info.forEach(item => {
        const infoItem = document.createElement('div');
        infoItem.className = 'info-item';
        infoItem.innerHTML = `
            <span class="info-label">${item.label}</span>
            <span class="info-value">${item.value}</span>
        `;
        infoDiv.appendChild(infoItem);
    });

    body.appendChild(scoreDisplay);
    body.appendChild(infoDiv);

    card.appendChild(header);
    card.appendChild(body);

    return card;
}

function formatScore(score) {
    if (score >= 8) return '⭐⭐⭐ Excellent';
    if (score >= 6) return '⭐⭐ Good';
    if (score >= 4) return '⭐ Fair';
    return 'Limited';
}

function formatCost(cost) {
    if (cost <= 3) return '💰 Low';
    if (cost <= 5) return '💰💰 Medium';
    return '💰💰💰 High';
}