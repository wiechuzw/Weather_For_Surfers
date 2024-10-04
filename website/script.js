const ctx = document.getElementById('weatherChart').getContext('2d');
const weatherChart = new Chart(ctx, {
    type: 'line', // Rodzaj wykresu, np. 'line' (liniowy), 'bar' (słupkowy)
    data: {
        labels: ['Pon', 'Wt', 'Śr', 'Czw', 'Pt', 'Sob', 'Ndz'], // Dni tygodnia
        datasets: [{
            label: 'Prognoza Temperatury (°C)',
            data: [12, 19, 3, 5, 2, 3, 9], // Przykładowe dane
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
