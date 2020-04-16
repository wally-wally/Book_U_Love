<template>
  <v-app id="app">
    <Header />
      <v-content :style="headerStyle" :class="className">
        <router-view />
      </v-content>
    <Footer />
  </v-app>
</template>

<script>
import Header from '@/components/common/Header';
import Footer from '@/components/common/Footer';

export default {
  components: {
    Header,
    Footer
  },
  data() {
    return {
      headerStyle: ''
    }
  },
  computed: {
    className() {
      return this.$store.state.common.onMobileDrawer ? 'blind' : ''
    }
  },
  created() {
    this.responsiveHeaderHeight()
  },
  mounted() {
     window.addEventListener('resize', () => {
      this.responsiveHeaderHeight()
    })
  },
  methods: {
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
</style>
