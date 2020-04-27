<template>
  <v-app id="app" :class="this.postLoading ? 'all-wrapper' : ''">
    <div :class="this.postLoading ? 'background-black' : ''"></div>
    <div :class="this.postLoading ? 'loader' : ''"></div>
    <span :class="this.postLoading ? 'loading-alert' : ''"></span>
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
import { mapState } from 'vuex'
import Header from '@/components/common/Header'
import Footer from '@/components/common/Footer'
import AlertCollectReview from '@/components/common/AlertCollectReview'
import '@/assets/css/loader.css'

export default {
  components: {
    Header,
    Footer,
    AlertCollectReview
  },
  data() {
    return {
      headerStyle: ''
    }
  },
  computed: {
    ...mapState({
      postLoading: state => state.data.postReviewLoading
    }),
    className() {
      return this.$store.state.common.onMobileDrawer ? 'blind' : ''
    }
  },
  created() {
    this.getCategory()
    this.responsiveHeaderHeight()
  },
  mounted() {
     window.addEventListener('resize', () => {
      this.responsiveHeaderHeight()
    })
  },
  methods: {
    async getCategory() {
      await this.$store.dispatch('GET_CATEGORIES')
    },
    responsiveHeaderHeight() {
      let height = window.innerWidth >= 550 ? 113.344 : 141.797
      this.headerStyle = `padding-top: ${height}px;`
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
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
