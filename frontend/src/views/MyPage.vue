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
  display: grid;
  grid-template-columns: 200px auto;
  gap: 20px;
  width: 80%;
  height: 100%;
  margin: 1em auto 4em;
}

@media (max-width: 900px) {
  .mypage-wrapper {
    display: block;
  }
}

@media (max-width: 600px) {
  .mypage-wrapper {
    width: 90%;
  }
}
</style>