<template>
  <div class="book-card-wrapper">
    <router-link :to="`/book/${this.bookData.id}`">
      <div class="book-img">
        <img v-if="this.$route.name !== 'MainPage'" style="width:200px;height:265px;" :src="this.imgUrl" alt="book-image">
        <img v-else :src="this.imgUrl" alt="book-image" class="main-book-img">
      </div>
    </router-link>
    <div class="book-info" v-if="this.$route.name !== 'MainPage'">
      <router-link :to="`/book/${this.bookData.id}`">
        <div class="book-title" style="color:black;">{{ this.bookData.title }}</div>
      </router-link>
      <div class="book-category">{{bookData.categorylist | categoryList }}</div>
      <span style="color:#ffa136">★{{bookData.avg}}</span><span style="font-size:0.9em"> ({{bookData.r_cnt}}명)</span>
    </div>
    <div class="main-book-info" v-else>
      <div class="book-title">{{ this.bookData.title }}</div>
      <div class="book-author">{{ this.bookData.author | filteredAuthor }}</div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  props: {
    bookData: {
      type: Object
    }
  },
  computed: {
    ...mapState({
      categories: state => state.data.categories
    }),
    imgUrl() {
      let url = this.bookData.coverLargeUrl
      let noImageCondition = [' ', 'http://bimage.interpark.com/bookpinion/add_images/noimg_70_98.gif']
      return noImageCondition.includes(url) ? require('../../assets/images/no_image/no_image.png') : url
    }
  },
  filters: {
    filteredAuthor(author) {
      if (!author.length) {
        return '작가 미등록'
      } else {
        let authorCnt = author.length
        let firstAuthorName = author[0].name
        return firstAuthorName + (authorCnt >= 2 ? ` 외 ${authorCnt - 1}명` : '')
      }
    }
  }
}
</script>

<style scoped>
.book-card-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin: 10px 15px;
}

.book-img {
  padding-bottom: 1.4em;
}

.book-img img {
  display: block;
  margin: auto;
  width: 100%;
  border: 0.8px solid lightgray;
  box-shadow: 3px 4px 4px rgba(0, 0, 0, 0.05);
}

.book-img img.main-book-img {
  max-width: 200px;
  height: 250px;
}

.book-info {
  text-align: center;
}

.book-info .book-category {
  font-size: 0.75em;
  margin-bottom: 0.75em;
}

.book-info .book-title {
  margin-bottom: 0.75em;
}

.book-info .book-detail-link {
  display: inline-block;
  padding: 0.5em 1.5em;
  margin: 10px 0;
  color: #fff;
  text-decoration: none;
  font-size: 0.9em;
  border-radius: 40px;
  overflow: hidden;
  background: linear-gradient(90deg, #0162c8, #55e7fc);
}

.book-info .book-detail-link:hover {
  cursor: pointer;
  box-shadow: 3px 5px 5px rgba(0, 0, 0, 0.1);
}

@media (min-width: 960px) and (max-width: 1264px) {
  .book-info .book-title {
    font-size: 0.95em;
  }
}

@media (min-width: 600px) and (max-width: 960px) {
  .book-info .book-title {
    font-size: 0.9em;
  }
}

.book-title{
  font-weight: 400;
  letter-spacing: -0.5px;
  line-height: 20px;
  /* width:200px; */
}

.main-book-info {
  text-align: left;
  line-height: 1;
  margin-top: -5px;
  font-family: 'Gothic A1';
}

.main-book-info .book-title,
.main-book-info .book-author {
  display: inline-block;
  width: 100%;
}

.main-book-info .book-title {
  font-size: 15px;
  font-weight: 600;
}

.main-book-info .book-author {
  font-size: 14px;
}
</style>
