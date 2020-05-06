<template>
  <div>
    <div class="sidebar-wrapper">
      <div class="mypage-title">
        <div class="user-name">{{ info.username }}님의</div>
        <div @click="goMyPageMain()">MY PAGE</div>
      </div>
      <div class="mypage-menu">
        <ul>
          <router-link to="/myinfo/dashboard">
            <li class="first-elem"><i class="fas fa-columns"></i>Dashboard</li>
          </router-link>
          <router-link to="/myinfo/mybooks">
            <li><i class="fas fa-book"></i>My Books</li>
          </router-link>
          <router-link to="/myinfo/account">
            <li><i class="fas fa-user"></i>Account</li>
          </router-link>
          <router-link to="/admin/users" v-if="this.info.user_id <= 4">
            <li><i class="fas fa-tools"></i>Admin Page</li>
          </router-link>
        </ul>
      </div>
    </div>
    <div class="mobile-sidebar-wrapper">
      <div class="mobile-mypage-title">
        <span class="user-name">{{ info.username }}님의 </span>
        <span @click="goMyPageMain()">MY PAGE</span>
      </div>
      <div class="mobile-mypage-menu">
        <v-select
        v-model="selectMenu"
        class="d-inline-block ma-0 pa-0"
        color="warning"
        :items="menus"
        label="메뉴를 선택하세요."
        ></v-select>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data() {
    return {
      menus: ['Dashboard', 'My Books', 'Account'],
      selectMenu: ''
    }
  },
  computed: {
    ...mapGetters(['info'])
  },
  created() {
    if (this.info.user_id <= 4) {
      this.menus.push('Admin Page')
    }
  },
  methods: {
    goMyPageMain() {
      this.selectMenu = ''
      this.$router.push('/myinfo')
    }
  },
  watch: {
    selectMenu() {
      if (this.selectMenu !== '') {
        let routeUrls = ['/myinfo/dashboard', '/myinfo/mybooks', '/myinfo/account', '/admin/users']
        let idx = this.menus.indexOf(this.selectMenu)
        this.$router.push(routeUrls[idx])
      }
    },
    '$route'() {
      switch (this.$route.name) {
        case 'MyDashBoard':
          this.selectMenu = 'Dashboard'
          break
        case 'MyBooks':
          this.selectMenu = 'My Books'
          break
        case 'Account':
          this.selectMenu = 'Account'
          break
        default:
          this.selectMenu = ''
          break
      }
    }
  }
}
</script>

<style scoped>
.sidebar-wrapper {
  min-width: 200px;
}

.mypage-title,
.mobile-sidebar-wrapper > .mobile-mypage-title {
  font-weight: 600;
  font-size: 1.7em;
  font-family: 'Noto Sans KR';
  text-align: center;
}

.mobile-sidebar-wrapper > .mobile-mypage-title {
  font-size: 1.4em;
}

.mypage-title div:last-child:hover {
  cursor: pointer;
}

.mypage-menu {
  margin-top: 1em;
}

.mypage-menu ul {
  padding: 0;
  margin: 0;
  list-style: none;
}

.mypage-menu ul li {
  font-size: 1.05em;
  padding: 0.7em 0;
  border-bottom: 0.8px solid silver;
}

.mypage-menu ul a { /* router-link color 속성 제거 */
  color: black;
}

.mypage-menu ul li[class="first-elem"] {
  border-top: 0.8px solid silver;
}

.mypage-menu ul li:hover {
  background: rgba(0, 0, 0, 0.08);
  cursor: pointer;
}

.mypage-menu ul li i {
  padding-right: 0.25em;
}

.mobile-sidebar-wrapper {
  display: none;
}

.mobile-mypage-title span:last-child:hover {
  cursor: pointer;
}

.mobile-mypage-menu {
  width: 200px;
}

@media (max-width: 900px) {
  .mobile-sidebar-wrapper {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    padding-bottom: 1em;
    margin-bottom: 1em;
    border-bottom: 1px solid silver;
  }

  .sidebar-wrapper {
    display: none;
  }
}

@media (max-width: 550px) {
  .mobile-sidebar-wrapper {
    padding-bottom: 0;
  }
}
</style>
