document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu functionality (if needed in the future)
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', (event) => {
            if (!mobileMenu.contains(event.target) && !mobileMenuButton.contains(event.target)) {
                mobileMenu.classList.add('hidden');
            }
        });
    }

    // Create the ticket purchases chart
    const ticketPurchasesChart = document.getElementById('ticketPurchasesChart');
    if (ticketPurchasesChart) {
        const ctx = ticketPurchasesChart.getContext('2d');
        const weeklySalesData = JSON.parse(document.getElementById('weekly-sales-data').textContent);
        const labels = Object.keys(weeklySalesData).sort();
        const datasets = [];
        const companies = new Set();
        
        // Get all unique company names
        labels.forEach(week => {
            Object.keys(weeklySalesData[week]).forEach(company => companies.add(company));
        });
        
        // Create a dataset for each company
        const colors = ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(75, 192, 192, 1)', 'rgba(255, 206, 86, 1)', 'rgba(153, 102, 255, 1)'];
        [...companies].forEach((company, index) => {
            datasets.push({
                label: company,
                data: labels.map(week => weeklySalesData[week][company] || 0),
                borderColor: colors[index % colors.length],
                tension: 0.4
            });
        });
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: datasets
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Ticket Purchases by Company'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }  
});