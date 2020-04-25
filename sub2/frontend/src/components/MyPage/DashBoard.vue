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
    </div>

  </div>
</template>

<script>
import { myBookdata, recommend} from '@/api/index.js'
export default {
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
    }
  }
}
</script>

<style scoped>
.dashboard-wrapper {
  margin: 0 0.25em;
  width: 80%
}
</style>