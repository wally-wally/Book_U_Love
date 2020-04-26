<template>
  <div class="dashboard-wrapper">
    <div>chart.js 를 이용하여 인사이트를 구성해봅시다</div>
    카테고리 선택
    <div class="row">
      <div class="col-3" @click="shownext(0,0)">
        전체
      </div>
      <div class="col-3">
        <div v-for="(m,idx) in mydata" :key="m.id"  @click="shownext(1,idx)">
          {{m.name}}
        </div>
      </div>
      <div class="col-3">
        <div v-for="(s,idx) in sub" :key="s.id" @click="shownext(2,idx)">
          {{s.name}}
        </div>
      </div>
      <div class="col-3">
        <div v-for="(d,idx) in detail" :key="d.id">
          {{d.name}}
        </div>
      </div>
    </div>
    
    <hr>
    <hr>
    <div class="row">
      <div class="col-3">
        {{this.main_chart}}
      </div>
      <div class="col-3">
        {{this.sub_chart}}
      </div>
      <div class="col-3">
        {{this.detail_chart}}
      </div>
      <div class="col-3">

      </div>
    </div>

    <div v-for="book in mybook" :key="book.id">
      <router-link :to="`/book/${book.id}`">
      {{book.title}}
      </router-link>
      
      
    <div class="dashboard">Dashboard</div>
    <div class="dashboard-sub">{{$store.getters.info.username}} 님의 선호 카테고리 분석 결과</div>
    <div class="chart-container" style="padding:30px 0;display:inline">
     <canvas ref="pieChart" id="pieChart"></canvas>
    </div>
    <!-- <div><b>{{}}</b> 선호형</div> -->
    <hr>
    <div class="dashboard-sub pt-5">For You</div>
    <div class="row">
      <div v-for="book in mybook" :key="book.id">
        <BookCard class="col-10" :bookData="book"/>
      </div>
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
      main : [],
      sub : [],
      detail : [],
      main_chart: {
        labels : [],
        data : [],
      },
      sub_chart : {
        labels :[],
        data : [],
      },
      detail_chart:{
        labels:[],
        data : [],
      }
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
      this.mydata = data.data.results
      for (const m in this.mydata) {
        this.main_chart.labels.push(this.mydata[m].name)
        this.main_chart.data.push(this.mydata[m].count)
      }
    },
    async recommendbook() {
      const data = await recommend()
      this.mybook = data.data
    },
    shownext(idx,val){ 
      if (idx == 0) {
        this.sub = []
      }
      else if (idx == 1){
        this.sub = this.mydata[val].subcategory_set
        this.detail = []
        this.sub_chart.labels =[]
        this.sub_chart.data = []
        for (const s in this.sub) {
          this.sub_chart.labels.push(this.sub[s].name)
          this.sub_chart.data.push(this.sub[s].count)
        }
      } else if (idx == 2){
        this.detail = this.sub[val].detailcategory_set
        this.detail_chart.labels = []
        this.detail_chart.data =[]
        for (const d in this.detail){
          this.detail_chart.labels.push(this.detail[d].name)
          this.detail_chart.data.push(this.detail[d].count)
        }
      }
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
          responsive:false,
          aspectRatio: 1,
          legend:{
            align: 'start',
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