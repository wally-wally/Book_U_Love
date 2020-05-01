<template>
    <div>
        <div class="d-flex">
            <v-select
            v-model="age"
            :items="ages"
            menu-props="auto" 
            label="Select"
            class="mx-2"
            ></v-select>
            <v-select
            v-model="gender"
            :items="genders"
            menu-props="auto"
            class="mx-2"
            label="Select"
            ></v-select>
        </div>
        <canvas ref="barChart" id="barChart"></canvas>
        <v-data-table
                :headers="tableHeaders"
                :items="data"
                item-key="noticeIdx"
                hide-default-footer
                color="#E6CC00"
                class="elevation-1">
                </v-data-table>
        <!-- <div v-for="d in data" :key="d.book__detailCategory__name">
            <router-link v-if="d.book__detailCategory__name" :to="`/category/detail/${d.book__detailCategory}`">
                {{d.book__detailCategory__name}} - {{d.id__count}} 개의 리뷰
                
            </router-link>
        </div> -->
    </div>
</template>

<script>
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

        }
    },
    created() {
        this.fetchMyInfo()
        this.getcategoryfilter()
        // this.getData()
    },
    mounted() {
        this.updateChart()
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
          this.updateChart()
      }
    },
    methods : {
        async fetchMyInfo() {
            const myInfo = await this.$store.dispatch('GET_MYINFO')
            this.gender = myInfo.gender === 'M' ? '남자' : '여자'
            this.age = parseInt(myInfo.age / 10) * 10
        },
        async getcategoryfilter(params) {
            const data = await fetchcategoryfilter(params)
            this.data = data.data
        },
        // async getData() {
        //     const data = await fetchReviewFilter()
        //     console.log(data)
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
    });
        }, 1000)
        }
    }
}
</script>

<style scoped>

</style>