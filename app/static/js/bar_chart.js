document.addEventListener("DOMContentLoaded", () => {
    const days = window.chartData.days;
    const units = window.chartData.energy;
    /* BAR CHART */
    new Chart(document.getElementById("barChart"), {
        type: "bar",
        data: {
            labels: days,
            datasets: [{
                label: "Electricity Usage (kWh)",
                data: units,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    })
})