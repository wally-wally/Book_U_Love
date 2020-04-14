<template>
  <div>
    <div class="chart-title">
      리뷰 평균 평점 상위 BEST 6
      <v-btn class="all-data-btn px-2" @click="showAllData()"><span class="all-data-btn-text"></span></v-btn>
    </div>
    <div>
      <v-alert
        dense
        text
        color="#607D8B"
        :style="{ fontFamily: 'Noto Sans KR' }">
        <i class="fas fa-check alert-all-data"></i><span class="pl-2 alert-all-data">전체 데이터 보기(All Data)를 선택하면 리뷰 개수가 20개 이상 작성된 음식점 중 평점이 3.5점 이상인 음식점들의 데이터(평점 순으로 나열)를 모두 볼 수 있습니다.</span>
      </v-alert>
    </div>
    <canvas ref="barChart" id="barChart"></canvas>
    <div class="remain-data-section">
      <transition name="fade" mode="out-in" v-if="showAll">
        <RemainStoresData :data="filterData"></RemainStoresData>
      </transition>
    </div>
  </div>
</template>

<script>
import RemainStoresData from '@/components/ReviewCount/RemainStoresData'
import getData from '@/assets/json/data_01.json'

export default {
  name: 'ReviewCountChart',
  components: {
    RemainStoresData
  },
  data() {
    return {
      data: getData,
      showAll: false,
      filterData: getData.filter(data => data['review_mean'] >= 3.5)
    }
  },
  mounted() {
    let chartLabels = []
    let chartData = []
    this.data.slice(0, 6).forEach(data => {
      chartLabels.push(data['store_name'])
      chartData.push(data['review_mean'].toFixed(2))  
    })

    new this.$_Chart(this.$refs.barChart, {
      type: 'bar',
      data: {
        labels: chartLabels,
        datasets: [{
            label: '# of mean review',
            data: chartData,
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
      },
      options: {
        scales: {
          xAxes: [{
            scaleLabel: {
              display: true,
              labelString: '음식점 이름',
              fontColor: "black"
            }
          }],
          yAxes: [{
            ticks: {
              min: 4,
              max: 5
            },
            scaleLabel: {
              display: true,
              labelString: '평균 평점',
              fontColor: "green"
            }
          }]
        }
      }
    });
  },
  methods: {
    showAllData() {
      this.showAll = true
    }
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
    position: relative;
  }

  .remain-data-section {
    margin: 1rem 0;
  }

  .all-data-btn {
    position: absolute;
    right: 0;
  }

  .fade-enter-active, .fade-leave-active {
    transition: opacity .2s;
  }
  
  .fade-enter, .fade-leave-to {
    opacity: 0;
  }

  @media(min-width: 600px) {
    .all-data-btn-text::after {
      content: '전체 데이터 보기';
    }
  }

  @media(max-width: 600px) {
    .all-data-btn-text::after {
      content: 'All Data';
      text-transform: capitalize;
    }

    .alert-all-data {
      font-size: 13px;
    }
  }
</style>