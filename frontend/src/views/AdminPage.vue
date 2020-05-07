<template>
  <div class="admin-page-wrapper">
    <div class="menus">
      <div :class="this.$route.name === 'AdminPageUsers' ? 'now-page' : ''" @click="goPage('users')">Users</div>
      <div :class="this.$route.name === 'AdminPageBooks' ? 'now-page' : ''" @click="goPage('books')">Books</div>
    </div>
    <h2>🛠️ Admin Page</h2>
    <div class="mobile-menus">
      <v-select
      v-model="selectMenu"
      class="d-inline-block mx-0 mb-0 mt-2 pa-0"
      color="warning"
      :items="menus"
      label="메뉴를 선택하세요."
      ></v-select>
    </div>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'AdminPage',
  data() {
    return {
      selectMenu: 'Users',
      menus: ['Users', 'Books']
    }
  },
  methods: {
    goPage(url) {
      this.$router.push(`/admin/${url}`)
    }
  },
  watch: {
    '$route'() {
      switch (this.$route.name) {
        case 'AdminPageUsers':
          this.selectMenu = 'Users'
          break
        case 'AdminPageBooks':
          this.selectMenu = 'Books'
          break
      }
    },
    selectMenu() {
      switch (this.selectMenu) {
        case 'Users':
          this.goPage('users')
          break
        case 'Books':
          this.goPage('books')
          break
      }
    }
  }
}
</script>

<style scoped>
.admin-page-wrapper {
  width: 80%;
  margin: 1em auto 7em;
}

.admin-page-wrapper h2 {
  font-family: 'Quicksand';
  padding-bottom: 16px;
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

.mobile-menus {
  display: none;
}

@media (max-width: 850px) {
  .mobile-menus {
    display: block;
  }

  .menus {
    display: none;
  }
}

@media (max-width: 600px) {
  .admin-page-wrapper {
    width: 90%;
  }
}
</style>