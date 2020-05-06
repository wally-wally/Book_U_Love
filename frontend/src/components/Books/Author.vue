<template>
  <div class="author-wrapper">
    <div class="author-title">{{ author.name }}</div>
    <hr color="lightgray">
    <div class="author-into-wrapper">
      <div class="author-section">
        <div class="author-img">
          <img :src="this.imgUrl" alt="author-image">
        </div>
        <div class="author-info">
          <div class="author-info-title" v-if="author.boneDate">
            📆 생년월일
          </div>
          <div class="author-info-section" v-if="author.boneDate">
            {{ author.boneDate }}
          </div>
          <div class="author-info-title" v-if="author.region">
            🌎 출생지
          </div>
          <div class="author-info-section" v-if="author.region">
            {{ author.region }}
          </div>
          <div class="author-info-title" v-if="author.description">
            📃 작가 소개
          </div>
          <div class="author-info-section" v-if="author.description">
            {{ author.description }}
          </div>
        </div>
      </div>
    </div>
    <hr color="lightgray">
    <div class="author-books">
      <div class="author-books-title">{{ author.name }}의 출간작</div>
      <div class="author-books-list">
        <div v-for="book in books" :key="book.id">
          <BookCard :bookData="book"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchauthor } from '@/api/index.js'
import BookCard from '@/components/Books/BookCard'

export default {
  components: {
    BookCard
  },
  name  : 'author',
  data() {
    return {
      author: {},
      books : [],
    }
  },
  created() {
    this.getauthor(this.$route.params.id)
    this.getauthorbook(this.$route.params.id)
  },
  methods : {
    async getauthorbook(id) {
      let bookData = await this.$store.dispatch('GET_BOOKS', {author:id})
      this.books = bookData.results
    },
    async getauthor(id) {
      const data = await fetchauthor(id)
      this.author = data.data
    }
  },
  computed:{
    imgUrl(){
      let url = this.author.imgUrl
      let noImageCondition = [' ','http://bimage.interpark.com/bookpinion/add_images/noimg_70_98.gif']
      return noImageCondition.includes(url) ? require('../../assets/images/no_image/no_image.png') : url
    }
  }
}
</script>

<style scoped>
.author-wrapper {
  margin-top: 8px;
}

.author-title {
  margin-bottom: 20px;
  font-size: 1.6rem;
  font-weight: bold;
  font-family: 'Noto Sans KR';
}

.author-into-wrapper {
  border: 10px solid #eee;
  margin: 20px 0 40px;
  padding: 20px;
}

.author-section {
  display: grid;
  grid-template-columns: 1fr 4fr;
  gap: 10px;
}

.author-section .author-img {
  text-align: center;
}

.author-img img {
  max-width: 200px;
}

.author-section .author-info .author-info-title {
  display: inline-block;
  font-size: 20px;
  font-weight: 600;
  font-family: 'Noto Sans KR';
  padding-bottom: 4px;
  margin-bottom: 10px;
  border-bottom: 2px solid silver;
}

.author-section .author-info .author-info-section {
  font-family: 'Gothic A1';
  font-size: 18px;
  margin-bottom: 20px;
}

.author-section .author-info .author-info-section:last-child {
  font-size: 15px;
  line-height: 1.7;
  letter-spacing: 0.2px;
}

@media (max-width: 700px) {
  .author-section {
    display: block;
  }

  .author-section .author-img img{
    width: 70%;
    margin-bottom: 20px;
  }
}

.author-books {
  margin: 40px 0;
}

.author-books .author-books-title {
  font-family: 'Noto Sans KR';
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 10px;
}

.author-books-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(25%, auto));
}

@media (max-width: 1264px) {
  .author-books-list {
    grid-template-columns: repeat(auto-fill, minmax(33.33333%, auto));
  }
}
@media (max-width: 960px) {
  .author-books-list {
    grid-template-columns: repeat(auto-fill, minmax(50%, auto));
  }
}
@media (max-width: 600px) {
  .author-books-list {
    grid-template-columns: repeat(auto-fill, minmax(100%, auto));
  }
}
</style>