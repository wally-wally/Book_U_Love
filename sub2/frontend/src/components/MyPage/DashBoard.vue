<template>
  <div class="dashboard-wrapper">
    <div class="dashboard">Dashboard</div>
    <div class="dashboard-sub">{{this.$store.getters.info.username}} 님의 선호 카테고리 분석 결과</div>
    <div class="chart-container" style="padding:30px 0;">
     <canvas ref="pieChart" id="pieChart"></canvas>
    </div>
    <hr>
    <div class="dashboard-sub pt-5">For You</div>
    <div class="row">
      <div v-for="book in mybook" :key="book.id">
        <BookCard class="col-10" :bookData="book"/>
      </div>
    </div>

  </div>
</template>

<script>
import { myBookdata, recommend} from '@/api/index.js'
import BookCard from '@/components/Books/BookCard'

export default {
  components: {BookCard},
  data() {
    return {
      mydata : {},
      mybook : {},
    }
  },
  mounted() {
    this.bookdata()
    this.recommendbook()
  },
  watch:{
    mydata(){
      this.makechart()
    }
  },
  methods : {
    async bookdata() {
      const data = await myBookdata()
      this.mydata = data.data
    },
    async recommendbook() {
      const data = await recommend()
      this.mybook = data.data
    },
    makechart(){
      let chartLabels = []
      let chartData = []
      for ( const i in this.mydata.category){
        console.log(this.mydata.category[i].book__category__name)
        chartLabels.push(this.mydata.category[i].book__category__name)
        chartData.push(this.mydata.category[i].score__count)
      }
      new this.$_Chart(this.$refs.pieChart, {
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
        options:{
          aspectRatio: 4,
          legend:{
            align: 'center',
            position: 'top'
          }
        }
    })
    }
  }
}
</script>

<style scoped>
.dashboard-wrapper {
  margin: 0 auto;
  width: 70%;
}
.dashboard{
  font-size: 1.5em;
  font-weight: bold;
  font-family: 'Noto Sans KR';
  margin-bottom: 1em;
}
.dashboard-sub{
  font-family: 'Nanum Gothic';
  font-weight: 600;
  font-size: 1.1em;
  padding-bottom: 0.8em;
}
</style>