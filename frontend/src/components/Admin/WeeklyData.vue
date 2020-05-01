<template>
  <div class="page-wrapper">
        <h2>이번주 최다 리뷰</h2>
        <div class="books-list">
            <div v-for="book in books" :key="book.id">
                <div class="book-box">
                    <BookCard :bookData="book[0]"/>
                    <v-chip color="error" class="mb-3">+ {{book[1]}} 개</v-chip>
                </div>
            </div>
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
            books: []
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


<style scoped>
h2 {
  font-size: 20px;
  font-family: 'Noto Sans KR';
  margin: 10px 0;
}

.books-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(25%, auto));
}

@media (max-width: 1264px) {
  .books-list {
    grid-template-columns: repeat(auto-fill, minmax(33.33333%, auto));
  }
}
@media (max-width: 960px) {
  .books-list {
    grid-template-columns: repeat(auto-fill, minmax(50%, auto));
  }
}
@media (max-width: 600px) {
  .books-list {
    grid-template-columns: repeat(auto-fill, minmax(100%, auto));
  }
}

.book-box {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.book-box > div:last-child {
    text-align: center;
}

.variable-count {
    font-weight: 600;
    font-family: 'Gothic A1';
}
</style>