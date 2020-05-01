<template>
  <div style="width:50%;margin:0 auto">
      <div style="margin:0 auto"> 이번주 최다 리뷰</div>
      <div v-for="book in books" :key="book.id">
          <BookCard :bookData="book[0]"/> + {{book[1]}} 개
    </div>
  </div>
</template>

<script>
import { fetchweekly } from '@/api/index.js'
import BookCard from '@/components/Books/BookCard'

export default {
    components : {BookCard},
    data() {
        return {
            books :[]
        }
    },
    methods : {
        async getweekly(){
            const data = await fetchweekly()
            this.books = data.data
        }
    },
    mounted() {
        this.getweekly()
    }
}
</script>

<style>

</style>