<template>
  <div class="mb-6">
    <div class="book-ranking-title">
      <span>BooksRanking</span>
      <br>
      <div class="sortby" @click="this.resort"><span>{{this.sort}}</span></div>
    </div>
    <div v-for="(book, i) in books[this.sort]" :key="i">
      <div>
        {{book.review_cnt}}개 - {{book.avg_score}} 점
      </div>
      <div  class="book-ranking-list">
      <div class="book-img">
        <img :src="book.coverSmallUrl" alt="book-image" width="50">
      </div>
      <div class="book-detail">
        <div class="book-name">
          <span>{{ book.name }}</span>
        </div>
        <div class="book-author">{{ book.author }}</div>
      </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      books: {'평점순': [],'리뷰 갯수순' : []},
      sort : '평점순'
    }
  },
  mounted(){
      this.getBookDetail()
  },
  methods : {
    async getBookDetail() {
      this.books['평점순'] = await this.$store.dispatch('GET_BOOK_DETAIL', {sortby: "score",top:10})
      this.books['리뷰 갯수순'] = await this.$store.dispatch('GET_BOOK_DETAIL', {sortby: "count",top:10})
    },
    resort() {
      if (this.sort == "평점순"){
        this.sort = "리뷰 갯수순";
      } else {
        this.sort = "평점순";
      }
    }
  }
}
</script>

<style scoped>
.book-ranking-title {
  text-align: center;
  font-family: 'Julius Sans One';
  font-weight: 600;
  font-weight: 1.1em;
  margin-bottom: 0.6em;
}

.book-ranking-list {
  display: flex;
  margin-bottom: 0.4em;
}

.book-img img {
  vertical-align: top;
  margin-right: 0.2em;
}

.book-detail {
  display: flex;
  flex-wrap: wrap;
  align-content: space-between;
  font-family: 'Sarabun'; 
}

.book-detail .book-name,
.book-detail .book-author {
  display: inline-block;
  width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 0.9em;
}

.book-detail .book-name span:hover {
  cursor: pointer;
  font-weight: 600;
}

.book-detail .book-author::before {
  content: 'by '
}

@media (max-width: 970px) {
  .book-detail .book-name,
  .book-detail .book-author {
    width: 100%;
  }
}

.sortby {
  display: inline-block;
  justify-items: right;
} 
.sortby:hover {
  cursor: pointer;
}
</style>