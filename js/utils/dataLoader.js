export async function loadCountries() {
    try {
        const response = await fetch('./data/countries.json');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error loading country data:', error);
        return [];
    }
}