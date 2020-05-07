<template>
  <div class="book-search-wrapper">
    <div class="book-search-name my-2" v-if="!loadingStatus">
      <div class="search-message">'{{ this.$route.params.query }}' (으)로 검색한 결과입니다.</div>
      <div class="book-count-message" v-if="totalBookCount">총 {{ totalBookCount }} 권이 있습니다.</div>
    </div>
    <div v-if="books.length && !loadingStatus">
      <div class="books-list">
        <div v-for="i in books.length" :key="i">
          <BookCard :bookData="books[i - 1]"/>
        </div>
      </div>
      <v-pagination
        v-model="pageNm"
        :length="pageCount"
        :total-visible="9"
        circle
        color="grey"
        class="my-4"></v-pagination>
    </div>
    <div v-else-if="loadingStatus">
      <div class="service-logo">
        <img src="../../assets/images/team_logo/books.png" alt="team-logo">
      </div>
      <div class="loading-message">데이터를 불러오는 중 입니다.</div>
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
      pageNm: 1,
      pageCount: 0,
      totalBookCount: 0,
      books: [],
      loadingStatus: false
    }
  },
  computed: {
    ...mapState({
      searchKeyword: state => state.data.searchKeyword
    })
  },
  created() {
    this.onBookDetail()
  },
  methods: {
    async getBookDetail(query) {
      let paramsData = {
        'query': query,
        'page': this.pageNm
      }
      let bookData = await this.$store.dispatch('GET_BOOKS', paramsData)
      this.books = bookData.results
      this.totalBookCount = bookData.count
      this.pageCount = parseInt(bookData.count / 10) + 1
      this.loadingStatus = false
    },
    onBookDetail() {
      this.loadingStatus = true
      this.getBookDetail(this.$route.params.query)
    },
    goToBookListTop() {
      window.scrollTo(0, 0)
    }
  },
  watch: {
    pageNm() {
      this.onBookDetail()
      this.goToBookListTop()
    },
    searchKeyword() {
      this.pageNm = 1
      this.onBookDetail()
      this.goToBookListTop()
    }
  }
}
</script>

<style scoped>
.book-search-wrapper {
  width: 80%;
  margin: 0 auto;
}

.book-search-wrapper .book-search-name {
  font-family: 'Noto Sans KR';
}

.book-search-wrapper .book-search-name > .search-message{
  font-weight: 600;
  font-size: 1.1em;
  margin-bottom: 4px;
}

.book-search-wrapper .book-search-name > .book-count-message {
  color: grey;
  font-weight: 300;
  font-size: 0.95em;
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

  .book-search-wrapper {
    width: 90%;
  }
}
</style>
