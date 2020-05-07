<template>
  <div style="background: #fafafa;">
    <div class="sub-header">
      <div class="sub-header-wrapper">
        <div class="sub-header-left">
          <div class="service-logo">
            <router-link to="/">
              <img src="../../assets/images/team_logo/books.png" alt="service-logo">
            </router-link>
          </div>
          <nav class="book-category-wrapper">
            <ul>
              <li class="category-tab">
                <span><i class="fas fa-caret-down ml-2"></i></span>
                <ul class="main-category">
                  <li class="main-category-item" v-for="category in this.categoryList" :key="category.name">
                    <div class="main-category-name" @click="goCategoryPage('main', category.id)">
                      {{ category.name }}
                      <i class="fas fa-chevron-right" v-if="category.subcategory_set.length" />
                    </div>
                    <ul class="sub-category" v-if="category.subcategory_set.length">
                      <li class="sub-category-item" v-for="subcategory in category.subcategory_set" :key="subcategory.name">
                        <div class="sub-category-name" @click="goCategoryPage('sub', subcategory.id)">
                          {{ subcategory.name }}
                          <i class="fas fa-chevron-right pl-1" v-if="subcategory.detailcategory_set.length"/>
                        </div>
                        <ul class="detail-category" v-if="subcategory.detailcategory_set.length">
                          <li class="detail-category-item" v-for="detailcategory in subcategory.detailcategory_set" :key="detailcategory.name">
                            <div class="detail-category-name" @click="goCategoryPage('detail', detailcategory.id)">{{ detailcategory.name }}</div>
                          </li>
                        </ul>
                      </li>
                    </ul>
                  </li>
                </ul>
              </li>
              <li class="category-sub">
                <span class="tmi-center" @click="goTMI">TMI CENTER</span>
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
              <span v-else class="logout-btn" @click="logout">Logout</span>
              <i class="fas fa-bars" @click.stop="showDrawer()"></i>
            </div>
          </nav>
        </div>
      </div>
    </div>
    <v-navigation-drawer v-model="onDrawer" absolute temporary class="v-navigation-drawer--fixed">
      <v-list>
        <v-list-item @click="goTMI">
          <v-list-item-title style="font-family: 'M PLUS Rounded 1c'; font-weight: bold;">📈 TMI Center</v-list-item-title>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>
      <v-list>
        <v-list-item>
          <v-list-item-title style="font-family: 'M PLUS Rounded 1c'; font-weight: bold;">Category</v-list-item-title>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>
      <v-list dense>
        <v-list-group ref="main-list" v-for="category in this.categoryList" :key="category.name" no-action>
          <template v-slot:activator>
            <v-list-item-title class="d-flex justify-space-between">
              <div class="mobile-category-name">{{ category.name }}</div>
              <div class="mobile-category-link" @click="goCategoryPage('main', category.id)"><i class="fas fa-external-link-alt"></i></div>
            </v-list-item-title>
          </template>
          <div v-if="category.subcategory_set.length">
            <v-list-group sub-group v-for="subcategory in category.subcategory_set" :key="subcategory.name" :prepend-icon="subcategory.detailcategory_set.length ? 'mdi-menu-down' : ' '">
              <template v-slot:activator>
                <v-list-item-content v-if="subcategory.detailcategory_set.length">
                  <v-list-item-title class="d-flex justify-space-between">
                    <div class="mobile-category-name">{{ subcategory.name }}</div>
                    <div class="mobile-category-link" @click="goCategoryPage('sub', subcategory.id)"><i class="fas fa-external-link-alt"></i></div>
                  </v-list-item-title>
                </v-list-item-content>
                <v-list-item-title v-else>
                  <div class="mobile-category-name" @click="goCategoryPage('sub', subcategory.id)">{{ subcategory.name }}</div>
                </v-list-item-title>
              </template>
              <div v-if="subcategory.detailcategory_set.length">
                <v-list-item v-for="detailcategory in subcategory.detailcategory_set" :key="detailcategory.name" link @click="goCategoryPage('detail', detailcategory.id)">
                  <v-list-item-title :style="{ 'fontSize': '13px' }">{{ detailcategory.name }}</v-list-item-title>
                </v-list-item>
              </div>
            </v-list-group>
          </div>
        </v-list-group>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { fetchCategories } from '@/api/index.js'
