function createCountryCard(country) {
    const card = document.createElement('div');
    card.classList.add('country-card');

    const countryName = document.createElement('h2');
    countryName.textContent = country.name;
    card.appendChild(countryName);

    const countryInfo = document.createElement('p');
    countryInfo.textContent = `Education Quality: ${country.educationQuality}, Living Costs: ${country.livingCosts}, Job Opportunities: ${country.jobOpportunities}, Cultural Aspects: ${country.culturalAspects}`;
    card.appendChild(countryInfo);

    return card;
}

export default createCountryCard;