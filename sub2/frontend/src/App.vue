<template>
  <v-app id="app">
    <Header />
      <v-content :style="headerHeight" :class="className">
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
  computed: {
    headerHeight() {
      let height = window.innerWidth >= 550 ? 113.344 : 141.797
      return `padding-top: ${height}px;`
    },
    className() {
      return this.$store.state.common.onMobileDrawer ? 'blind' : ''
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