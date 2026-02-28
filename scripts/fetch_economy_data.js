import fs from 'fs';
import https from 'https';

// Make HTTPS requests
function makeRequest(url) {
    return new Promise((resolve, reject) => {
        https.get(url, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(data));
                } catch (e) {
                    resolve(null);
                }
            });
        }).on('error', reject);
    });
}

// Get country code from REST Countries API
async function getCountryCode(countryName) {
    try {
        const url = `https://restcountries.com/v3.1/name/${encodeURIComponent(countryName)}`;
        const data = await makeRequest(url);
        
        if (data && data.length > 0) {
            return data[0].cca3; // Return 3-letter country code
        }
        return null;
    } catch (error) {
        return null;
    }
}

// Get economy data from World Bank API
async function getEconomyData(countryCode) {
    try {
        const indicators = {
            'gdp': 'NY.GDP.MKTP.CD',           // GDP (current US$)
            'gdp_per_capita': 'NY.GDP.PCAP.CD', // GDP per capita (current US$)
            'population': 'SP.POP.TOTL',        // Population
            'inflation': 'FP.CPI.TOTL.ZG',      // Inflation rate
            'gni_per_capita': 'NY.GNP.PCAP.CD'  // GNI per capita
        };

        const economyData = {};
        
        for (const [key, indicator] of Object.entries(indicators)) {
            try {
                const url = `https://api.worldbank.org/v2/country/${countryCode}/indicator/${indicator}?format=json&per_page=1&date=2022`;
                const response = await makeRequest(url);
                
                if (response && response[1] && response[1][0] && response[1][0].value) {
                    economyData[key] = response[1][0].value;
                } else {
                    economyData[key] = null;
                }
            } catch (e) {
                economyData[key] = null;
            }
            
            // Rate limiting - wait a bit between requests
            await new Promise(resolve => setTimeout(resolve, 500));
        }
        
        return economyData;
    } catch (error) {
        console.error(`Error fetching economy data for ${countryCode}:`, error.message);
        return null;
    }
}

// Main function
async function fetchEconomyData() {
    try {
        // Read country names from CSV
        const csvData = fs.readFileSync('./data/country_name.csv', 'utf-8');
        const countries = csvData.split('\n')
            .slice(1) // Skip header
            .map(line => line.trim())
            .filter(line => line.length > 0);

        console.log(`Found ${countries.length} countries to process...`);

        const economyDataset = [];
        let processedCount = 0;

        for (const country of countries) {
            try {
                console.log(`Processing: ${country} (${processedCount + 1}/${countries.length})`);
                
                // Get country code
                const countryCode = await getCountryCode(country);
                
                if (!countryCode) {
                    console.warn(`⚠️  Could not find country code for: ${country}`);
                    economyDataset.push({
                        country_name: country,
                        country_code: null,
                        error: 'Country code not found'
                    });
                } else {
                    // Get economy data
                    const economyData = await getEconomyData(countryCode);
                    
                    economyDataset.push({
                        country_name: country,
                        country_code: countryCode,
                        year: 2022,
                        ...economyData
                    });
                    console.log(`✓ Successfully fetched data for: ${country}`);
                }
                
                processedCount++;
                
                // Rate limiting - wait between countries
                await new Promise(resolve => setTimeout(resolve, 1000));
                
            } catch (error) {
                console.error(`Error processing ${country}:`, error.message);
                economyDataset.push({
                    country_name: country,
                    error: error.message
                });
            }
        }

        // Save to JSON file
        fs.writeFileSync(
            './data/economy_situation.json',
            JSON.stringify(economyDataset, null, 2),
            'utf-8'
        );

        console.log(`\n✅ Complete! Data saved to ./data/economy_situation.json`);
        console.log(`Processed: ${processedCount} countries`);
        console.log(`Successful: ${economyDataset.filter(d => !d.error).length}`);
        console.log(`Failed: ${economyDataset.filter(d => d.error).length}`);

    } catch (error) {
        console.error('Fatal error:', error);
    }
}

// Run the script
fetchEconomyData();
