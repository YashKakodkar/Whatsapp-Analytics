function memberTable() {
    var table = document.getElementById('memberTable');

    jsonData.members.forEach(function (member) {
        var tr = document.createElement('tr');
        tr.innerHTML = '<td>' + member.name + '</td>';
        if (member.activeStatus) {
            tr.innerHTML += '<td class="active">' + "ACTIVE" + '</td>';
        } else {
            tr.innerHTML += '<td class="inactive">' + "INACTIVE" + '</td>';
        }
        tr.innerHTML += //'<td>' + member.dateAdded + '</td>' +
            '<td>' + member.messagesSent + '</td>' +
            '<td>' + member.timesAdded + '</td>' +
            '<td>' + member.timesRemoved + '</td>' +
            '<td>' + member.timesLeft + '</td>';
        table.appendChild(tr);
    });
}


function memberPieChart() {
    var members = jsonData.members.map(function (e) {
        return e.name;
    });
    var data = jsonData.members.map(function (e) {
        return e.messagesSent;
    });


    // for (i = 0; i < data.length; i++) {
    //     colors.push(randomColor())
    // }

    var pieData = {
        labels: members,
        datasets: [{
            data: data,
            backgroundColor: colors,
            borderColor: 'rgba(0, 0, 0, 0)'
        }]
    }
    var ctx = document.getElementById("messagePieChart").getContext("2d");
    // create the chart using the chart canvas
    var messagePieChart = new Chart(ctx, {
        type: 'pie',
        data: pieData,
        options: {
            maintainAspectRatio: false,
            responsive: true,
            legend: {
                labels: {
                    fontColor: 'rgba(255, 255, 255, 0.6)'
                },
                position: 'right'
            },
            layout: {
                padding: {
                    left: 0,
                    right: 0,
                    top: 0,
                    bottom: 0
                }
            }
        }
    });
}


//2
function memberActivityChart() {
    memberDatasets = []
    memberBarDatasets = []
    for (i = 0; i < jsonData.members.length; i++) {
        var data = jsonData.members[i].memberChatLog.map(function (e) {
            return e.amount;
        });;
        color = colors[i]
        var dataset = {
            label: jsonData.members[i].name,
            fill: false,
            lineTension: 0.1,
            borderWidth: 2,
            borderColor: color,
            backgroundColor: color,
            pointBackgroundColor: color,
            pointRadius: 0,
            pointHoverRadius: 5,
            data: data,
        };
        var barDataset = {
            label: jsonData.members[i].name,
            backgroundColor: color,
            data: data
        };
        memberBarDatasets.push(barDataset);
        memberDatasets.push(dataset);
    }

    var memberChartData = {
        labels: labels,
        datasets: memberDatasets
    };

    var barChartData = {
        labels: labels,
        datasets: memberBarDatasets
    };

    // get chart canvas
    var ctx = document.getElementById("memberChart").getContext("2d");

    // create the chart using the chart canvas
    var memberChart = new Chart(ctx, {
        type: 'line',
        data: memberChartData,
        options: {
            legend: {
                labels: {
                    fontColor: 'rgba(255, 255, 255, 0.6)'
                }
            },
            scales: {
                xAxes: [{
                    ticks: {
                        fontColor: 'rgba(255, 255, 255, 0.4)',
                        padding: 15

                    },
                    gridLines: {
                        color: 'rgba(255, 255, 255, 0.1)',
                        zeroLineColor: 'rgba(255, 255, 255, 0.1)',
                        tickMarkLength: 0
                    }
                }],
                yAxes: [{
                    ticks: {
                        fontColor: 'rgba(255, 255, 255, 0.4)',
                        padding: 15
                    },
                    gridLines: {
                        color: 'rgba(255, 255, 255, 0.1)',
                        zeroLineColor: 'rgba(255, 255, 255, 0.1)',
                        tickMarkLength: 0,
                        display: false,
                        zeroLineWidth: 0
                    }
                }]
            }
        }
    });

    var ctx = document.getElementById("memberBarChart").getContext("2d");

    var memberBarChart = new Chart(ctx, {
        type: 'bar',
        data: barChartData,
        options: {
            tooltips: {
                mode: 'index',
                intersect: false
            },
            responsive: true,
            legend: {
                display: false
            },
            scales: {
                xAxes: [{
                    stacked: true,
                    ticks: {
                        fontColor: 'rgba(255, 255, 255, 0.4)',
                        padding: 15
                    },
                    gridLines: {
                        color: 'rgba(255, 255, 255, 0.1)',
                        zeroLineColor: 'rgba(255, 255, 255, 0.1)',
                        tickMarkLength: 0,
                        display: false,
                        zeroLineWidth: 0
                    }
                }],
                yAxes: [{
                    stacked: true,
                    ticks: {
                        fontColor: 'rgba(255, 255, 255, 0.4)',
                        padding: 15

                    },
                    gridLines: {
                        color: 'rgba(255, 255, 255, 0.1)',
                        zeroLineColor: 'rgba(255, 255, 255, 0.1)',
                        tickMarkLength: 0
                    }
                }]
            }
        }
    });
}

//3
function activityChart() {
    var data = jsonData.chatLog.map(function (e) {
        return e.amount;
    });;

    var ctx = document.getElementById("myChart").getContext("2d");
    var gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0.1, 'rgba(42,192,181,1)');
    gradient.addColorStop(0.5, 'rgba(42,192,181,0.6)');
    gradient.addColorStop(0.8, 'rgba(33,174,162,0.20)');
    gradient.addColorStop(1, 'rgba(31,190,165,0.05)');

    var chartData = {
        labels: labels,
        datasets: [{
            label: 'Chat Activity',
            fill: true,
            lineTension: 0.1,
            backgroundColor: gradient,
            borderColor: "#29C0B5",
            borderWidth: 2,
            pointBackgroundColor: "#29C0B5",
            pointRadius: 0,
            pointHoverRadius: 5,
            data: data,
        }]
    };
    // get chart canvas

    // create the chart using the chart canvas
    var myChart = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
            legend: {
                labels: {
                    fontColor: 'rgba(255, 255, 255, 0.6)'
                }
            },
            scales: {
                xAxes: [{
                    ticks: {
                        fontColor: 'rgba(255, 255, 255, 0.4)',
                        padding: 15
                    },
                    gridLines: {
                        color: 'rgba(255, 255, 255, 0.1)',
                        zeroLineColor: 'rgba(255, 255, 255, 0.1)',
                        tickMarkLength: 0
                    }
                }],
                yAxes: [{
                    ticks: {
                        fontColor: 'rgba(255, 255, 255, 0.4)',
                        padding: 15
                    },
                    gridLines: {
                        color: 'rgba(255, 255, 255, 0.1)',
                        zeroLineColor: 'rgba(255, 255, 255, 0.1)',
                        tickMarkLength: 0,
                        display: false,
                        zeroLineWidth: 0
                    }
                }]
            }
        }
    });
}
