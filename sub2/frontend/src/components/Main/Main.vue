<template>
  <div class="main-wrapper">
    <ImageSlider />
    <ImageSwiper />
    <div v-for="theme in themes" :key="theme">
      <div v-if="(theme === 'age_gender' || theme === 'favoriteCategory') && isLogin">
        <BookSwiper :theme="theme" />
      </div>
      <div v-else-if="theme !== 'age_gender' && theme !== 'favoriteCategory'">
        <BookSwiper :theme="theme" />
      </div>
    </div>
   <div>
    <!-- <YoutubeSwiper /> -->
    </div>
    <!-- <div class="my-6 main-contents">
      <div class="main-sidebar">
        <WeeklyAuthor />
        <BooksRanking />
      </div>
      <div class="main-book-section">
        <BooksHeader />
        <BooksList />
      </div>
    </div> -->
  </div>
</template>

<script>
import { mapState } from 'vuex'
import ImageSlider from '@/components/Main/ImageSlider'
import ImageSwiper from '@/components/Main/ImageSwiper'
import BookSwiper from '@/components/Main/BookSwiper'
// import YoutubeSwiper from '@/components/Main/YoutubeSwiper'

// import WeeklyAuthor from '@/components/Main/WeeklyAuthor'
// import BooksRanking from '@/components/Main/BooksRanking'
// import BooksHeader from '@/components/Main/BooksHeader'
// import BooksList from '@/components/Main/BooksList'

export default {
  name: 'Main',
  components: {
    ImageSlider,
    ImageSwiper,
    BookSwiper,
    // YoutubeSwiper
    // WeeklyAuthor,
    // BooksRanking,
    // BooksHeader,
    // BooksList
  },
  data() {
    return {
      themes: ['favoriteCategory', 'sortScore', 'sortReviewCnt']
      // themes: ['favoriteCategory', 'age_gender', 'sortScore', 'sortReviewCnt']
    }
  },
  computed: {
    ...mapState({
      isLogin: state => state.user.isLogin
    })
  }
}
</script>

<style scoped>
.main-wrapper {
  width: 80%;
  margin: 0 auto;
  box-sizing: border-box;
}

/* .main-contents {
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 4fr;
  gap: 0.75em;
}

.main-contents .main-sidebar {
  min-width: 250px;
}

@media (max-width: 800px) {
  .main-contents {
    display: block;
  }
} */
</style>