// 渲染图表函数
function renderChart(chartId, data, chart) {
    let option = {};

    // 商品销量排行
    if (chartId === 'chart1') {
        // 创建商品详情列表
        if (data.product_details && data.product_details.length > 0) {
            // 获取产品详情容器
            const productDetailsContainer = document.getElementById('product-details-container');
            if (productDetailsContainer) {
                // 清除容器内容
                productDetailsContainer.innerHTML = '';

                // 创建标题
                const title = document.createElement('h3');
                title.className = 'product-list-title';
                title.textContent = '商品详情列表';
                productDetailsContainer.appendChild(title);

                // 创建表格
                const table = document.createElement('table');
                table.className = 'product-list-table';

                // 创建表头
                const thead = document.createElement('thead');
                const headerRow = document.createElement('tr');

                const idHeader = document.createElement('th');
                idHeader.textContent = '编号';
                idHeader.className = 'product-id-cell';

                const titleHeader = document.createElement('th');
                titleHeader.textContent = '商品名称';

                headerRow.appendChild(idHeader);
                headerRow.appendChild(titleHeader);
                thead.appendChild(headerRow);
                table.appendChild(thead);

                // 创建表体
                const tbody = document.createElement('tbody');

                // 添加数据行
                data.product_details.forEach(product => {
                    const row = document.createElement('tr');

                    const idCell = document.createElement('td');
                    idCell.textContent = product.id;
                    idCell.className = 'product-id-cell';

                    const titleCell = document.createElement('td');
                    titleCell.textContent = product.title;

                    row.appendChild(idCell);
                    row.appendChild(titleCell);
                    tbody.appendChild(row);
                });

                table.appendChild(tbody);
                productDetailsContainer.appendChild(table);
            }
        }

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
            title: {
                text: '垂钓饵料相关商品最近12个月销售额趋势',
                left: 'center'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross',
                    crossStyle: {
                        color: '#999'
                    }
                }
            },
            toolbox: {
                feature: {
                    dataView: { show: true, readOnly: false },
                    magicType: { show: true, type: ['line', 'bar'] },
                    restore: { show: true },
                    saveAsImage: { show: true }
                }
            },
            legend: {
                data: ['总销售额', '环比增长'],
                top: 30
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: [
                {
                    type: 'category',
                    data: data.xAxis.data,
                    axisPointer: {
                        type: 'shadow'
                    },
                    axisLabel: {
                        rotate: 45
                    }
                }
            ],
            yAxis: [
                {
                    type: 'value',
                    name: '销售额',
                    min: 0,
                    axisLabel: {
                        formatter: '{value} 元'
                    }
                },
                {
                    type: 'value',
                    name: '增长率',
                    axisLabel: {
                        formatter: '{value} %'
                    }
                }
            ],
            series: [
                {
                    name: '总销售额',
                    type: 'line',
                    smooth: true,
                    data: data.series[0].data,
                    markPoint: data.series[0].markPoint,
                    markLine: data.series[0].markLine,
                    areaStyle: {},
                    itemStyle: {
                        color: '#3498db'
                    }
                },
                {
                    name: '环比增长',
                    type: 'bar',
                    yAxisIndex: 1,
                    data: data.series[1].data,
                    itemStyle: {
                        color: function(params) {
                            // 根据正负值显示不同颜色
                            return params.value >= 0 ? '#2ecc71' : '#e74c3c';
                        }
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