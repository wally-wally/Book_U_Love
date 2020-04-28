<template>
    <canvas ref="Chart" id="Chart"></canvas>
</template>

<script>
export default {
  name : "chart",
  props : {
    chartLabels : {type:Array},
    chartData : {type:Array},
    chartType : {type:String}
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
      makechart(){
        new this.$_Chart(this.$refs.Chart, {
        type: this.chartType,
        data: {
          labels: this.chartLabels,
          datasets: [{
            label: '리뷰 개수',
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
          aspectRatio: 4,
          legend:{
            // align: 'start',
            // position: 'bottom'
            display: false
          },
          scales: {
            xAxes: [{
              gridLines: {
                display: false
              }
             }],
            yAxes: [{
                gridLines: {
                    display: false
                },
                ticks: {
                   display: false
               }
            }]
          },
          plugins: {
            datalabels: {
                formatter: () => {
                  return null;
                }
            }
          }
        },
    })
    }
  }
}
</script>

<style>

</style>