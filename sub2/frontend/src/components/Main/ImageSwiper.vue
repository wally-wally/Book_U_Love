<template>
  <div class="mb-6" style="border: 1px solid transparent;">
    <v-carousel :height="450" show-arrows-on-hover class="desktop-carousel">
      <v-carousel-item
        v-for="(book, i) in books"
        :key="i"
        :src="images[i]"
        reverse-transition="fade-transition"
        transition="fade-transition">
        <div class="carousel-item-wrapper">
          <div class="carousel-title">{{ info.username }}</div>
          <div class="recommend-book">
            <div class="book-img">
              <img :src="book.coverLargeUrl" alt="book-image">
            </div>
            <div class="book-info">
              <div class="book-title">{{ book.title }}</div>
              <div class="book-category">{{ book.categorylist | categoryList }}</div>
              <div class="book-author">{{ book.author | filteredAuthor }}</div>
              <div class="book-description" v-if="book.description" v-html="book.description.slice(0, 60).replace('<b>', ' ') + '...'"></div>
              <div class="book-publisher-review" v-else-if="book.publisherReview" v-html="book.publisherReview.slice(0, 60).replace('<b>', ' ') + '...'"></div>
              <div class="book-contents" v-else v-html="book.contents.slice(0, 60).replace('<b>', ' ') + '...'"></div>
              <v-btn color="error" @click="goDetail(book.id)">READ MORE</v-btn>
            </div>
          </div>
        </div>
      </v-carousel-item>
    </v-carousel>
    <v-carousel :height="700" show-arrows-on-hover class="mobile-carousel">
      <v-carousel-item
        v-for="(book, i) in books"
        :key="i"
        :src="images[i]"
        reverse-transition="fade-transition"
        transition="fade-transition">
        <div class="carousel-item-wrapper">
          <div class="carousel-title">{{ info.username }}</div>
          <div class="recommend-book">
            <div class="book-img">
              <img :src="book.coverLargeUrl" alt="book-image">
            </div>
            <div class="book-info">
              <div class="book-title">{{ book.title }}</div>
              <div class="book-category">{{ book.categorylist | categoryList }}</div>
              <div class="book-author">{{ book.author | filteredAuthor }}</div>
              <div class="book-description" v-if="book.description" v-html="book.description.slice(0, 60).replace('<b>', ' ') + '...'"></div>
              <div class="book-publisher-review" v-else-if="book.publisherReview" v-html="book.publisherReview.slice(0, 60).replace('<b>', ' ') + '...'"></div>
              <div class="book-contents" v-else v-html="book.contents.slice(0, 60).replace('<b>', ' ') + '...'"></div>
              <v-btn color="error" @click="goDetail(book.id)">READ MORE</v-btn>
            </div>
          </div>
        </div>
      </v-carousel-item>
    </v-carousel>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'ImageSwiper',
  data() {
    return {
      books: [],
      images: [
        require('../../assets/images/image_slider/silder_image01.jpg'),
        require('../../assets/images/image_slider/silder_image02.jpg'),
        require('../../assets/images/image_slider/silder_image03.jpg')
      ]
    }
  },
  computed: {
    ...mapGetters(['info'])
  },
  created() {
    this.$store.commit('togglePostReviewLoading', true)
    this.getTotalRecommend()
  },
  methods: {
    async getTotalRecommend() {
      let dataOne = await this.$store.dispatch('GET_BOOKS', {sortby: "score",top:10})
      this.books.push(dataOne['results'][0])
      let dataTwo = await this.$store.dispatch('GET_BOOKS', {sortby: "count",top:10})
      this.books.push(dataTwo['results'][0])
      let recommendBooks = await this.$store.dispatch('GET_RECOMMEND_BOOKS')
      if (recommendBooks.length) {
        this.books.unshift(recommendBooks.sort((a, b) => b.avg - a.avg)[0])
      }
      await this.$store.commit('togglePostReviewLoading', false)
    },
    goDetail(bookID) {
      this.$router.push(`/book/${bookID}`)
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
.desktop-carousel {
  display: block;
}

.mobile-carousel {
  display: none;
}

.carousel-item-wrapper {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 90%;
  transform: translate(-50%, -50%);
  font-family: 'Gothic A1';
  text-align: center;
  background-color: rgba(255, 255, 255, 0.5);
  padding: 12px 4px;
  border-radius: 20px;
}

.recommend-book {
  display: grid;
  grid-template-columns: 1fr 3.5fr;
  gap: 10px;
  width: 90%;
  margin: 0 auto;
}

.book-img > img {
  max-width: 200px;
}

.book-info {
  text-align: left;
}

.carousel-title {
  font-family: 'Stylish';
  font-size: 24px;
  font-weight: 600;
  margin: 4px 0 16px;
}

.book-info > .book-title {
  font-weight: 600;
  font-size: 20px;
  margin-bottom: 2px;
}

.book-info > .book-category {
  font-size: 14px;
  margin-bottom: 10px;
}

.book-info > .book-author,
.book-info > .book-description,
.book-info > .book-publisher-review,
.book-info > .book-contents {
  margin-bottom: 20px;
}

.book-info > .book-publisher-review {
  font-size: 16px;
  font-family: 'Gothic A1';
}

@media (min-width: 700px) {
  .carousel-title:after {
    content: '님을 위해 이 책을 추천드려요!';
  }
}

@media (max-width: 700px) {
  .recommend-book {
    display: block;
  }

  .desktop-carousel {
    display: none;
  }

  .mobile-carousel {
    display: block;
  }

  .carousel-title:after {
    content: '님을 위한 강력 추천 도서';
  }
}

@media (max-width: 530px) {
  .carousel-title {
    font-size: 20px;
  }

  .book-info {
    font-size: 14px;
  }
}
</style>