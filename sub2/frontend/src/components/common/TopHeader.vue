<template>
  <div class="top-header">
    <div class="top-header-wrapper">
      <div class="homepage-title">
        <router-link to="/">
          <span class="link-text">Book U Love</span>
        </router-link>
        <span v-if="this.userName" class="login-user-name ml-2">({{ this.userName }}<span class="greeting">님 환영합니다</span>)</span>
      </div>
      <div class="team-intro">
        <span class="link-text" @click.stop="toggleDialog">Introduction</span>
      </div>
    </div>
    <v-dialog v-model="showDialog" width="900">
      <v-card>
        <v-card-title>
          <strong class="team-name">Introduction</strong>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <div class="intro-contents">
            <div class="service-intro pb-4">
              <div class="intro-title">✔️서비스 소개</div>
              <div class="service-contents">
                <ul>
                  <li>도서 추천 서비스</li>
                  <li>유저의 정보를 바탕으로 맞춤 도서를 추천해드립니다.</li>
                </ul>
              </div>
            </div>
            <div class="team-intro">
              <div class="intro-title">✔️'다뭉비싸' 팀 소개</div>
              <div class="team-contents">
                <ul>
                  <li>이승열 : Merge</li>
                  <li>심규현 : Frontend 한땀한땀 장인</li>
                  <li>김아현 : Frontend 디자이너</li>
                  <li>박태수 : Backend 정보 수집가</li>
                  <li>이병주 : Backend 분석가</li>
                </ul>
              </div>
            </div>
          </div>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="warning" @click.stop="toggleDialog" :style="{ fontFamily: 'Noto Sans KR', fontSize: '12px' }" small>닫기</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data() {
    return {
      showDialog: false
    }
  },
  computed: {
    ...mapGetters(['userName'])
  },
  methods: {
    toggleDialog() {
      this.showDialog = !this.showDialog
    }
  }
}
</script>

<style scoped>
.v-application a {
  text-decoration: none;
  color: black;
}

.top-header {
  background-color: black;
}

.top-header-wrapper {
  display: flex;
  justify-content: space-between;
  width: 90%;
  margin: 0 auto;
  padding: 0.2em 0;
}

.link-text,
.login-user-name {
  font-family: 'Sarabun';
  color: white;
}

.login-user-name {
  font-size: 0.9em;
}

.homepage-title .link-text {
  font-size: 1.3em;
}

.team-intro .link-text {
  line-height: 2.05em;
}

.link-text:hover {
  cursor: pointer;
}

/* Introduction dialog style */
.team-name { 
  font-size: 1.2em;
  font-weight: 600;
  font-family: 'Quicksand';
  text-shadow: 3px 6px 6px rgba(0, 0, 0, .1);
}

.intro-contents div[class$='-title'] {
  font-size: 1.1em;
  font-weight: 600;
  font-family: 'Nanum Coding';
  color: black;
  padding-bottom: 0.25em;
}

.intro-contents div[class$='-contents'] > ul {
  list-style: disc;
}

.intro-contents div[class$='-contents'] > ul > li {
  padding-bottom: 3px;
}

@media (max-width: 405px) {
  .login-user-name .greeting {
    display: none;
  }
}
</style>