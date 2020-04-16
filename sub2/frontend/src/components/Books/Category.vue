<template>
  <div class="category-wrapper">
    <div class="category-name ml-2 my-2 pl-3">
      {{ searchCategory }}
    </div>
    <div class="row" v-if="books.length">
      <div v-for="book in books" :key="book.id" class="books-list col-lg-3 col-md-4 col-sm-6">
        <BookCard :bookData="book"/>
      </div>
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
      books : []
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
      let bookData = await this.$store.dispatch('GET_BOOK_DETAIL', {'category': id})
      this.books = bookData
    },
    onBookDetail() {
      let categoryID = Number(this.$route.params.id)
      this.getBookDetail(categoryID)
    },
    goToBookListTop() {
      window.scrollTo(0, 0)
    }
  },
  watch: {
    '$route'() {
      this.pageNm = 1
      this.onBookDetail()
      this.goToBookListTop()
    },
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
</style>