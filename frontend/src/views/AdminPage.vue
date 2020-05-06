<template>
  <div class="admin-page-wrapper">
    <div class="menus">
      <div :class="this.$route.name === 'AdminPageUsers' ? 'now-page' : ''" @click="goPage('users')">Users</div>
      <div :class="this.$route.name === 'AdminPageBooks' ? 'now-page' : ''" @click="goPage('books')">Books</div>
    </div>
    <h2>Admin Page</h2>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'AdminPage',
  methods: {
    goPage(url) {
      this.$router.push(`/admin/${url}`)
    }
  }
}
</script>

<style scoped>
.admin-page-wrapper {
  width: 80%;
  margin: 0 auto;
}

.admin-page-wrapper h2 {
  font-family: 'Quicksand';
  padding-bottom: 8px;
}

.menus {
  position: fixed;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
}

.menus > div {
  font-family: 'Nanum Gothic';
  font-size: 15px;
  text-align: center;
  padding: 6px 12px;
  border: 0.5px solid silver;
  transition: all .15s;
}

.menus > div:hover {
  cursor: pointer;
  font-weight: 600;
  background-color: ivory;
}

.menus {
  border: 1px solid silver;
  box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.12);
}

.menus > div.now-page {
  font-weight: 600;
  background-color: ivory;
}
</style>