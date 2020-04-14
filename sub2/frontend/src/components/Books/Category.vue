<template>
  <div class="category-wrapper">
    <div class="category-name ml-2 my-2 pl-3">
      {{ searchCategory }}
    </div>
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
    <div v-else-if="loadingStatus">
      <div class="service-logo">
        <img src="../../assets/images/team_logo/books.png" alt="team-logo">
      </div>
      <div class="loading-message">데이터를 불러오는 중 입니다.</div>
    </div>
    <div v-else class="no-category-books">
      <i class="fas fa-times d-block text-center"></i>
      <p>해당 카테고리의 도서가 없습니다.</p>
    </div>
  </div>
</template>

<script>
import BookCard from '@/components/Books/BookCard'

export default {
  name : "category",
  components: {
    BookCard
  },
  data() {
    return {
      pageNm: 1,
      pageCount: 0,
      books : [],
      loadingStatus: false
    }
  },
  computed: {
    searchCategory() {
      let categoryList = this.$store.state.data.categories
      return categoryList.find(category => category.id === Number(this.$route.params.id))['name']
    }
  },
  created() {
    this.onBookDetail()
  },
  methods : {
    async getBookDetail(id) {
      let paramsData = {
        'category': id,
        'page': this.pageNm
      }
      let bookData = await this.$store.dispatch('GET_BOOK_DETAIL', paramsData)
      this.books = bookData.results
      this.pageCount = parseInt(bookData.count / 10) + 1
      this.loadingStatus = false
    },
    onBookDetail() {
      this.loadingStatus = true
      let categoryID = Number(this.$route.params.id)
      this.getBookDetail(categoryID - (categoryID === 100 || categoryID === 200 ? 0 : 1))
    },
    goToBookListTop() {
      window.scrollTo(0, 0)
    }
  },
  watch: {
    '$route': 'onBookDetail',
    pageNm() {
      this.onBookDetail()
      this.goToBookListTop()
    }
  }
}
</script>

<style scoped>
.category-wrapper {
  width: 90%;
  margin: 0 auto;
}

.category-wrapper .category-name {
  font-family: 'Noto Sans KR';
  font-weight: 600;
  font-size: 1.1em;
}

.no-category-books {
  font-family: 'Gothic A1';
  color: crimson;
}

.no-category-books i {
  font-size: 7em;
  margin: 0.2em 0;
}

.no-category-books > p {
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
</style>