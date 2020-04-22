<template>
  <div class="dashboard-wrapper">
    <div>chart.js 를 이용하여 인사이트를 구성해봅시다</div>
    좋아하는 카테고리
    <br>
    {{mydata}}
    <hr>
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
    }
  },
  mounted() {
    this.bookdata()
    this.recommendbook()
  },
  methods : {
    async bookdata() {
      const data = await myBookdata()
      this.mydata = data.data
    },
    async recommendbook() {
      const data = await recommend()
      this.mybook = data.data
    }
  }
}
</script>

<style scoped>
.dashboard-wrapper {
  margin: 0 0.25em;
}
</style>