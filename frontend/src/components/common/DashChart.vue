<template>
<div>
    <canvas ref="Chart" id="Chart"></canvas>
</div>
</template>

<script>
import ChartJSPluginDatalabels from "chartjs-plugin-datalabels";

export default {
  name : "chart",
  props : {
    chartLabels : {type:Array},
    chartData : {type:Array},
    chartType : {type:String}
  },
  data() {
    return {
      total : 0
    }
  },
  watch :  {
    chartData : function() {
        this.makechart()
    }  
  },
  mounted() {
    this.makechart()
  },
  methods : {
    sum(){
      this.total = 0
      for (const i in this.chartData) {
        this.total += this.chartData[i];
      }
    },
      async makechart(){
        await this.sum()
        const ctx = this.$refs.Chart.getContext('2d')
        new this.$_Chart(ctx, {
        type: this.chartType,
        data: {
          labels: this.chartLabels,
          datasets: [{
            // label: '리뷰 개수',
            data: this.chartData,
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)'
            ],
            borderColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)'
            ],
            // borderWidth: 1
          }]
        },
        options:{
          aspectRatio: 1,
          legend:{
            // align: 'start',
            // position: 'bottom'
            display: false
          },
          // tooltips: {
          //   enabled: false
          // },
          // scales: {
          //   xAxes: [{
          //     gridLines: {
          //       display: false
          //     }
          //    }],
          //   yAxes: [{
          //       gridLines: {
          //           display: false
          //       },
          //       ticks: {
          //          display: false
          //      }
          //   }]
          // }
          plugins: {
            datalabels: {
                color: '#111',
                textAlign: 'center',
                font: {
                    lineHeight: 1.6
                },
                formatter: (value,ctx) => {
                  if ((value/this.total)>=0.11) {
                  return ctx.chart.data.labels[ctx.dataIndex]+ "\n" + Math.floor((value/this.total)*100) +'%';
                  }
                  else {
                    return null
                  }
                }
            }
        }
        }
    })
    }
  }
}
</script>

<style>

</style>