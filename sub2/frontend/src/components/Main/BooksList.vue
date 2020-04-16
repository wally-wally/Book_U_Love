<template>
  <div class="my-1">
    <div class="row">
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
      pageCount: 0
    }
  },
  computed: {
    ...mapState({
      books: state => state.data.books
    })
  },
  mounted() {
    this.getBooksList()
  },
  methods: {
    async getBooksList() {
      const booksData = await this.$store.dispatch('GET_BOOKS', this.pageNm)
      this.pageCount = parseInt(booksData.count / 10)
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
</style>