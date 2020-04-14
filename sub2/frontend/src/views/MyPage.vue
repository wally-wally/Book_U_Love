<template>
  <div class="mypage-wrapper">
    <MyPageSidebar />
    <router-view />
  </div>
</template>

<script>
import MyPageSidebar from '@/components/MyPage/MyPageSidebar'

export default {
  components: {
    MyPageSidebar
  }
}
</script>

<style scoped>
.mypage-wrapper {
  display: flex;
  justify-content: stretch;
  width: 90%;
  height: 100%;
  margin: 1em auto;
}

@media (max-width: 900px) {
  .mypage-wrapper {
    display: block;
  }
}
</style>