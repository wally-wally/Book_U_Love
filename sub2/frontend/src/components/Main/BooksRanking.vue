<template>
  <div class="mb-6">
    <div class="book-ranking-title">
      <span>BooksRanking</span>
      <br>
      <div class="sortby">
        <span :class="sortCriteria === 'sortByScore' ? 'select-sort-item' : ''" @click="resort(0)">평점순</span>
        <span :class="sortCriteria === 'sortByReviewCnt' ? 'select-sort-item' : ''" @click="resort(1)">리뷰 갯수 순</span>
      </div>
    </div>
    <div v-if="!loadingStatus">
      <div v-for="(book, i) in books[this.sortCriteria].slice(0, idx)" :key="i" class="book-rank-wrapper">
        <div class="book-info">
          <div class="ranking-index" :style="{ color: setColor(i + 1) }">{{ i + 1 }}위</div>
          <div class="book-small-info" v-if="sortCriteria === 'sortByScore'">
            <span class="now-sort-criteria">{{book.avg}}점</span>
            <span>{{book.review_cnt}}개</span>
          </div>
          <div class="book-small-info" v-else>
            <span>{{book.avg}}점</span>
            <span class="now-sort-criteria">{{book.review_cnt}}개</span>
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
      <div class="more-btn" v-if="smallSize">
        <span @click="showMoreItems">4 ~ 10위 {{ !moreItems ? '보기' : '숨기기' }}</span>
      </div>
    </div>
    <div v-else>
      <p class="alert-message">데이터를 불러오는 중입니다.</p>
    </div>
  </div>
</template>

<script>
import { rankingColor } from '@/utils/rankingColor.js'

export default {
  data() {
    return {
      books: {'sortByScore': [], 'sortByReviewCnt' : []},
      sortCriteria : 'sortByScore',
      idx: 10,
      smallSize: false,
      moreItems: false,
      loadingStatus: false
    }
  },
  created(){
    this.loadingStatus = true
    this.getBooks()
    this.idx = window.innerWidth <= 800 ? 3 : 10
    this.smallSize = window.innerWidth <= 800
  },
  mounted() {
    window.addEventListener('resize', () => {
      this.smallSize = window.innerWidth <= 800
      if (window.innerWidth > 800) {
        this.idx = 10
        this.smallSize = false
      } else {
        this.idx = !this.moreItems ? 3 : 10
        this.smallSize = true
      }
    })
  },
  methods : {
    async getBooks() {
      const scoredata = await this.$store.dispatch('GET_BOOKS', {sortby: "score",top:10})
      this.books['sortByScore'] = scoredata["results"]
      const reviewdata =  await this.$store.dispatch('GET_BOOKS', {sortby: "count",top:10})
      this.books['sortByReviewCnt'] = reviewdata["results"]
      this.loadingStatus = false
    },
    resort(val) {
      this.sortCriteria = val ? 'sortByReviewCnt' : 'sortByScore'
    },
    setColor(rank) {
      return rankingColor(rank)
    },
    showMoreItems() {
      this.idx = !this.moreItems ? 10 : 3
      this.moreItems = !this.moreItems
    }
  }
}
</script>

<style scoped>
.book-ranking-title {
  text-align: center;
  font-family: 'Julius Sans One';
  font-weight: 1.1rem;
  margin-bottom: 20px;
}

.book-ranking-title > span:first-child {
  font-weight: 600;
}

.book-rank-wrapper {
  padding: 4px 0;
  border-bottom: 1px solid silver;
}

.book-rank-wrapper:first-child {
  border-top: 1px solid silver;
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

.book-detail .book-author:before {
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

.book-small-info > .now-sort-criteria {
  color: #ff5252;
  font-weight: 600;
}

.book-small-info > span:not(.now-sort-criteria) {
  font-size: 14px;
}

.more-btn {
  float: right;
  transform: translateY(10%);
  margin-bottom: 20px;
  transition: all .1s;
}

.more-btn > span {
  width: 100%;
  font-family: 'Gothic A1';
  font-size: 14px;
  border: 0.8px solid silver;
  border-radius: 15px;
  margin-top: 0px;
  padding: 6px;
}

.more-btn:hover {
  cursor: pointer;
  transform: translateY(5%);
}

.more-btn:hover > span {
  font-weight: 600;
  box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.15);
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
  margin-top: 5px;
  font-family: 'Gothic A1';
}

.sortby:hover {
  cursor: pointer;
}

.sortby > span {
  margin: 0 10px;
  padding-bottom: 5px;
}

.select-sort-item {
  font-weight: 600;
  border-bottom: 1px solid darkgray;
}

.alert-message {
  text-align: center;
  font-family: 'Gothic A1';
  font-weight: 600;
  font-size: 15px;
  margin-top: 40px;
}
</style>