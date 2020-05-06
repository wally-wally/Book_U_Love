<template>
  <div class="mt-3 mb-6">
    <!-- <div class="text-right mb-3" v-if="!this.allBooks.length">
      <v-btn color="error" @click="toggleDialog">전체 도서 데이터 가져오기</v-btn>
    </div> -->
    <v-data-table
      v-if="!this.postReviewLoading && !fetchAll"
      :headers="tableHeaders"
      :items="books"
      item-key="title"
      hide-default-footer
      color="#E6CC00"
      class="elevation-1">
      <template v-slot:item.categorylist="{ item }">
        {{ item.categorylist | categoryList }}
      </template>
    </v-data-table>
    <!-- <v-data-table
      v-if="!this.postReviewLoading && fetchAll"
      :headers="tableHeaders"
      :items="books"
      :single-expand="true"
      :search="searchKeyword2"
      :page.sync="page"
      show-expand
      item-key="isbn"
      hide-default-footer
      color="#E6CC00"
      @page-count="pageCount = $event"
      class="elevation-1">
      <template v-slot:top>
        <v-text-field v-model="searchKeyword2" append-icon="fa-search" label="도서 검색" single-line hide-details class="mx-4" color="#f7b157"></v-text-field>
      </template>
      <template v-slot:item.categorylist="{ item }">
        {{ item.categorylist | categoryList }}
      </template>
    </v-data-table> -->
    <div class="book-pagination" v-if="books.length && !fetchAll && !this.postReviewLoading">
      <i :class="pageNm === 1 ? 'fas fa-chevron-left limit-page-nm' : 'fas fa-chevron-left'" @click="changePageNm(-1)"></i>
      <span>{{ pageNm }}</span>
      <span> / </span>
      <span>{{ pageCount }}</span>
      <i :class="pageNm === pageCount ? 'fas fa-chevron-right limit-page-nm' : 'fas fa-chevron-right'" @click="changePageNm(1)"></i>
    </div>
    <!-- <div class="book-pagination" v-if="books.length && fetchAll && !this.postReviewLoading">
      <v-pagination v-model="page" :length="pageCount" :total-visible="7" circle color="#E6CC00"></v-pagination>
    </div> -->
    <v-dialog v-model="dialog" width="600" persistent>
      <v-card>
        <v-card-text class="pb-0">
          <div class="text-center alert-dialog-text">
            <i class="fas fa-hourglass-half"></i>
            <div>전체 도서 데이터를 가져오는데 시간이 오래 걸릴 수 있습니다.</div>
            <div>그래도 진행하시겠습니까?</div>
          </div>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" @click="fetchAllBooks" :style="{ 'fontFamily': 'Stylish', 'fontSize': '17px' }">가져오기</v-btn>
          <v-btn color="warning" @click="toggleDialog" :style="{ 'fontFamily': 'Stylish', 'fontSize': '17px' }">닫기</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data() {
    return {
      page: 1,
      pageNm: 1,
      pageCount: 0,
      tableHeaders: [
        { text: '제목', value: 'title', sortable: false },
        { text: 'ISBN', value: 'isbn', sortable: false },
        { text: '카테고리', value: 'categorylist', sortable: false },
        { text: '평균 평점', value: 'avg', sortable: false },
        { text: '리뷰 개수', value: 'r_cnt', sortable: false }
      ],
      books: [],
      searchKeyword: '',
      searchKeyword2: '',
      dialog: false,
      fetchAll: false
    }
  },
  computed: {
    ...mapState({
      categories: state => state.data.categories,
      allBooks: state => state.data.allBooks,
      postReviewLoading: state => state.data.postReviewLoading
    })
  },
  created() {
    this.$store.commit('togglePostReviewLoading', true)
    // if (this.allBooks.length) {
    //   this.fetchAll = true
    //   this.books = this.allBooks
    //   this.pageCount = this.$store.state.data.allBooksCount
    //   this.$store.commit('togglePostReviewLoading', false)
    //   return
    // }
    this.getBooksList()
  },
  methods: {
    async getBooksList() {
      let booksData = await this.$store.dispatch('GET_BOOKS', { 'page': this.pageNm })
      this.books = booksData.results
      this.pageCount = parseInt(booksData.count / 10) + (booksData.count % 10 === 0 ? 0 : 1)
      this.$store.commit('allBooksCount', this.pageCount)
      await this.$store.commit('togglePostReviewLoading', false)
    },
    changePageNm(val) {
      if ((this.pageNm < this.pageCount && val === 1) || (this.pageNm > 1 && val === -1)) {
        this.pageNm += val
        this.$store.commit('togglePostReviewLoading', true)
        this.books = []
        this.getBooksList()
      }
    },
    toggleDialog() {
      this.dialog = !this.dialog
    },
    async fetchAllBooks() {
      this.$store.commit('fetchAllBookStatus', true)
      this.dialog = false
      if (!this.allBooks.length) {
        this.$store.commit('togglePostReviewLoading', true)
        this.books = []
        let count = 1
        for (let i = 1; i < this.pageCount + 1; ++i) {
          let bookData = await this.$store.dispatch('GET_BOOKS', { 'page': i })
          await this.books.push(...bookData.results)
          await this.$store.commit('getNowCountBooks', count)
          count += 1
        }
        await this.storeAllBooks()
      } else {
        this.books = this.allBooks
      }
    },
    storeAllBooks() {
      this.fetchAll = true
      this.$store.commit('storeAllBooks', this.books)
      this.$store.commit('togglePostReviewLoading', false)
      this.$store.commit('fetchAllBookStatus', false)
    }
  }
}
</script>

<style scoped>
.book-pagination {
  text-align: center;
  font-weight: 600;
  font-family: 'Gothic A1';
  margin: 20px 0 30px;
}

.book-pagination > i {
  padding: 0 8px;
}

.book-pagination > i:not(.limit-page-nm) {
  cursor: pointer;
}

.fas.limit-page-nm {
  color: lightgray;
}

.alert-dialog-text {
  font-family: 'Stylish';
  font-weight: 600;
}

.alert-dialog-text i {
  font-size: 100px;
  margin-bottom: 12px;
}

.alert-dialog-text > div {
  font-size: 18px;
  line-height: 2;
}
</style>