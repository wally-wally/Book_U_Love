<template>
<div>
            <div class="row">
                <v-select
                class="col-2"
                v-model="age"
                :items="ages"
                menu-props="auto" 
                label="Select"
                ></v-select>
                <v-select
                class="col-2"
                v-model="gender"
                :items="genders"
                menu-props="auto" 
                label="Select"
                ></v-select>
            </div>
    <div v-for="d in data" :key="d.book__detailCategory__name">
        <router-link v-if="d.book__detailCategory__name" :to="`/category/detail/${d.book__detailCategory}`">
            {{d.book__detailCategory__name}} - {{d.id__count}} 개의 리뷰
        </router-link>
    </div>
</div>
</template>

<script>
import { fetchcategoryfilter } from '@/api/index.js'

export default {
    data() {
        return  {
            data : [],
            age : '전체',
          gender : '전체',
          ages : ['전체',10,20,30,40,50,60,70] ,
          genders : ['전체','남자','여자'],
        }
    },
    mounted() {
        this.getcategoryfilter()
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
      }
    },
    methods : {
        async getcategoryfilter(params) {
            const data = await fetchcategoryfilter(params)
            this.data = data.data
        }
    }
}
</script>

<style>

</style>