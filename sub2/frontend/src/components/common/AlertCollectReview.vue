<template>
  <v-snackbar v-model="snackbar" :vertical="true" :timeout="10000" :multi-line="true" :style="{ fontFamily: 'Gothic A1' }">
    {{ info.username }}님에게 적합한 책을 추천해드리기 위해 리뷰를 추가로 작성해주세요.
    <br>
    ({{ sec }}초 후 자동으로 사라짐)
    <v-btn class="d-inline-block" color="pink" text @click="goCollectPage">
      <b>작성 페이지로 이동</b>
    </v-btn>
  </v-snackbar>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import { fetchMyInfo } from '@/api/index.js'

export default {
  data() {
    return {
      snackbar: false,
      sec: 0,
    }
  },
  computed: {
    ...mapState({
      isLogin: state => state.user.isLogin
    }),
    ...mapGetters(['info'])
  },
  created() {
    if (this.isLogin && this.$route.name === 'MainPage') {
      this.checkReviewCnt()
      this.countTime()
    }
  },
  methods: {
    async checkReviewCnt() {
      const reviewCnt = await this.$store.dispatch('GET_MYBOOK_REVIEW_CNT')
      this.snackbar = reviewCnt < 20
    },
    countTime() {
      this.sec = 10
      this.polling = setInterval(() => this.sec -= 1, 1000)
      setTimeout(() => clearInterval(this.polling), 10000)
    },
    goCollectPage() {
      this.snackbar = false
      this.$router.push('/collect')
    }
  },
  beforeDestroy() {
    clearInterval(this.polling)
  },
  watch: {
    isLogin() {
      if (!this.isLogin) {
        this.snackbar = false
        clearInterval(this.polling)
      }
    },
    '$route'() {
      if (this.isLogin && this.$route.path === '/') {
        clearInterval(this.polling)
        this.checkReviewCnt()
        this.countTime()
      } else if (this.$route.path !== '/') {
        this.snackbar = false
        clearInterval(this.polling)
      }
    }
  }
}
</script>