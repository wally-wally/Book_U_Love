<template>
  <div style="position: fixed; width: 100%; z-index:10000;">
    <TopHeader/>
    <SubHeader />
    <transition name="fade">
      <v-speed-dial v-if="fab && !this.$store.state.common.onMobileDrawer" class="go-top-button" :bottom="true" :right="true" fixed>
        <template v-slot:activator>
          <a href="#">
            <v-btn color="#ECECE0" fab>
              <v-icon class="fas fa-arrow-up" dark></v-icon>
            </v-btn>
          </a>
        </template>
      </v-speed-dial>
    </transition>
  </div>
</template>

<script>
import TopHeader from '@/components/common/TopHeader'
import SubHeader from '@/components/common/SubHeader'

export default {
  components: {
    TopHeader,
    SubHeader
  },
  data() {
    return {
      fab: false,
      drawerStatus: false
    }
  },
  created() {
    this.getCategory()
    window.addEventListener('scroll', () => {
      let scrollHegiht = document.scrollingElement.scrollTop
      this.fab = scrollHegiht >= 180
    })
  },
  methods: {
    async getCategory() {
      await this.$store.dispatch('GET_CATEGORIES')
    }
  }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity .2s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>