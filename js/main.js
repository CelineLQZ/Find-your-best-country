// This file initializes the application and handles user interactions.

import { loadCountries } from './utils/dataLoader.js';
import { Recommender } from './services/recommender.js';
import { renderUI } from './components/ui.js';

document.addEventListener('DOMContentLoaded', async () => {
    const countries = await loadCountries();
    const recommender = new Recommender(countries);
    
    renderUI(recommender);
});