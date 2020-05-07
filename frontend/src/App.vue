<template>
  <v-app id="app" :class="this.postLoading ? 'all-wrapper' : ''">
    <transition name="fade" mode="in-out">
      <YoutubeVideoDialog v-if="this.showYoutubeVideo"></YoutubeVideoDialog>
    </transition>
    <ExplorerAlert :dialog="dialog" @closeDialog="closeDialog"></ExplorerAlert>
    <div :class="this.postLoading ? 'background-black' : ''"></div>
    <div :class="this.postLoading ? 'loader' : ''"></div>
    <span :class="this.postLoading ? 'loading-alert' : ''"></span>
    <div :class="this.postLoading && this.fetchAllBookStatus ? 'progress' : ''">
      진행률 : {{ this.progressRate }}[%]
    </div>
    <Header />
      <v-content :style="headerStyle" :class="className">
        <transition name="fade">
          <router-view />
        </transition>
        <AlertCollectReview />
      </v-content>
    <Footer />
  </v-app>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import Header from '@/components/common/Header'
import Footer from '@/components/common/Footer'
import ExplorerAlert from '@/components/common/ExplorerAlert.vue'
import AlertCollectReview from '@/components/common/AlertCollectReview'
import YoutubeVideoDialog from '@/components/Main/YoutubeVideoDialog.vue'
import '@/assets/css/loader.css'

export default {
  components: {
    Header,
    Footer,
    ExplorerAlert,
    AlertCollectReview,
    YoutubeVideoDialog
  },
  data() {
    return {
      headerStyle: '',
      dialog: false
    }
  },
  computed: {
    ...mapState({
      postLoading: state => state.data.postReviewLoading,
      fetchAllBookStatus: state => state.data.fetchAllBookStatus,
      allBooks: state => state.data.allBooks,
      allBooksCount: state => state.data.allBooksCount,
      showYoutubeVideo: state => state.common.showYoutubeVideo
    }),
    className() {
      return this.$store.state.common.onMobileDrawer ? 'blind' : ''
    },
    ...mapGetters(['progressRate'])
  },
  created() {
    this.getCategory()
    this.responsiveHeaderHeight()
  },
  mounted() {
    let agent = navigator.userAgent.toLowerCase()
    if ((navigator.appName == 'Netscape' && navigator.userAgent.search('Trident') != -1) || (agent.indexOf("msie") != -1)) {
      this.dialog = true
    } else {
      this.closeDialog()
    }
     window.addEventListener('resize', () => {
      this.responsiveHeaderHeight()
    })
  },
  methods: {
    async getCategory() {
      await this.$store.dispatch('GET_CATEGORIES')
    },
    responsiveHeaderHeight() {
      let height = window.innerWidth >= 620 ? 113.344 : 141.797
      this.headerStyle = `padding-top: ${height}px;`
    },
    closeDialog() {
      this.dialog = false
    }
  }
};
</script>

<style>
*:focus {
  outline: none;
}

a,
.v-application a,
.router-link-active,
.router-link-exact-active {
  text-decoration:none;
  color: black;
}
.blind {
  pointer-events: none;
  touch-action:none;
  overflow: hidden;
  background-color:rgb(33, 33, 33);
  border-color: rgb(33, 33, 33);
  opacity: 0.46;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .1s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
