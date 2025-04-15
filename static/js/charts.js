// 渲染图表函数
function renderChart(chartId, data, chart) {
    let option = {};
    
    // 商品销量排行
    if (chartId === 'chart1') {
        option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                data: data.categories,
                axisTick: { alignWithLabel: true },
                axisLabel: { rotate: 45 }
            },
            yAxis: { type: 'value', name: '销量' },
            series: [
                {
                    name: '销量',
                    type: 'bar',
                    barWidth: '60%',
                    data: data.series[0].data,
                    itemStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: '#83bff6' },
                            { offset: 0.5, color: '#188df0' },
                            { offset: 1, color: '#188df0' }
                        ])
                    }
                }
            ]
        };
    }
    // 商品价格分布
    else if (chartId === 'chart2') {
        option = {
            title: [
                {
                    text: '价格分布箱线图',
                    left: 'center'
                }
            ],
            tooltip: {
                trigger: 'item',
                formatter: function(params) {
                    return `<div>
                        <p>最大值: ${data.max}</p>
                        <p>上四分位: ${data.q3}</p>
                        <p>中位数: ${data.median}</p>
                        <p>下四分位: ${data.q1}</p>
                        <p>最小值: ${data.min}</p>
                    </div>`;
                }
            },
            grid: {
                left: '10%',
                right: '10%',
                bottom: '15%'
            },
            xAxis: {
                type: 'category',
                data: ['价格分布'],
                boundaryGap: true,
                nameGap: 30,
                splitArea: { show: false },
                axisLabel: { show: true },
                splitLine: { show: false }
            },
            yAxis: {
                type: 'value',
                name: '价格',
                splitArea: { show: true }
            },
            series: [
                {
                    name: '价格',
                    type: 'boxplot',
                    datasetIndex: 0,
                    tooltip: { trigger: 'item' },
                    data: [
                        [data.min, data.q1, data.median, data.q3, data.max]
                    ],
                    itemStyle: {
                        borderColor: '#1890ff'
                    }
                },
                {
                    name: '异常值',
                    type: 'scatter',
                    datasetIndex: 0,
                    data: data.outliers,
                    itemStyle: {
                        color: '#fc8452'
                    }
                }
            ]
        };
    }
    // 店铺销量/销售额排行
    else if (chartId === 'chart3') {
        option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['销售额', '销量'],
                top: 10
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                data: data.categories,
                axisLabel: { rotate: 45 }
            },
            yAxis: [
                {
                    type: 'value',
                    name: '销售额',
                    position: 'left'
                },
                {
                    type: 'value',
                    name: '销量',
                    position: 'right'
                }
            ],
            series: [
                {
                    name: '销售额',
                    type: 'bar',
                    data: data.series[0].data,
                    yAxisIndex: 0,
                    itemStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: '#3498db' },
                            { offset: 1, color: '#2980b9' }
                        ])
                    }
                },
                {
                    name: '销量',
                    type: 'bar',
                    data: data.series[1].data,
                    yAxisIndex: 1,
                    itemStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: '#2ecc71' },
                            { offset: 1, color: '#27ae60' }
                        ])
                    }
                }
            ]
        };
    }
    // 地域分布
    else if (chartId === 'chart4') {
        option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                data: data.categories,
                axisLabel: { rotate: 45 }
            },
            yAxis: { type: 'value', name: '销量' },
            series: [
                {
                    name: '销量',
                    type: 'bar',
                    data: data.series[0].data,
                    itemStyle: {
                        color: function(params) {
                            const colorList = [
                                '#c23531', '#2f4554', '#61a0a8', '#d48265',
                                '#91c7ae', '#749f83', '#ca8622', '#bda29a',
                                '#6e7074', '#546570', '#c4ccd3'
                            ];
                            return colorList[params.dataIndex % colorList.length];
                        }
                    }
                }
            ]
        };
    }
    // 包邮 vs 非包邮的销量比较
    else if (chartId === 'chart5') {
        option = {
            tooltip: {
                trigger: 'item',
                formatter: '{a} <br/>{b}: {c} ({d}%)'
            },
            legend: {
                orient: 'vertical',
                left: 'left',
                data: data.map(item => item.name)
            },
            series: [
                {
                    name: '销量分布',
                    type: 'pie',
                    radius: ['40%', '70%'],
                    avoidLabelOverlap: false,
                    itemStyle: {
                        borderRadius: 10,
                        borderColor: '#fff',
                        borderWidth: 2
                    },
                    label: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        label: {
                            show: true,
                            fontSize: '20',
                            fontWeight: 'bold'
                        }
                    },
                    labelLine: {
                        show: false
                    },
                    data: data.map(item => ({
                        value: item.value,
                        name: item.name
                    }))
                }
            ]
        };
    }
    // 总销售额分析
    else if (chartId === 'chart6') {
        option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                data: data.categories,
                axisLabel: { rotate: 45 }
            },
            yAxis: { type: 'value', name: '商品数量' },
            series: [
                {
                    name: '商品数量',
                    type: 'bar',
                    data: data.series[0].data,
                    itemStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: '#f39c12' },
                            { offset: 1, color: '#d35400' }
                        ])
                    }
                }
            ]
        };
    }
    // 标题关键词分析（词云图）
    else if (chartId === 'chart7') {
        option = {
            title: {
                text: '商品标题关键词',
                left: 'center'
            },
            tooltip: {
                show: true,
                formatter: function(params) {
                    return params.name + ': ' + params.value;
                }
            },
            series: [{
                type: 'wordCloud',
                shape: 'circle',
                keepAspect: false,
                left: 'center',
                top: 'center',
                width: '90%',
                height: '80%',
                right: null,
                bottom: null,
                sizeRange: [12, 60],
                rotationRange: [-45, 45],
                rotationStep: 5,
                gridSize: 8,
                drawOutOfBound: false,
                layoutAnimation: true,
                textStyle: {
                    fontFamily: 'sans-serif',
                    fontWeight: 'bold',
                    color: function() {
                        return 'rgb(' + 
                            Math.round(Math.random() * 200) + ',' + 
                            Math.round(Math.random() * 200) + ',' + 
                            Math.round(Math.random() * 200) + ')';
                    }
                },
                emphasis: {
                    focus: 'self',
                    textStyle: {
                        shadowBlur: 10,
                        shadowColor: '#333'
                    }
                },
                data: data.map(function(item) {
                    return {
                        name: item.name,
                        value: item.value
                    };
                })
            }]
        };
    }
    
    // 设置图表
    chart.setOption(option, true);
}