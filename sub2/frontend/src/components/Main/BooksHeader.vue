<template>
  <header>
    <div class="books-header-title">
      <span>Book List</span>
      <!-- <span class="category-btn" @click.stop="toggleDialog">(Select Category)</span> -->
    </div>
    <nav class="books-category">
      <ul class="desktop-size-header">
        <li v-for="theme in themes" :key="theme">
          <div>{{ theme }}</div>
        </li>
      </ul>
      <ul class="mobile-size-header">
        <i class="fas fa-bars" @click="showDrawer"></i>
        <div class="mobile-drawer" v-if="clickedDrawerIcon">
          <li v-for="theme in themes" :key="theme">
            <div>{{ theme }}</div>
          </li>
        </div>
      </ul>
    </nav>
    <v-dialog v-model="showDialog" width="900" persistent>
      <v-card>
        <v-card-title>
          <strong class="team-name">카테고리 선택</strong>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <div class="team-intro-contents">
            <ul>
              <li v-for="category in categories" :key="category.id" class="mb-2">
              <router-link :to="`/category/${category.id}`">
                <span>{{ category.id }}</span> | <span>{{ category.name }}</span>
              </router-link>
              </li>
            </ul>
          </div>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="warning" @click.stop="toggleDialog" :style="{ fontFamily: 'Noto Sans KR' }">닫기</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </header>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data() {
    return {
      themes: ['Best Sellers', 'Review TOP 100'],
      clickedDrawerIcon: false,
      showDialog: false
    }
  },
  computed: {
    ...mapState({
      categories: state => state.data.categories
    })
  },
  created() {
    this.getCategory()
  },
  mounted() {
    window.addEventListener('resize', () => {
      if (window.innerWidth > 550) {
        this.clickedDrawerIcon = false
      }
    })
  },
  methods: {
    async getCategory() {
      await this.$store.dispatch('GET_CATEGORIES')
    },
    showDrawer() {
      this.clickedDrawerIcon = !this.clickedDrawerIcon
    },
    toggleDialog() {
      this.showDialog = !this.showDialog
    }
  }
}
</script>

<style scoped>
header {
  position: relative;
  margin-bottom: 0.6em; 
}

header .books-header-title span {
  font-family: 'Julius Sans One';
  font-weight: 600;
}

header .books-header-title .category-btn {
  font-size: 0.95em;
}

header .books-header-title .category-btn:hover {
  cursor: pointer;
  font-weight: 900;
  text-shadow: 2px 4px 4px rgba(0, 0, 0, 0.08);
}

header .books-category {
  position: absolute;
  top: 0;
  right: 0;
  font-family: 'Chivo';
}

header .books-category ul {
  list-style: none;
}

header .books-category ul[class='desktop-size-header'] li{
  display: inline-block;
  margin: 0 0.5em;
}

header .books-category ul[class='desktop-size-header'] li:first-child {
  margin-left: 0;
}

header .books-category ul[class='desktop-size-header'] li:last-child {
  margin-right: 0;
}

header .books-category ul[class='desktop-size-header'] li div:hover {
  cursor: pointer;
  border-bottom: 1.5px solid darkslategrey;
}

header .books-category ul[class='mobile-size-header'] {
  display: none;
  position: relative;
}

header .books-category ul[class='mobile-size-header'] .mobile-drawer {
  position: absolute;
  right: 0;
  width: 130px;
  z-index: 10;
  background-color: #fff;
  border: 0.5px solid lightgray;
  border-radius: 5px;
  box-shadow: 3px 5px 5px rgba(0, 0, 0, 0.05);
}

header .books-category ul[class='mobile-size-header'] .mobile-drawer li {
  font-size: 0.95em;
  padding: 0.25em 0.4em;
}

@media (max-width: 900px) {
  header .books-category ul[class='desktop-size-header'] li{
    margin: 0 0.25em;
  }
}

@media (max-width: 550px) {
  header .books-category ul[class='desktop-size-header'] {
    display: none;
  }

  header .books-category ul[class='mobile-size-header'] {
    display: block;
  }
}
</style>