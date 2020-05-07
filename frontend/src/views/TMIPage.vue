<template>
  <div class="wrapper">
    <nav class="tmi-nav">
      <ul>
        <li @click="goPage('/weeklydata')"><span :class="clickedUrl === '/weeklydata' ? 'on' : ''" id="tmi-sub-menu">최근 1주일 간 상위 리뷰 데이터</span></li>
        <li @click="goPage('/filterbook')"><span :class="clickedUrl === '/filterbook' ? 'on' : ''" id="tmi-sub-menu">동년배 책 분석</span></li>
        <li @click="goPage('/filtercategory')"><span :class="clickedUrl === '/filtercategory' ? 'on' : ''" id="tmi-sub-menu">동년배 취향 분석</span></li>
        <li @click="goPage('/reviewcategory')"><span :class="clickedUrl === '/reviewcategory' ? 'on' : ''" id="tmi-sub-menu">카테고리별 전체 리뷰</span></li>
      </ul>
    </nav>
    <nav class="tmi-mobile-nav">
      <div class="tmi-mobile-title">
        <span>📈 TMI Center</span>
      </div>
      <div class="tmi-mobile-menu">
        <v-select
        v-model="selectMenu"
        class="d-inline-block ma-0 pa-0"
        color="warning"
        :items="menus"
        label="메뉴를 선택하세요."
        ></v-select>
      </div>
    </nav>
    <router-view class="mt-4" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      clickedUrl: '',
      selectMenu: '',
      menus: [
        '최근 1주일 간 상위 리뷰 데이터',
        '동년배 책 분석',
        '동년배 취향 분석',
        '카테고리별 전체 리뷰',
      ]
    }
  },
  methods: {
    goPage(url) {
      this.$router.push(`/tmi${url}`)
      this.clickedUrl = url
    }
  },
  watch: {
    '$route'() {
      switch (this.$route.name) {
        case 'TMI1':
          this.selectMenu = '최근 1주일 간 상위 리뷰 데이터'
          break
        case 'TMI2':
          this.selectMenu = '동년배 책 분석'
          break
        case 'TMI3':
          this.selectMenu = '동년배 취향 분석'
          break
        case 'TMI4':
          this.selectMenu = '카테고리별 전체 리뷰'
          break
        default:
          this.selectMenu = ''
      }
    },
    selectMenu() {
      switch (this.selectMenu) {
        case '동년배 취향 분석':
          this.goPage('/filtercategory')
          break
        case '동년배 책 분석':
          this.goPage('/filterbook')
          break
        case '카테고리별 전체 리뷰':
          this.goPage('/reviewcategory')
          break
        case '최근 1주일 간 상위 리뷰 데이터':
          this.goPage('/weeklydata')
          break
        default:
          this.goPage('')
      }
    }
  }
}
</script>

<style scoped>
.wrapper {
  width: 80%;
  margin: 0 auto;
}

.tmi-nav ul {
  list-style-type: none;
  display: flex;
  height: 58px;
  padding: 0;
  border-bottom: 1px solid #f7b157;
}

.tmi-nav ul li {
  flex: 1;
}

.tmi-nav ul li:hover {
  cursor: pointer;
}

.tmi-nav ul li:first-child span {
  border-left: 1px solid #ddd;
}

.tmi-nav ul li span {
  display: block;
  height: 59px;
  border: 1px solid #ddd;
  border-left: none;
  border-bottom: none;
  font-size: 16px;
  font-weight: 700;
  font-family: 'Stylish';
  color: #505050;
  text-align: center;
  line-height: 59px;
  text-decoration: none;
}

.tmi-nav ul li span.on {
  position: relatvie;
  height: 58px;
  border-color: #f7b157;
  border-top-width: 2px;
  line-height: 57px;
  border-bottom: 1px solid #fff;
}

.tmi-nav ul li span.on::before {
  content: '';
  position: absolute;
  left: -1px;
  top: -2px;
  width: 1px;
  height: 100%;
  background: #ffc837;
  border-top: 2px solid #f7b157;
}

.tmi-mobile-nav {
  display: none;
}

.tmi-mobile-nav .tmi-mobile-title {
  font-size: 1.4em;
  font-weight: 600;
  font-family: 'Noto Sans KR';
  padding-bottom: 20px;
}

@media (max-width: 900px) {
  .tmi-mobile-nav {
    display: block;
    height: 90px;
    margin-bottom: 10px;
  }

  .tmi-nav {
    display: none;
  }
}

@media (max-width: 750px) {
  .tmi-nav ul li span {
    font-size: 2.2vw;
  }
}

@media (max-width: 600px) {
  .wrapper {
    width: 90%;
  }
}
</style>