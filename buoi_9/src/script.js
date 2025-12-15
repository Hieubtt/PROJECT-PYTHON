const months = [
    'Tháng 1','Tháng 2','Tháng 3','Tháng 4','Tháng 5','Tháng 6',
    'Tháng 7','Tháng 8','Tháng 9','Tháng 10','Tháng 11','Tháng 12'
];

let revenueData = {
    A: [120,130,140,150,160,170,180,190,200,210,220,230],
    B: [100,110,120,130,140,150,160,170,180,190,200,210],
    C: [90,100,110,120,130,140,150,160,170,180,190,200]
};

let lineChart, donutChart;

function renderCharts(store = 'all') {
    let seriesData = [];
    let donutData = [];

    if (store === 'all') {
        Object.keys(revenueData).forEach(s => {
            seriesData.push({
                name: 'Cửa hàng ' + s,
                data: revenueData[s]
            });
            donutData.push({
                name: 'Cửa hàng ' + s,
                y: revenueData[s].reduce((a,b) => a + b, 0)
            });
        });
    } else {
        seriesData.push({
            name: 'Cửa hàng ' + store,
            data: revenueData[store]
        });
        donutData.push({
            name: 'Cửa hàng ' + store,
            y: revenueData[store].reduce((a,b) => a + b, 0)
        });
    }

    lineChart = Highcharts.chart('lineChart', {
        title: { text: 'Doanh thu theo tháng' },
        xAxis: { categories: months },
        yAxis: { title: { text: 'Doanh thu' } },
        series: seriesData,
        exporting: { enabled: true }
    });

    donutChart = Highcharts.chart('donutChart', {
        chart: { type: 'pie' },
        title: { text: 'Tỷ trọng doanh thu' },
        plotOptions: {
            pie: {
                innerSize: '60%',
                dataLabels: { enabled: true }
            }
        },
        series: [{
            name: 'Tổng doanh thu',
            data: donutData
        }],
        exporting: { enabled: true }
    });
}

document.getElementById('storeFilter').addEventListener('change', e => {
    renderCharts(e.target.value);
});

function updateData() {
    const store = document.getElementById('storeInput').value;
    const month = parseInt(document.getElementById('monthInput').value);
    const revenue = parseFloat(document.getElementById('revenueInput').value);

    if (isNaN(revenue)) {
        alert('Vui lòng nhập doanh thu hợp lệ');
        return;
    }

    revenueData[store][month] = revenue;
    renderCharts(document.getElementById('storeFilter').value);
}

renderCharts();
