document.addEventListener('DOMContentLoaded', function() {
    const menuItems = document.querySelectorAll('.menu-item');
    const chartTitles = {
        'chart1': { title: '商品销量排行', desc: '展示销量最高的前10个商品' },
        'chart2': { title: '商品价格分布', desc: '箱线图展示价格分布情况' },
        'chart3': { title: '店铺销量/销售额排行', desc: '展示销量和销售额最高的店铺' },
        'chart4': { title: '地域分布', desc: '各地区店铺销量分布情况' },
        'chart5': { title: '包邮 vs 非包邮的销量比较', desc: '包邮与非包邮商品的销量比例' },
        'chart6': { title: '总销售额分析', desc: '各价格区间的销售额分布' },
        'chart7': { title: '标题关键词分析', desc: '商品标题中出现频率最高的关键词' }
    };
    
    // 初始化ECharts实例
    const chartDom = document.getElementById('mainChart');
    const myChart = echarts.init(chartDom);
    
    // 检查是否支持词云图
    function hasWordCloudSupport() {
        return typeof 'echarts.wordCloud' !== 'undefined' || 
               typeof echarts.graphic.registerShape === 'function';
    }
    
    // 加载图表函数
    function loadChart(chartId) {
        // 更新标题和描述
        document.getElementById('currentChartTitle').textContent = chartTitles[chartId].title;
        document.getElementById('currentChartDesc').textContent = chartTitles[chartId].desc;
        
        // 更新菜单项状态
        menuItems.forEach(item => {
            item.classList.remove('active');
            if(item.dataset.chart === chartId) {
                item.classList.add('active');
            }
        });
        
        // 显示加载中
        myChart.showLoading({
            text: '数据加载中...',
            color: '#3498db',
            textColor: '#2c3e50',
            maskColor: 'rgba(255, 255, 255, 0.8)'
        });
        
        // 根据不同图表类型加载数据
        fetch(`/data/${chartId}`)
            .then(response => response.json())
            .then(data => {
                myChart.hideLoading();
                renderChart(chartId, data, myChart);
            })
            .catch(error => {
                console.error('Error loading chart data:', error);
                myChart.hideLoading();
                myChart.setOption({
                    title: {
                        text: '数据加载失败',
                        left: 'center',
                        top: 'center',
                        textStyle: {
                            color: '#e74c3c'
                        }
                    }
                });
            });
    }
    
    // 注册事件监听
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            const chartId = this.dataset.chart;
            loadChart(chartId);
        });
    });
    
    // 窗口大小改变时重置图表大小
    window.addEventListener('resize', function() {
        myChart.resize();
    });
    
    // 加载默认图表
    loadChart('chart1');
});