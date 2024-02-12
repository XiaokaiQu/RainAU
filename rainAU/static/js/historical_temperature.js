var dom = document.getElementById('container_ht');
var myChart = echarts.init(dom, null, {
  renderer: 'canvas',
  useDirtyRect: false
});

var app = {};

var option;

option = {
  tooltip: {
    trigger: 'axis'
  },
  legend: {},
  toolbox: {
    show: true,
    feature: {
      dataZoom: {
        yAxisIndex: 'none'
      },
      dataView: { readOnly: false },
      magicType: { type: ['line', 'bar'] },
      restore: {},
      saveAsImage: {}
    }
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: temp_data_ht.date_list
  },
  yAxis: {
    type: 'value',
    axisLabel: {
      formatter: '{value} °C'
    }
  },
    series: [
    {
      name: 'Highest',
      type: 'line',
      data: temp_data_ht.second_list,
      markPoint: {
        data: [
          { type: 'max', name: 'Max' },
          { type: 'min', name: 'Min' }
        ]
      },
      markLine: {
        data: [
          { type: 'average', name: 'Avg' },
          [
            {
              symbol: 'none',
              x: '90%',
              yAxis: 'max'
            },
            {
              symbol: 'circle',
              label: {
                position: 'start',
                formatter: 'Max'
              },
              type: 'max',
              name: 'Max'
            }
          ]
        ]
      }
    },
    {
      name: 'Lowest',
      type: 'line',
      data: temp_data_ht.first_list,
      markPoint: {
        data: [
          { type: 'max', name: 'Max' },
          { type: 'min', name: 'Min' }
        ]
      },
      markLine: {
        data: [
          { type: 'average', name: 'Avg' },
          [
            {
              symbol: 'none',
              x: '90%',
              yAxis: 'min'
            },
            {
              symbol: 'circle',
              label: {
                position: 'start',
                formatter: 'Min'
              },
              type: 'min',
              name: 'Min'
            }
          ]
        ]
      }
    }
  ]
};

if (option && typeof option === 'object') {
  myChart.setOption(option);
}

window.addEventListener('resize', myChart.resize);