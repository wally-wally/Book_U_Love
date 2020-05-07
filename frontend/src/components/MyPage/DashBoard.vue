<template>
  <div class="dashboard-wrapper">
    <div class="dashboard">📊 Dashboard</div>
    <div class="dashboard-sub">1️⃣ {{$store.getters.info.username}} 님의 선호 카테고리 분석 결과</div>
    <div class="dashboard-section" v-if="mydata.length">
      <div class="category-select">
        <div>
          <div class="cats-title">대분류</div>
          <div v-for="(m,idx) in mydata" :key="m.id"  @click="shownext(1,idx)" class="cats-item-wrapper">
            <span class="cats-name">{{m.name}}</span>
          </div>
        </div>
        <div>
          <div class="cats-title">중분류</div>
          <div v-for="(s,idx) in sub" :key="s.id" @click="shownext(2,idx)" class="cats-item-wrapper">
            <span v-if="s.count" class="cats-name">{{s.name}}</span>
          </div>
        </div>
        <div>
          <div class="cats-title">소분류</div>
          <div v-for="(d,idx) in detail" :key="idx" class="cats-item-wrapper">
            <span v-if="d.count" class="cats-name">{{d.name}}</span>
          </div>
        </div>
      </div>  
      <div class="chart-section">
        <div>
          <DashChart :chartData="this.main_chart.data" :chartLabels="this.main_chart.labels" chartType="pie"/>
        </div>
        <div>
          <DashChart :chartData="this.sub_chart.data" :chartLabels="this.sub_chart.labels" chartType="pie"/>
        </div>
        <div>
          <DashChart :chartData="this.detail_chart.data" :chartLabels="this.detail_chart.labels" chartType="pie"/>
        </div>
      </div>
    </div>
    <div class="dashboard-section" v-else>
      <i class="fas fa-times d-block text-center"></i>
      <p class="no-category-alert">작성한 리뷰 데이터가 없습니다.</p>
    </div>
      
    
    <hr class="mt-5">
    <div class="dashboard-sub pt-5">2️⃣ {{ this.info.username }}님을 위한 추천 도서</div>
    <div v-if="'message' in mybook">
      <div class="no-books-text">
        <i class="fas fa-book"></i>
        <p>{{ this.info.username }}님을 위한 맞춤 추천 도서가 없습니다.</p>
        <p>관심 카테고리를 설정하고 리뷰를 더 많이 작성해주시면</p>
        <p>맞춤 도서를 추천해드릴께요!</p>
      </div>
      <div class="alert-title">대신 이런 책은 어떠세요? (리뷰 평점 TOP 10)</div>
      <div class="review-top-books">
        <div v-for="(book, idx) in reviewTopBooks" :key="idx">
          <BookCard :bookData="book"/>
        </div>
      </div>
    </div>
    <div v-else class="books-list">
      <div v-for="book in mybook" :key="book.id">
        <BookCard class="col-10" :bookData="book"/>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { myBookdata, recommend } from '@/api/index.js'
import BookCard from '@/components/Books/BookCard'
import DashChart from '@/components/common/DashChart'

