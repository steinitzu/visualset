var chart = new Highcharts.Chart({

    chart: {
        renderTo: 'container',
        animation: false
    },
    
    title: {
        text: 'Energy levels'
    },

    xAxis: {
        min: 0,
        max: 60,
        title: {text: 'Duration (minutes)'}
    },
    yAxis: {
        min: 0,
        max: 100,
        title: {text: 'Energy!'},
    },

    plotOptions: {
        series: {
            point: {
                events: {
                    drag: function (e) {  

                    },
                    drop: function () {
                        console.log(this)
                    }
                }
            },
            stickyTracking: false
        },
        column: {
            stacking: 'normal'
        },
        line: {
            cursor: 'ns-resize'
        }
    },

    tooltip: {
        yDecimals: 0
    },

    series: [{
        data: [
            {x: 0, y: 50},
            {x: 12, y: 50},
            {x: 24, y: 50},
            {x: 36, y: 50},
            {x: 48, y: 50},
            {x: 60, y: 50},                       
        ],
        draggableY: true,
        dragPrecisionY: 5,
        dragMaxY: 100,
        dragMinY: 0,
        cursor: 'move',
    }]

});


function sendData() {
    let data = chart.series[0].data
    let json = {'points': []}
    data.forEach(function(point) {
        json.points.push({
            energy: point.y,
            minute: point.x
        })                
    })
    fetch('http://localhost:8000/api/lines', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(json)
    })
          
    
}
            
