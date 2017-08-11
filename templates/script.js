var ctx = document.getElementById('commitsByMonthChart');
var commitsByDomainChart = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [
            {
                label: 'Number of commits',
                data: [
                    {% for x in commits_by_month %}
                        {'x': '{{ x[0] }}-01', 'y': {{ x[1] }}},
                    {% endfor %}
                ]
            }
        ]
    },
    options: {
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    unit: 'month',
                    displayFormats: {
                        month: 'YYYY-MM'
                    }
                }
            }]
        }
    }
})
