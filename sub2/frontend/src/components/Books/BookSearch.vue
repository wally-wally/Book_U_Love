<template>
  <div class="book-search-wrapper">
    <div class="book-search-name ml-2 my-2 pl-3">
      '{{ this.$route.params.query }}' (으)로 검색한 결과입니다.
    </div>
    <div class="row" v-if="books.length">
      <div v-for="book in books" :key="book.id" class="books-list col-lg-3 col-md-4 col-sm-6">
        <BookCard :bookData="book"/>
      </div>
    </div>
    <div v-else class="no-search-books">
      <i class="fas fa-times d-block text-center"></i>
      <p>검색한 키워드를 포함하는 도서가 없습니다.</p>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import BookCard from '@/components/Books/BookCard'

export default {
  name: 'BookSearch',
  components: {
    BookCard
  },
  data() {
    return {
      books: []
    }
  },
  created() {
    this.onBookDetail()
  },
  methods: {
    async getBookDetail(query) {
      this.books = await this.$store.dispatch('GET_BOOK_DETAIL', {query: query})
    },
    onBookDetail() {
      this.getBookDetail(this.$route.params.query)
    }
  },
  watch: {
    '$route': 'onBookDetail'
  }
}
</script>

<style scoped>
.book-search-wrapper {
  width: 90%;
  margin: 0 auto;
}

.book-search-wrapper .book-search-name {
  font-family: 'Noto Sans KR';
  font-weight: 600;
  font-size: 1.1em;
}

.no-search-books {
  font-family: 'Gothic A1';
  color: crimson;
}

.no-search-books i {
  font-size: 7em;
  margin: 0.2em 0;
}

.no-search-books > p {
  font-weight: 600;
  font-size: 1.1em;
  text-align: center;
}
</style>