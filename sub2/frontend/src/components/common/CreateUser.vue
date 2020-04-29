<template>
    <div style="width:80%;margin:0 auto">
      <div v-for="u in users" :key="u">
        {{u.username}} | {{u.email}} | {{u.categorys}} | {{u.gender}} | {{u.age}} |{{ u.review_set.length }} 
      </div>
            <div class="category-title">관심 카테고리(하나만고르셈)</div>
            <v-select
              v-model="selectedCategories"
              class="pa-0"
              :items="this.categories.map(category => `${category.id}-${category.mainCatsName}-${category.subCatsName}-${category.name}`)"
              multiple
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
        }
    },
  computed: {
    ...mapState({
      categories: state => state.data.detailCategories
    }),
  },
  mounted () {
    this.allusers()
  },
    methods :  {
      allusers() {
        axios.get('http://localhost:8000/accounts/allusers/').then(result => {
          this.users = result.data.results
        })
      },
        createuser() {
            let convertCategoryIDs = this.selectedCategories.map(category => category.split('-')[0])
            const userData = {
                gender: this.gender,
                age: this.age,
                categorys: convertCategoryIDs
            }
            console.log(userData)
            axios.post('http://localhost:8000/accounts/createuser/',userData)
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