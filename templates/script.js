window.onload = function() {
    var ctx = document.getElementById('commitsByMonthChart');
    var commitsByDomainChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [
                {% for x in commits_by_month -%}
                    '{{ x[0] }}',
                {% endfor %}
            ],
            datasets: [
                {
                    label: 'Number of commits',
                    data: [
                        {% for x in commits_by_month -%}
                            {{ x[1] }},
                        {% endfor %}
                    ]
                }
            ]
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
};
