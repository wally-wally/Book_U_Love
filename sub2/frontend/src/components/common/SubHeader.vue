<template>
  <div style="background: #fafafa;">
    <div class="sub-header" :id="this.showCategory ? 'ext' : ''">
      <div class="sub-header-wrapper">
        <div class="sub-header-left">
          <div class="service-logo">
            <img src="../../assets/images/team_logo/books.png" alt="service-logo">
          </div>
          <nav class="book-category-wrapper">
            <ul @click.stop="showAllCategory()">
              <li class="korea-category-tab">
                <span>
                  <i class="fas fa-caret-down ml-2"></i>
                </span>
                <div class="category-list-wrapper" :id="!this.showCategory ? 'list-hide' : ''">
                  <ul class="category-list">
                    <li v-for="category in koreaCategories.slice(0, 14)" :key="category.id" @click="goCategoryPage(category.id)">
                      {{ category.name | showAllText }}
                    </li>
                  </ul>
                </div>
                <div class="category-list-wrapper" :id="!this.showCategory ? 'list-hide' : ''">
                  <ul class="category-list">
                    <li v-for="category in koreaCategories.slice(15)" :key="category.id" @click="goCategoryPage(category.id)">
                      {{ category.name | showAllText }}
                    </li>
                  </ul>
                </div>
              </li>
              <li class="foreign-category-tab">
                <span>
                  <i class="fas fa-caret-down ml-2"></i>
                </span>
                <div class="category-list-wrapper" :id="!this.showCategory ? 'list-hide' : ''">
                  <ul class="category-list">
                    <li v-for="category in foreignCategories" :key="category.id" @click="goCategoryPage(category.id)">
                      {{ category.name | showAllText }}
                    </li>
                  </ul>
                </div>
              </li>
            </ul>
          </nav>
        </div>
        <div class="sub-header-right">
          <nav class="sub-header-right-wrapper">
            <div class="input-box">
              <form @submit.prevent="searchPage">
                <input class="keyword-input" type="text" v-model="searchKeyword" placeholder="검색 키워드를 작성해주세요.">
                <button><i class="fas fa-search mr-0"></i></button>
              </form>
            </div>
            <div class="icon-groups">
              <router-link v-if="isLogin" to="/myinfo" class="mr-3">
                <span>My Page</span>
              </router-link>
              <router-link v-if="!isLogin" to="/login" class="mr-3">
                <span>Login</span>
              </router-link>
              <span v-else class="mr-3 logout-btn" @click="logout">Logout</span>
              <i class="fas fa-bars" @click.stop="showDrawer()"></i>
            </div>
          </nav>
        </div>
      </div>
    </div>
    <v-navigation-drawer v-model="onDrawer" absolute temporary class="v-navigation-drawer--fixed">
      <v-list>
        <v-list-item>
          <v-list-item-title style="font-family: 'M PLUS Rounded 1c'; font-weight: bold;">Category</v-list-item-title>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>
      <v-list dense class="py-1">
        <v-list-item class="mobile-menu-list-item">
          <v-list-item-icon class="my-3 mr-1">
            <v-icon class="fas fa-dice-one" small></v-icon>
          </v-list-item-icon>
          <v-list-item-content class="mobile-menu-title">
            <v-list-item-title>
              <span class="region-title" @click="showKoreaCategoryList = !showKoreaCategoryList">국내도서<i class="fas fa-caret-down ml-2"></i></span>
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <div class="korea-book-category" v-if="showKoreaCategoryList">
          <ul>
            <li v-for="category in koreaCategories" :key="category.id" @click="goCategoryPage(category.id)">
              {{ category.name | showAllText }}
            </li>
          </ul>
        </div>
      </v-list>
      <v-list dense class="py-1">
        <v-list-item class="mobile-menu-list-item">
          <v-list-item-icon class="my-3 mr-1">
            <v-icon class="fas fa-dice-two" small></v-icon>
          </v-list-item-icon>
          <v-list-item-content class="mobile-menu-title">
            <v-list-item-title>
              <span class="region-title" @click="showForeignCategoryList = !showForeignCategoryList">외국도서<i class="fas fa-caret-down ml-2"></i></span>
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <div class="foreign-book-category" v-if="showForeignCategoryList">
          <ul>
            <li v-for="category in foreignCategories" :key="category.id" @click="goCategoryPage(category.id)">
              {{ category.name | showAllText }}
            </li>
          </ul>
        </div>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data() {
    return {
      onKoreaCategory: false,
      onForeignCategory: false,
      searchKeyword: '',
      onDrawer: false,
      showCategory: false,
      showKoreaCategoryList: false,
      showForeignCategoryList: false,
      subHeaderBoxShadow: '3px 5px 5px rgba(0, 0, 0, 0.1)'
    }
  },
  computed: {
    ...mapState({
      isLogin: state => state.user.isLogin,
    }),
    koreaCategories() {
      let categoryList = this.$store.state.data.categories
      return categoryList.filter(data => data.name.slice(0, 2) === '국내')
    },
    foreignCategories() {
      let categoryList = this.$store.state.data.categories
      return categoryList.filter(data => data.name.slice(0, 2) === '외국')
    },
  },
  mounted() {
    window.addEventListener('resize', () => {
      if (window.innerWidth <= 970) {
        this.showCategory = false
      } else {
        this.closeDrawerCategoryList()
        this.onDrawer = false
      }
    })
    window.addEventListener('scroll', () => {
      this.toggleSubHeaderShadow()
      if (this.showCategory) {
        this.showCategory = false
      }
    })
  },
  methods: {
    showAllCategory() {
      this.showCategory = !this.showCategory
      this.toggleSubHeaderShadow()
    },
    toggleSubHeaderShadow() {
      document.querySelector('.sub-header').style.boxShadow = this.showCategory || document.documentElement.scrollTop >= 180 ? this.subHeaderBoxShadow : ''
    },
    showDrawer() {
      this.onDrawer = !this.onDrawer
    },
    closeDrawerCategoryList() {
      this.showKoreaCategoryList = false
      this.showForeignCategoryList = false
    },
    goCategoryPage(categoryID) {
      this.$router.push(`/category/${categoryID}`)
    },
    searchPage() {
      if (this.searchKeyword) {
        this.$router.push(`/search/${this.searchKeyword}`)
      } else {
        alert('최소 1자 이상 키워드를 입력해주세요.')
      }
    },
    logout() {
      if (confirm('정말로 로그아웃하시겠습니까?')) {
        this.$store.commit('logout')
        this.$router.push('/')
      }
    }
  },
  filters: {
    showAllText(name) {
      return name.length === 4 ? `${name} 전체보기` : name.split('>')[1]
    }
  },
  watch: {
    onDrawer: {
      handler(newVal, oldVal) {
        this.$store.commit('showDrawer', this.onDrawer)
        if (!newVal && oldVal) {
          this.closeDrawerCategoryList()
        }
      }
    },
    '$route' (to, from) {
      if (to.path !== from.path) {
        setTimeout(() => {
          this.showCategory = false
          document.querySelector('.sub-header').style.boxShadow = ''
        }, 0)
      }
      if (to.name !== 'search') {
        this.searchKeyword = ''
      }
    }
  }
}
</script>