export default {
  components: {BookCard, DashChart},
  data() {
    return {
      mydata : [],
      mybook : [],
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
      },
      reviewTopBooks: []
    }
  },
  computed: {
    ...mapGetters(['info'])
  },
  created() {
    this.bookdata()
    this.recommendbook()
  },
  methods : {
    async bookdata() {
      const data = await myBookdata()
      this.mydata = data.data.results
      if (data.data.results.length) {
        for (const m in this.mydata) {
          this.main_chart.labels.push(this.mydata[m].name)
          this.main_chart.data.push(this.mydata[m].count)
        }
      }
    },
    async getReviewTopBooks() {
      let data = await this.$store.dispatch('GET_BOOKS', {sortby: "score",top:10})
      this.reviewTopBooks = data['results']
    },
    async recommendbook() {
      const data = await recommend()
      this.mybook = data.data
      if (this.mybook.length === undefined) {
        this.getReviewTopBooks()
      }
    },
    shownext(idx,val){ 
      if (idx == 0) {
        this.sub = []
      } else if (idx == 1){
        this.sub = this.mydata[val].subcategory_set
        this.detail = []
        this.sub_chart.labels =[]
        this.sub_chart.data = []
        for (const s in this.sub) {
          if(this.sub[s].count){
            this.sub_chart.labels.push(this.sub[s].name)
            this.sub_chart.data.push(this.sub[s].count)
          }
        }
      } else if (idx == 2){
        this.detail = this.sub[val].detailcategory_set
        this.detail_chart.labels = []
        this.detail_chart.data =[]
        for (const d in this.detail){
          if(this.detail[d].count){
          this.detail_chart.labels.push(this.detail[d].name)
          this.detail_chart.data.push(this.detail[d].count)
          }
        }
      }
    },
    // makechart(){
    //   let chartLabels = []
    //   let chartData = []
    //   for (const i in this.mydata.category){
    //     console.log(this.mydata.category[i].book__category__name)
    //     chartLabels.push(this.mydata.category[i].book__category__name)
    //     chartData.push(this.mydata.category[i].score__count)
    //   }
    //   new this.$_Chart(this.$refs.pieChart, {
    //     type: 'doughnut',
    //     data: {
    //       labels: chartLabels,
    //       datasets: [{
    //         label: '# of rate',
    //         data: chartData,
    //         backgroundColor: [
    //           'rgba(255, 99, 132, 0.2)',
    //           'rgba(54, 162, 235, 0.2)',
    //           'rgba(255, 206, 86, 0.2)',
    //           'rgba(75, 192, 192, 0.2)',
    //           'rgba(153, 102, 255, 0.2)'
    //         ],
    //         borderColor: [
    //           'rgba(255, 99, 132, 1)',
    //           'rgba(54, 162, 235, 1)',
    //           'rgba(255, 206, 86, 1)',
    //           'rgba(75, 192, 192, 1)',
    //           'rgba(153, 102, 255, 1)'
    //         ],
    //         borderWidth: 1
    //       }]
    //     },
    //     options:{
    //       responsive:true,
    //       aspectRatio: 1,
    //       legend:{
    //         align: 'start',
    //         position: 'top'
    //       }
    //     }
    //   })
    // }
  },
  // watch:{
  //   mydata() {
  //     if (this.mydata.length > 0) {
  //       this.makechart()
  //     }
  //   }
  // }
}
</script>

<style scoped>
.dashboard-wrapper {
  margin: 0 auto;
  width: 85%;
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
  font-size: 1.2em;
  padding-bottom: 0.8em;
}

.dashboard-section i {
  font-size: 100px;
}

.dashboard-section .no-category-alert {
  font-family: 'Noto Sans KR';
  font-weight: 600;
  text-align: center;
}

.no-books-text {
  font-family: 'Noto Sans KR';
  font-weight: 600;
  text-align: center;
  padding-bottom: 20px;
  margin-bottom: 20px;
  border-bottom: 5px dashed silver;
}

.no-books-text i {
  font-size: 100px;
  margin-bottom: 10px;
}

.no-books-text p {
  margin-bottom: 2px;
}

.alert-title {
  font-family: 'Gothic A1';
  font-size: 17px;
  font-weight: 600;
  margin-bottom: 10px;
}

.category-select,
.chart-section {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(33.33333%, auto));
}

.books-list,
.review-top-books {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(25%, auto));
}

@media (max-width: 1670px) {
  .books-list,
  .review-top-books {
    grid-template-columns: repeat(auto-fill, minmax(33.33333%, auto));
  }
}
@media (max-width: 1300px) {
  .books-list,
  .review-top-books {
    grid-template-columns: repeat(auto-fill, minmax(50%, auto));
  }
}
@media (max-width: 640px) {
  .books-list,
  .review-top-books {
    grid-template-columns: repeat(auto-fill, minmax(100%, auto));
  }
}

@media (max-width: 900px) {
  .dashboard-wrapper {
    width: 100%;
  }
}

.cats-item-wrapper {
  margin: 8px 0;
  text-align: center;
}

.cats-title {
  font-family: 'Noto Sans KR';
  font-weight: 600;
  font-size: 17px;
  text-shadow: 3px 3px 5px rgba(0, 0, 0, 0.1);
  text-align: center;
  background-color: rgb(252, 243, 230);
  padding: 5px 0;
  width: 90%;
  margin: 0 auto;
}

.cats-name {
  font-family: 'Noto Sans KR';
  font-size: 17px;
  width: 90%;
  margin: 0 auto;
}

.cats-name:hover {
  cursor: pointer;
  font-weight: 600;
}
</style>