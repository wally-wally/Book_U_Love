<template>
  <div>
    <div class="chart-title">지역별 평균 평점 3.5점 이상인 음식점 비율 분포 그래프</div>
    <canvas ref="doughnutChart" id="doughnutChart"></canvas>
  </div>
</template>

<script>
import getData from '@/assets/json/data_02.json'

export default {
  name: 'RegionalRateChart',
  data() {
    return {
      data: getData
    }
  },
  mounted() {
    let chartLabels = []
    let chartData = []
    let originData = this.data
    for (let region in this.data) {
      let rate = (this.data[region]['filtering_stores_count'] / this.data[region]['total_stores_count']) * 100
      chartLabels.push(`${region}-${rate.toFixed(2)}[%]`)
      chartData.push(rate.toFixed(2))
    }
    new this.$_Chart(this.$refs.doughnutChart, {
      type: 'doughnut',
      data: {
        labels: chartLabels,
        datasets: [{
          label: '# of rate',
          data: chartData,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)'
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)'
          ],
          borderWidth: 1
        }]
      },
      options: {
        tooltips: {
          callbacks: {
            label: function(tooltipItem) {
              let region = chartLabels[tooltipItem.index].split('-')[0]
              let totalCount = originData[region]['total_stores_count']
              let filterCount = originData[region]['filtering_stores_count']
              return `필터링된 음식점 수 : ${filterCount}개 / 전체 음식점 수 : ${totalCount}개`
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