<style scoped>
.v-application a {
  text-decoration: none;
  color: black;
}

.sub-header {
  position: relative;
  padding: 0.3em 0;
  height: auto;
}

#ext {
  height: 450px;
}

.sub-header-wrapper {
  display: flex;
  justify-content: space-between;
  width: 90%;
  margin: 0 auto;
  padding: 0.2em 0;
}

.service-logo,
.book-category-wrapper {
  display: inline-block;
}

.service-logo img {
  width: 60px;
  vertical-align: middle;
}

.book-category-wrapper {
  margin-left: 1.5em;
  vertical-align: middle;
}

.book-category-wrapper > ul {
  list-style: none;
  margin-left: 1rem;
  padding: 0;
}

.book-category-wrapper > ul > li {
  float: left;
}

.book-category-wrapper > ul > li:not(:last-child) {
  float: left;
  margin-right: 12rem;
}

.book-category-wrapper > ul > li > span {
  font-size: 1.02em;
  font-family: 'Gothic A1';
  font-weight: 600;
  position: relative;
}

.book-category-wrapper > ul > li > .category-list-wrapper {
  position: absolute;
  top: 70px;
  font-size: 0.9em;
}

.book-category-wrapper > ul > li[class="korea-category-tab"] > .category-list-wrapper:last-child {
  display: inline;
  margin-left: 50px;
}

