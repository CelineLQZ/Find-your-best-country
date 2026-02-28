function renderCountryList(countries) {
    const countryListContainer = document.getElementById('country-list');
    countryListContainer.innerHTML = '';

    countries.forEach(country => {
        const countryCard = createCountryCard(country);
        countryListContainer.appendChild(countryCard);
    });
}

function createCountryCard(country) {
    const card = document.createElement('div');
    card.className = 'country-card';
    
    const countryName = document.createElement('h3');
    countryName.textContent = country.name;

    const countryDetails = document.createElement('p');
    countryDetails.textContent = `Education Quality: ${country.educationQuality}, Living Costs: ${country.livingCosts}, Job Opportunities: ${country.jobOpportunities}`;

    card.appendChild(countryName);
    card.appendChild(countryDetails);

    return card;
}

function renderForm(onSubmit) {
    const formContainer = document.getElementById('form-container');
    const form = document.createElement('form');

    const input = document.createElement('input');
    input.type = 'text';
    input.placeholder = 'Enter your preferences';
    form.appendChild(input);

    const submitButton = document.createElement('button');
    submitButton.type = 'submit';
    submitButton.textContent = 'Get Recommendations';
    form.appendChild(submitButton);

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        onSubmit(input.value);
    });

    formContainer.appendChild(form);
}

export { renderCountryList, renderForm };