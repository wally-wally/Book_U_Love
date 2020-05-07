<template>
    <div>
      <div class="page-description">
        🔖 연령대와 성별에 따른 동년배들의 카테고리(소분류)별 리뷰 개수 분포를 확인할 수 있습니다.
      </div>
        <div class="select-box">
          <v-select
          v-model="age"
          :items="ages"
          menu-props="auto" 
          label="연령대"
          class="mx-2"
          color="warning"
          ></v-select>
          <v-select
          v-model="gender"
          :items="genders"
          menu-props="auto"
          class="mx-2"
          label="성별"
          color="warning"
          ></v-select>
        </div>
        <div class="canvas-section">
          <canvas ref="barChart" id="barChart" width="400" height="200"></canvas>
        </div>
        <v-data-table
          :headers="tableHeaders"
          :items="data"
          item-key="noticeIdx"
          color="#E6CC00"
          @click:row="goCategoryPage($event)"
          class="elevation-1 my-12">
        </v-data-table>
    </div>
</template>

<script>
import { mapState } from 'vuex'
import { fetchcategoryfilter, fetchReviewFilter } from '@/api/index.js'

export default {
  data() {
    return  {
      data : [],
      age : '전체',
      gender : '전체',
      ages : ['전체',10,20,30,40,50,60,70] ,
      genders : ['전체','남자','여자'],
      tableHeaders: [
        { text: '카테고리', value: 'book__detailCategory__name' },
        { text: '리뷰개수', value: 'id__count' },
      ],
      // chartID: -1
    }
  },
  created() {
    // this.resetChart()
    this.fetchMyInfo()
    this.getcategoryfilter()
    this.updateChart()
    // this.getData()
  },
  computed: {
    ...mapState({
      isLogin: state => state.user.isLogin
    })
  },
  watch : {
    age() {
      const params = {}
      if (this.gender != "전체") {
        params.gender = this.gender
      }
      if (this.age != "전체") {
        params.age = this.age
      }
      this.getcategoryfilter(params)
      // this.resetChart()
      this.updateChart()
    },
    gender(){ 
      const params = {}
      if (this.gender != "전체") {
        params.gender = this.gender
      }
      if (this.age != "전체") {
        params.age = this.age
      }
      this.getcategoryfilter(params)
      // this.resetChart()
      this.updateChart()
    }
  },
  methods : {
    // resetChart() {
    //   const canvasTag = document.querySelector('canvas')
    //   this.chartID += 1
    //   canvasTag.id = `barChart${this.chartID}`
    // },
    async fetchMyInfo() {
      if (this.isLogin) {
        const myInfo = await this.$store.dispatch('GET_MYINFO')
        this.gender = myInfo.gender === 'M' ? '남자' : '여자'
        this.age = parseInt(myInfo.age / 10) * 10
      }
    },
    async getcategoryfilter(params) {
      const { data } = await fetchcategoryfilter(params)
      this.data = data
    },
    goCategoryPage(data) {
      this.$router.push(`/category/detail/${data.book__detailCategory}/`)
    },
    // async getData() {
    //   const data = await fetchReviewFilter()
    //   console.log(data)
    // },
    updateChart() {
      setTimeout(() => {
        let chartLabels = []
        let chartData = []
        this.data.slice(0, 6).forEach(obj => {
          chartLabels.push(obj.book__detailCategory__name)
          chartData.push(obj.id__count)
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
                  labelString: '카테고리',
                  fontColor: "black"
                }
              }],
              yAxes: [{
                scaleLabel: {
                  display: true,
                  labelString: '리뷰 개수',
                  fontColor: "black"
                }
              }]
            }
          }
        })
      }, 1000)
    }
  }
}
</script>

<style scoped>
.page-description {
  font-size: 17px;
  font-family: 'Nanum Gothic';
  font-weight: 600;
  margin: 30px 0;
}

.select-box {
  display: flex;
}

@media (max-width: 900px) {
  .page-description {
    font-size: 15px;
    margin-top: 10px;
  }

  .select-box {
    display: block;
  }
}
</style>