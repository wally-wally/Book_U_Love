<template>
  <div class="mb-6">
    <div class="book-ranking-title">
      <span>BooksRanking</span>
      <br>
      <div class="sortby" @click="this.resort"><span>{{this.sort}}</span></div>
    </div>
    <div v-for="(book, i) in books[this.sort]" :key="i">
      <div>
        {{book.review_cnt}}개 - {{book.avg}} 점
      </div>
      <div  class="book-ranking-list">
      <router-link :to="`/book/${book.id}`">
      <div class="book-img">
        <img :src="book.coverSmallUrl" alt="book-image" width="50">
      </div>
      </router-link>
      <div class="book-detail">
        <div class="book-name">
          <span>{{ book.title }}</span>
        </div>
        <div v-if="book.author.length > 1 " class="book-author">{{ book.author[0].name }} 외 {{book.author.length-1}}명</div>
        <div v-else class="book-author">{{ book.author[0].name }}</div>
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
      this.getBooks()
  },
  methods : {
    async getBooks() {
      const scoredata = await this.$store.dispatch('GET_BOOKS', {sortby: "score",top:10})
      console.log(scoredata)
      this.books['평점순'] = scoredata["results"]
      const reviewdata =  await this.$store.dispatch('GET_BOOKS', {sortby: "count",top:10})
      this.books['리뷰 갯수순'] = reviewdata["results"]
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
  width: 200px;
  font-size: 0.9em;
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