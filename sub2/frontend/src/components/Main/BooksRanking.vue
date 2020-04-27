<template>
  <div class="mb-6">
    <div class="book-ranking-title">
      <span>BooksRanking</span>
      <br>
      <div class="sortby" @click="this.resort"><span>{{this.sort}}</span></div>
    </div>
    <div v-for="(book, i) in books[this.sort]" :key="i" class="book-rank-wrapper">
      <div class="book-info">
        <div class="ranking-index" :style="{ color: setColor(i + 1) }">{{ i + 1 }}위</div>
        <div class="book-small-info">
          <span class="book-review-cnt">{{book.review_cnt}}개</span>
          <span class="book-review-avg">{{book.avg}}점</span>
        </div>
      </div>
      <div class="book-ranking-list">
        <router-link :to="`/book/${book.id}`">
          <div class="book-img">
            <img :src="book.coverSmallUrl" alt="book-image" width="50">
          </div>
        </router-link>
        <div class="book-detail">
          <div class="book-name"><span>{{ book.title }}</span></div>
          <div v-if="book.author.length > 1 " class="book-author">{{ book.author[0].name }} 외 {{book.author.length-1}}명</div>
          <div v-else class="book-author">{{ book.author[0].name }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { rankingColor } from '@/utils/rankingColor.js'

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
    },
    setColor(rank) {
      return rankingColor(rank)
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

.book-rank-wrapper {
  margin-bottom: 16px;
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
  font-family: 'Gothic A1'; 
}

.book-detail .book-name,
.book-detail .book-author {
  width: 200px;
  font-size: 0.9em;
}

.book-detail .book-author::before {
  content: 'by '
}

.book-info {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  margin-bottom: 8px;
  font-family: 'Gothic A1';
}

.ranking-index {
  font-weight: 600;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.15);
}

.book-small-info {
  font-weight: 500;
}

.book-small-info > span:first-child {
  padding-right: 10px;
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