export default {
  data() {
    return {
      searchKeyword: '',
      onDrawer: false,
      subHeaderBoxShadow: '3px 5px 5px rgba(0, 0, 0, 0.1)',
      c_setting : [null,null,null],
    }
  },
  computed: {
    ...mapState({
      isLogin: state => state.user.isLogin,
      categoryList: state => state.data.categories
    })
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
    })
  },
  methods: {
    maincategory(tmp){
      this.showAllCategory()
      this.c_setting = [tmp,null,null]
    },
    subcategory(tmp){
      this.showAllCategory()
      this.c_setting[1] = tmp
      this.c_setting[2] = null
    },
    detailcategory(tmp){
      this.c_setting[2] = tmp
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
    goCategoryPage(type,categoryID) {
      this.$router.push(`/category/${type}/${categoryID}`)
    },
    searchPage() {
      if (this.searchKeyword) {
        this.$store.commit('setSearchKeyword', this.searchKeyword)
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
    },
    goTMI() {
      this.$router.push('/tmi')
    }
  },
  watch: {
    onDrawer: {
      handler(newVal, oldVal) {
        this.$store.commit('showDrawer', this.onDrawer)
        if (!newVal && oldVal) {
          this.closeDrawerCategoryList()
          this.$refs['main-list'].forEach(function(component) {
            component.isActive = false
          })
        }
      }
    },
    '$route' (to, from) {
      this.closeDrawerCategoryList()
      if (to.name == 'MainPage') {
        this.c_setting = [null,null,null]
      }
      if (to.path !== from.path) {
        setTimeout(() => {
          this.showCategory = false
          document.querySelector('.sub-header').style.boxShadow = ''
        }, 0)
      }
      if (to.name !== 'search') {
        this.searchKeyword = ''
        this.$store.commit('setSearchKeyword', '')
      }
    }
  }
}
</script>

<style scoped>
li {
  list-style-type: none;
}

.v-application a {
  text-decoration: none;
  color: black;
}

.sub-header {
  position: relative;
  padding: 0.3em 0;
  height: auto;
}

.select {
  background-color:rgb(204, 205, 207);
}

.categoryname {
  display : inline-block;
  margin : 0.3em;
  font-size: 1.02em;
  font-family: 'Gothic A1';
  font-weight: 600;
}

.categoryname:hover,
i:hover,
.tmi-center:hover {
  cursor: pointer
}

.sub-header-wrapper {
  display: flex;
  justify-content: space-between;
  width: 80%;
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

/* ALL CATEGORY 메뉴 */
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
  margin-right: 1rem;
}

.book-category-wrapper > ul > li > span,
.tmi-center {
  font-size: 1.02em;
  font-family: 'Noto Sans KR';
  font-weight: 600;
}

.main-category {
  position: absolute;
  top: 100%;
  width: 140px;
  background-color: #fafafa;
  padding: 6px 0 6px 3px;
  box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.2);
  font-size: 14px;
  font-family: 'Gothic A1';
  opacity: 0;
  pointer-events: none;
  transition: all .2s;
}

.category-tab:not(.tmi-center):hover .main-category{
  opacity: 1;
  pointer-events: auto;
}

.main-category > li,
.sub-category > li,
.detail-category > li {
  padding: 3px 0;
}

.main-category > li:not(:last-child),
.sub-category > li:not(:last-child),
.detail-category > li:not(:last-child) {
  border-bottom: 0.5px solid silver;
}

.main-category:before {
  content: ' ';
  position: absolute;
  top: -25px;
  left: 0;
  right: 0;
  height: 25px;
}

.sub-category {
  position: absolute;
  top: 0;
  left: 100%;
  width: 140%;
  height: 671.5px;
  background-color: #fafafa;
  padding: 6px 0;
  box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.2);
  font-size: 14px;
  font-family: 'Gothic A1';
  opacity: 0;
  pointer-events: none;
  transition: all .2s;
}

.main-category-item:hover .sub-category{
  opacity: 1;
  pointer-events: auto;
}

.fa-chevron-right {
  visibility: hidden;
}

.main-category-item:hover .main-category-name > .fa-chevron-right {
  visibility: visible;
}

.sub-category-item:hover .sub-category-name > .fa-chevron-right {
  visibility: visible;
}

.detail-category {
  position: absolute;
  top: 0;
  left: 100%;
  width: 110%;
  height: 671.5px;
  background-color: #fafafa;
  padding: 6px 0;
  box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.2);
  font-size: 14px;
  font-family: 'Gothic A1';
  opacity: 0;
  pointer-events: none;
  transition: all .2s;
}

.sub-category-item:hover .detail-category{
  opacity: 1;
  pointer-events: auto;
}

.fa-chevron-right {
  padding-left: 3px;
}

.main-category-item:hover .main-category-name,
.sub-category-item:hover .sub-category-name,
.detail-category-item:hover .detail-category-name {
  color: darkgoldenrod;
  background-color: ivory;
  cursor: pointer;
}

.book-category-wrapper > ul > li > span:hover {
  cursor: pointer;
  color: #F1AF4D;
}

.book-category-wrapper ul li:first-child span:before {
  content: 'ALL CATEGORY'
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
.mobile-category-name {
  font-size: 13px;
  white-space: nowrap;
}

.mobile-category-link {
  font-size: 13px;
}

/* responsive web */
@media (max-width: 970px) {
  .icon-groups .logout-btn {
    margin-right: 12px;
  }
}

@media (min-width: 620px) and (max-width: 970px) {
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

@media (max-width: 619px) {
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

@media (max-width: 600px) {
  .sub-header-wrapper {
    width: 90%;
  }
}
</style>
