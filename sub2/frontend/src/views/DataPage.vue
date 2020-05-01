<template>
  <div class="wrapper">
    <nav class="github-nav">
      <ul>
        <li @click="goPage('/filtercategory')"><span :class="clickedUrl === '/filtercategory' ? 'on' : ''" id="github-info-menu">동년배 취향 분석</span></li>
        <li @click="goPage('/reviewcategory')"><span :class="clickedUrl === '/reviewcategory' ? 'on' : ''" id="github-repos-menu">카테고리별 전체 리뷰</span></li>
        <li @click="goPage('/weeklydata')"><span :class="clickedUrl === '/weeklydata' ? 'on' : ''" id="github-repos-menu">최근 1주일 간 상위 리뷰 데이터</span></li>
      </ul>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  data() {
    return {
      clickedUrl: ''
    }
  },
  methods: {
    goPage(url) {
      this.$router.push(`/tmi${url}`)
      this.clickedUrl = url
    }
  }
}
</script>

<style scoped>
.wrapper {
  width: 80%;
  margin: 0 auto;
}

.github-nav ul {
  list-style-type: none;
  display: flex;
  height: 58px;
  padding: 0;
  border-bottom: 1px solid #f7b157;
}

.github-nav ul li {
  flex: 1;
}

.github-nav ul li:hover {
  cursor: pointer;
}

.github-nav ul li:first-child span {
  border-left: 1px solid #ddd;
}

.github-nav ul li span {
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

.github-nav ul li span.on {
  position: relatvie;
  height: 58px;
  border-color: #f7b157;
  border-top-width: 2px;
  line-height: 57px;
  border-bottom: 1px solid #fff;
}

.github-nav ul li span.on::before {
  content: '';
  position: absolute;
  left: -1px;
  top: -2px;
  width: 1px;
  height: 100%;
  background: #ffc837;
  border-top: 2px solid #f7b157;
}

@media (max-width: 750px) {
  .github-nav ul li span {
    font-size: 2.2vw;
  }
}
</style>