<template>
    <div>
        <div class="row">
            <div class="col-4">
                <div v-for="(m,idx) in mydata" :key="m.id"  @click="shownext(1,idx)">
                    {{m.name}}
                </div>
            </div>
            <div class="col-4">
                <div v-for="(s,idx) in sub" :key="s.id" @click="shownext(2,idx)">
                    {{s.name}}
                </div>
            </div>
            <div class="col-4">
                <div v-for="(d,idx) in detail" :key="d.id">
                    {{d.name}}
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-4">
                <DashChart :chartData="this.main_chart.data" :chartLabels="this.main_chart.labels" chartType="pie"/>
            </div>
            <div class="col-4">
                <DashChart :chartData="this.sub_chart.data" :chartLabels="this.sub_chart.labels" chartType="pie"/>

            </div>
            <div class="col-4">
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
  mounted() {
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

<style>

</style>