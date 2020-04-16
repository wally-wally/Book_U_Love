<template>
  <div class="my-1">
    <div class="row" v-if="books.length && !loadingStatus">
      <div v-for="book in books" :key="book.id" class="books-list col-lg-3 col-md-4 col-sm-6">
        <BookCard :bookData="book"/>
      </div>
      <v-pagination
        v-model="pageNm"
        :length="pageCount"
        :total-visible="9"
        circle
        color="grey"></v-pagination>
    </div>
    <div v-else>
      <div class="service-logo">
        <img src="../../assets/images/team_logo/books.png" alt="team-logo">
      </div>
      <div class="loading-message">데이터를 불러오는 중 입니다.</div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import BookCard from '@/components/Books/BookCard'

export default {
  name: 'BooksList',
  components: {
    BookCard
  },
  data() {
    return {
      pageNm: 1,
      pageCount: 0,
      books: [],
      loadingStatus: false
    }
  },
  created() {
    this.getBooksList()
  },
  methods: {
    async getBooksList() {
      this.loadingStatus = true
      const booksData = await this.$store.dispatch('GET_BOOKS', { 'page': this.pageNm })
      this.books = booksData.results
      this.pageCount = parseInt(booksData.count / 10) + 1
      this.loadingStatus = false
    },
    goToBookListTop() {
      let goToHeight = window.innerWidth > 800 ? 400 : 820
      window.scrollTo(0, goToHeight)
    }
  },
  watch: {
    pageNm() {
      this.getBooksList()
      this.goToBookListTop()
    }
  }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity .3s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}

@media (max-width: 600px) {
  .books-list {
    padding: 40px 20px;
  }
}

.service-logo {
  text-align: center;
}

.service-logo img {
  margin: 34px 0;
  width: 200px;
  height: 200px;
}

.loading-message {
  text-align: center;
  font-size: 18px;
  font-weight: 600;
  font-family: 'Noto Sans KR';
}
</style>
