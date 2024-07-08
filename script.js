async function fetchData() {
    const url = "https://data.ibb.gov.tr/api/3/action/datastore_search?resource_id=b742a205-1adb-4f99-8b04-6f3025feb404&limit=5";
    const dataContainer = document.getElementById('data-container');
    dataContainer.innerHTML = '<p>Loading...</p>';

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const records = data.result.records;

        dataContainer.innerHTML = '';
        records.forEach(record => {
            const recordElement = document.createElement('div');
            recordElement.className = 'record';
            recordElement.innerHTML = `
                <p><strong>İlçe:</strong> ${record.ilce}</p>
                <p><strong>Water Usage:</strong> ${record.usage} m³</p>
            `;
            dataContainer.appendChild(recordElement);
        });
    } catch (error) {
        dataContainer.innerHTML = `<p>Error: ${error.message}</p>`;
    }
}