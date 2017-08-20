window.onload = function() {
    var commitsByMonthChart = new Chart(document.getElementById('commitsByMonthChart'), {
        type: 'bar',
        data: {
            labels: {{ date_labels|tojson() }},
            datasets: [{
                label: 'Number of commits',
                data: {{ commits_by_month|tojson() }}
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    gridLines: {
                        display: false
                    }
                }]
            }
        }
    });
    var linesByMonthChart = new Chart(document.getElementById('linesByMonthChart'), {
        type: 'line',
        data: {
            labels: {{ date_labels|tojson() }},
            datasets: [
                {% for key, value in lines_by_month.items() %}
                    {
                        label: '{{ key }}',
                        data: {{ value|tojson() }}
                    },
                {% endfor %}
            ]
        },
        options: {
            elements: {
                line: {
                    tension: 0
                }
            },
            scales: {
                xAxes: [{
                    gridLines: {
                        display: false
                    }
                }],
                yAxes: [{
                    stacked: true,
                    ticks: {
                        callback: function(value, index, values) {
                            return (value / 1000) + ' k';
                        }
                    }
                }]
            }
        }
    });
};
