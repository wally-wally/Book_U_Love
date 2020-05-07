<template>
  <div class="mb-6" style="border: 1px solid transparent;">
    <div class="loading-section" v-if="loading">
      <p class="text-center">
        <img src="../../assets/images/team_logo/logo.png" alt="service-logo">
      </p>
      <p>Book_U_Love 도서 추천 서비스입니다.</p>
    </div>
    <v-carousel v-if="!loading" :height="450" show-arrows-on-hover class="desktop-carousel">
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
    <v-carousel v-if="!loading" :height="700" show-arrows-on-hover class="mobile-carousel">
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
      ],
      loading: false
    }
  },
  computed: {
    ...mapGetters(['info'])
  },
  created() {
    this.loading = true
    this.$store.commit('togglePostReviewLoading', true)
    this.getTotalRecommend()
  },
  methods: {
    getRandomIntInclusive(min, max) {
      min = Math.ceil(min)
      max = Math.floor(max)
      return Math.floor(Math.random() * (max - min + 1)) + min
    },
    async getTotalRecommend() {
      let tempBooks = []
      let dataOne = await this.$store.dispatch('GET_BOOKS', {sortby: "score",top:10})
      dataOne['results'].slice(0, 4).forEach(bookData => {
        tempBooks.push(bookData)
      })
      let dataTwo = await this.$store.dispatch('GET_BOOKS', {sortby: "count",top:10})
      dataTwo['results'].slice(0, 2).forEach(bookData => {
        tempBooks.push(bookData)
      })
      let recommendBooks = await this.$store.dispatch('GET_RECOMMEND_BOOKS')
      if (recommendBooks.length) {
        recommendBooks.sort((a, b) => b.avg - a.avg).slice(0, 8).forEach(bookData => {
          tempBooks.unshift(bookData)
        })
      }
      await this.selectRandomBooks(tempBooks)
      this.$store.commit('togglePostReviewLoading', false)
      this.loading = false
    },
    async selectRandomBooks(tempBooks) {
      let idxGroup = []
      while (idxGroup.length < 3) {
        let randomIdx = this.getRandomIntInclusive(0, tempBooks.length - 1)
        if (!idxGroup.includes(randomIdx)) {
          idxGroup.push(randomIdx)
          this.books.push(tempBooks[randomIdx])
        }
      }
      this.books = this.books.sort((a, b) => b.avg - a.avg)
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

.loading-section {
  width: 100%;
}

.loading-section img {
  max-width: 300px;
  width: 100%;
}

.loading-section > p:last-child {
  text-align: center;
  font-weight: 600;
  font-family: 'Noto Sans KR';
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