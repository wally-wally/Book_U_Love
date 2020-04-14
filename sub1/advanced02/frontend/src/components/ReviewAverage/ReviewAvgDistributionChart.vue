<template>
  <div>
    <div class="chart-title">음식점들의 평균 평점 분포</div>
    <canvas ref="pieChart" id="pieChart"></canvas>
  </div>
</template>

<script>
import getData from '@/assets/json/data_03.json'

export default {
  name: 'RegionalRateChart',
  mounted() {
    let chartLabels = getData['chart_labels']
    let chartData = getData['score_distribution']
    new this.$_Chart(this.$refs.pieChart, {
      type: 'pie',
      data: {
        labels: chartLabels,
        datasets: [{
          label: '# of rate',
          data: chartData,
          backgroundColor: [
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
            'rgba(153, 102, 255, 1)'
          ],
          borderWidth: 1
        }]
      },
       options: {
        tooltips: {
          callbacks: {
            label: function(tooltipItem) {
              let totalReviewCount = getData['score_distribution'].reduce((total, x) => total += x, 0)
              let hoverData = getData['score_distribution'][tooltipItem.index]
              let rate = ((hoverData / totalReviewCount) * 100).toFixed(2)
              return `${rate}%`
            }
          }
        }
      }
    })
  }
}
</script>

<style scoped>
  .chart-title {
    font-size: 21px;
    font-family: 'Noto Serif KR';
    font-weight: 600;
    text-align: center;
    margin: 0.8rem 0;
  }
</style>