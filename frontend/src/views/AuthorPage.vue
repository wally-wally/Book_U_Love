<template>
  <div class="author">
    <router-view />
  </div>
</template>

<script>
export default {

}
</script>

<style scoped>
.author {
  width: 80%;
  margin: 0 auto;
}

@media (max-width: 600px) {
  .author {
    width: 90%;
  }
}
</style>