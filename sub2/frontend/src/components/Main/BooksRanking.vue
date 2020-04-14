<template>
  <div class="mb-6">
    <div class="book-ranking-title">
      <span>BooksRanking</span>
    </div>
    <div v-for="(book, i) in books" :key="i" class="book-ranking-list">
      <div class="book-img">
        <img src="http://image.kyobobook.co.kr/images/book/large/701/l9788954752701.jpg" alt="book-image" width="50">
      </div>
      <div class="book-detail">
        <div class="book-name">
          <span>{{ book.name }}</span>
        </div>
        <div class="book-author">{{ book.author }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      books: [ // 샘플 데이터
        {
          'name': '펭수, 디 오리지널',
          'main-img': 'http://image.kyobobook.co.kr/images/book/large/701/l9788954752701.jpg',
          'author': 'EBS'
        },
        {
          'name': '펭수, 디 오리지널',
          'main-img': 'http://image.kyobobook.co.kr/images/book/large/701/l9788954752701.jpg',
          'author': 'EBS'
        },
      ]
    }
  },
}
</script>

<style scoped>
.book-ranking-title {
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
</style>