.book-category-wrapper > ul > li > .category-list-wrapper > ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.book-category-wrapper > ul > li .category-list-wrapper > ul > li {
  padding: 0.15em 0.6em 0.15em 0;
  font-family: 'Noto Sans KR';
  border-bottom: 0.8px solid #ccc;
}

.book-category-wrapper > ul > li .category-list-wrapper > ul > li:first-child {
  border-top: 0.8px solid #ccc;
}

.book-category-wrapper > ul > li .category-list-wrapper > ul > li:hover {
  cursor: pointer;
  background: rgba(0, 0, 0, .05);
}

.korea-category-tab ul[class="category-list"] {
  display: inline;
}

.book-category-wrapper > ul > li > span:hover {
  cursor: pointer;
  color: #F1AF4D;
}

.book-category-wrapper ul li:first-child span::before {
  content: '국내도서'
}

.book-category-wrapper ul li:last-child span::before {
  content: '외국도서'
}

.sub-header-right-wrapper {
  font-size: 1.01em;
  font-family: 'Gothic A1';
  line-height: 3.7em;
}

.sub-header-right-wrapper form {
  display: inline;
}

.sub-header-right input {
  border: 1px solid lightgray;
  border-radius: 10px;
  box-shadow: 3px 5px 5px rgba(0, 0, 0, .05);
  margin-right: 0.4em;
  height: 22px;
  width: 20vw;
  padding: 5px;
}

.input-box,
.icon-groups {
  display: inline;
  padding-left: 10px;
}

.input-box input {
  font-size: 0.92em;
}

.input-box button > i {
  line-height: 1.4;
}

.icon-groups button > i:hover,
.input-box button > i:hover,
.icon-groups .logout-btn:hover {
  cursor: pointer;
}

.icon-groups span {
  padding: 0.4em;
  border: 0.5px solid lightgray;
  border-radius: 8px;
  box-shadow: 3px 5px 5px rgba(0, 0, 0, .05);
  color: #12337A;
  font-weight: lighter;
}

.icon-groups span:hover {
  background-color: #DEE4F1;
  transition: background-color .3s linear;
}

.fa-bars {
  display: none;
}

#list-hide {
  visibility: hidden;
}

/* When mobile size, navigation-drawer */
aside {
  z-index: 50000;
}

aside ul {
  list-style: none;
}

aside ul > li {
  padding: 0.35em 0;
  font-size: 0.9em;
  border-bottom: 0.8px solid rgba(0, 0, 0, .1);
  width: 90%;
  font-family: 'Nanum Gothic';
}

aside ul > li:first-child {
  border-top: 0.8px solid rgba(0, 0, 0, .1);
}

aside .region-title {
  font-size: 1rem;
  font-weight: bold;
  font-family: 'Gothic A1';
}

/* responsive web */
@media (min-width: 550px) and (max-width: 970px) {
  .sub-header-wrapper {
    display: block;
  }

  .sub-header-left {
    display: none;
  }

  .sub-header-right-wrapper {
    display: flex;
    justify-content: space-between;
  }

  .fa-bars {
    display: inline;
  }

  .input-box {
    display: inline-block;
    width: 60%;
  }

  .input-box > a {
    line-height: 1.5em;
  }

  .input-box input {
    width: 80%;
  }
}

@media (max-width: 549px) {
  .sub-header-wrapper {
    display: block;
  }

  .sub-header-left {
    display: none;
  }

  .icon-groups {
    display: block;
    text-align: right;
    padding: 0;
  }

  .fa-bars {
    display: inline;
  }

  .input-box {
    display: block;
    padding: 0.4em 0 0;
  }

  .input-box form {
    display: flex;
    justify-content: space-between;
  }

  .input-box button {
    line-height: 1;
  }

  .input-box input {
    width: 100%;
  }
}
</style>
