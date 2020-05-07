<template>
  <div class="main-wrapper">
    <ImageSlider v-if="!isLogin" />
    <ImageSwiper v-else />
    <div v-for="theme in themes" :key="theme">
      <div v-if="(theme === 'age_gender' || theme === 'favoriteCategory') && isLogin">
        <BookSwiper :theme="theme" />
      </div>
      <div v-else-if="theme !== 'age_gender' && theme !== 'favoriteCategory'">
        <BookSwiper :theme="theme" />
      </div>
    </div>
    <YoutubeSwiper />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import ImageSlider from '@/components/Main/ImageSlider'
import ImageSwiper from '@/components/Main/ImageSwiper'
import BookSwiper from '@/components/Main/BookSwiper'
import YoutubeSwiper from '@/components/Main/YoutubeSwiper'

export default {
  name: 'Main',
  components: {
    ImageSlider,
    ImageSwiper,
    BookSwiper,
    YoutubeSwiper
  },
  data() {
    return {
      themes: ['sortScore', 'sortReviewCnt']
    }
  },
  computed: {
    ...mapState({
      isLogin: state => state.user.isLogin
    })
  },
  created() {
    if (this.isLogin) {
      this.checkRecommendBooksExist()
    }
  },
  methods: {
    async checkRecommendBooksExist() {
      let bookdata = await this.$store.dispatch('GET_RECOMMEND_BOOKS')
      if (!bookdata.length) {
        this.themes.push('favoriteCategory')
      } else {
        this.themes.unshift('favoriteCategory')
      }
    }
  }
}
</script>

<style scoped>
.main-wrapper {
  width: 80%;
  margin: 0 auto;
  box-sizing: border-box;
}

@media (max-width: 600px) {
  .main-wrapper {
    width: 90%;
  }
}
</style>