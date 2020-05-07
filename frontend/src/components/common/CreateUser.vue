<template>
    <div style="width:80%;margin:0 auto">
            <div class="category-title">관심 카테고리(하나만고르셈)</div>
            <v-select
              v-model="selectedCategories"
              multiple
              class="pa-0"
              :items="this.subcategory"
              chips
            ></v-select>
            <div class="gender-title">성별</div>
            <v-radio-group v-model="gender" row id="gender" class="pa-0">
                <v-radio label="남성" value="M" color="primary"></v-radio>
                <v-radio label="여성" value="F" color="primary"></v-radio>
              </v-radio-group>
            <div class="add-info-age" style="height:100px;">
              <label for="age" class="d-block age-title">나이</label>
              <input style="height:30px" id="age" v-model="age" type="number" min="1">
            </div>

            <div style="width:200px;height:200px;background-color:rgb(163,132,175)" @click="createuser()"> 생성</div>
    </div>
</template>

<script>
import { mapState } from 'vuex'
import axios from 'axios'
export default {
    data() {
        return {
          users : [],
          gender: '',
          age: '',
          selectedCategories: [],
          subcategory : [], 
          subindex : {},
        }
    },
  computed: {
    ...mapState({
      categories: state => state.data.categories
    }),
  },
  created() {
    this.getCategory()
  },
  mounted () {
    this.allusers()
  },
    methods :  {
      async getCategory() {
      await this.$store.dispatch('GET_CATEGORIES')
      await this.setSubCategory()
    },
    setSubCategory() {
      for (const i in this.categories){
      const main = this.categories[i]
        for (const j in main.subcategory_set){
          const sub = main.subcategory_set[j]
          this.subcategory.push(sub.name)
          this.subindex[sub.name] = sub.id
        }
      }
    },
      allusers() {
        axios.get('http://i02b205.p.ssafy.io:8000/accounts/allusers/').then(result => {
          this.users = result.data.results
        })
      },
        createuser() {
            let convertCategoryIDs = []
              for (const i in this.selectedCategories){
                convertCategoryIDs.push(this.subindex[this.selectedCategories[i]])
              }
            const userData = {
                gender: this.gender,
                age: this.age,
                categorys: convertCategoryIDs
            }
            console.log(userData)
            axios.post('http://i02b205.p.ssafy.io:8000/accounts/createuser/',userData)
                .then((result) => {
                  console.log(result)
                })
                .catch(error => {
                  console.log(error)
              })

        }
    }
}
</script>

<style>

</style>