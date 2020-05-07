<template>
    <div class="page-wrapper">
      <div class="page-description">
        🔖 각 카테고리별 리뷰 분포를 확인할 수 있습니다.
      </div>
        <div class="chart-wrapper">
            <div>
                <div class="cats-title">대분류</div>
                <div v-for="(m,idx) in mydata" :key="m.id"  @click="shownext(1,idx)" class="cats-item-wrapper">
                    <span class="cats-name">{{m.name}}</span>
                </div>
            </div>
            <div>
                <div class="cats-title">중분류</div>
                <div v-for="(s,idx) in sub" :key="s.id" @click="shownext(2,idx)" class="cats-item-wrapper">
                    <span class="cats-name">{{s.name}}</span>
                </div>
            </div>
            <div>
                <div class="cats-title">소분류</div>
                <div v-for="(d,idx) in detail" :key="idx" class="cats-item-wrapper">
                    <span class="cats-name">{{d.name}}</span>
                </div>
            </div>
        </div>
        <div class="chart-wrapper">
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
</template>

<script>
import { fetchreviewcategory } from '@/api/index.js'
import DashChart from '@/components/common/DashChart'
export default {
    components : {DashChart},
  data() {
      return {
      mydata : {},
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
      }
      }
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
        this.getreviewcategory(params)
      },
      gender(){ 
          const params = {}
          if (this.gender != "전체") {
              params.gender = this.gender
          }
          if (this.age != "전체") {
              params.age = this.age
          }
        this.getreviewcategory(params)
      }
  },
  created() {
    this.$store.commit('togglePostReviewLoading', true)
    this.getreviewcategory()
  },
  methods : {
      async getreviewcategory(params) {
        this.main_chart = {
            labels : [],
            data : [],
        }
        const data = await fetchreviewcategory(params)
        this.mydata = data.data.results
        for (const m in this.mydata) {
          this.main_chart.labels.push(this.mydata[m].name)
          this.main_chart.data.push(this.mydata[m].count)
        }
        this.$store.commit('togglePostReviewLoading', false)
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

@media (max-width: 900px) {
  .page-description {
    font-size: 15px;
    margin-top: 10px;
  }
}

.page-wrapper {
  margin: 10px 0;
}

.cats-item-wrapper {
  margin: 8px 0;
  text-align: center;
}

.cats-title {
  font-family: 'Noto Sans KR';
  font-weight: 600;
  font-size: 18px;
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

.chart-wrapper {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(33.333333%, auto));
}

@media (max-width: 700px) {
  .cats-title {
    font-size: 16px;
  }

  .cats-name {
    font-size: 14px;
  }
}
</style>