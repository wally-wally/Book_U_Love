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
      <div class="loading-message">
        <span v-if="loadingStatus">데이터를 불러오는 중 입니다.</span>
        <span v-else>해당 데이터가 없습니다.</span>
      </div>
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
      recommendBooks : [],
      loadingStatus: false
    }
  },
  computed: {
    ...mapState({
      isLogin: state => state.user.isLogin,
      bookTheme: state => state.data.mainBookTheme
    })
  },
  created() {
    if (this.isLogin) {
      this.getRecommendBooks()
    }
    this.$store.commit('toggleMainBookTheme', 'All Books')
    this.getBooksList()
  },
  methods: {
    async getRecommendBooks() {
      this.recommendBooks = await this.$store.dispatch('GET_RECOMMEND_BOOKS')
    },
    async getBooksList() {
      this.loadingStatus = true
      let booksData = []
      if (this.bookTheme === 'All Books') {
        booksData = await this.$store.dispatch('GET_BOOKS', { 'page': this.pageNm })
        this.books = booksData.results
        this.pageCount = parseInt(booksData.count / 10) + (booksData.count % 10 === 0 ? 0 : 1)
      } else if (this.bookTheme === 'Recommend Books') {
        this.books = this.recommendBooks.slice(10 * (this.pageNm - 1), 10 * this.pageNm)
        this.pageCount = parseInt(this.recommendBooks.length / 10) + (this.recommendBooks.length % 10 === 0 ? 0 : 1)
      }
      this.loadingStatus = false
    },
    goToBookListTop() {
      let goToHeight = window.innerWidth > 800 ? 400 : window.innerWidth >= 550 ? 1110 : 1010
      window.scrollTo(0, goToHeight)
    }
  },
  watch: {
    pageNm() {
      this.getBooksList()
      this.goToBookListTop()
    },
    bookTheme() {
      this.pageNm = 1
      this.getBooksList()
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
    padding: 20px;
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
