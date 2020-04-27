<template>
  <div class="book-card-wrapper">
      <router-link :to="`/book/${this.bookData.id}`">
    <div class="book-img">
      <img style="width:200px;height:265px;" :src="this.imgUrl" alt="book-image">
    </div>
      </router-link>
    <div class="book-info">
      <router-link :to="`/book/${this.bookData.id}`">
        <div class="book-title" style="color:black;">{{ this.bookData.title }}</div>
      </router-link>
      <div class="book-category">{{bookData.categorylist | categoryList }}</div>
      <span style="color:#ffa136">★{{bookData.avg}}</span><span style="font-size:0.9em"> ({{bookData.review_cnt}}명)</span>
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
  }
}
</script>

<style scoped>
.book-card-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  margin: 30px;
}
.book-img {
  padding-bottom: 1.4em;
}

.book-img img {
  display: block;
  margin: auto;
  width: 90%;
  border: 0.8px solid lightgray;
  box-shadow: 3px 4px 4px rgba(0, 0, 0, 0.05);
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

@media (max-width: 600px) {
  .book-img img {
    width: 4vw;
  }
}
.book-title{
  font-weight: 400;
  letter-spacing: -0.5px;
  line-height: 20px;
  /* width:200px; */
}
</style>
