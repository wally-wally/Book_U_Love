<template>
  <footer id="footer">
    <div class="footer-title">
      <img src="https://user-images.githubusercontent.com/52685250/80765397-e5c09d80-8b7d-11ea-8193-7b61baa0345e.png" width="280">
    </div>
    <nav id="footer-menu-primary" class="footer-menu" style="width:60%; margin:0 auto;">
      <ul class="pl-0">
        <!-- <li id="menu-item-91" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-91"><span style="padding:30px;">About</span></li> -->
        <li id="menu-item-92" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-92" @click.stop="toggleDialog"><span style="padding:30px;">Information</span></li>
        <!-- <li id="menu-item-93" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-93"><span style="padding:30px;">Contact</span></li> -->
      </ul>
    </nav>
    <p class="copyright pt-3">Copyright ⓒ 2020 by <span class="editor" @click="goGitlab()">Damungbissa</span>. All rights reserved.</p>
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
  </footer>
</template>

<script>
export default {
  data() {
    return {
      showDialog: false
    }
  },
  methods: {
    goGitlab() {
      window.open('https://lab.ssafy.com/s02-bigdata-sub2/s02p22b205')
    },
    toggleDialog() {
      this.showDialog = !this.showDialog
    }
  }
}
</script>

<style scoped>
  /* .editor {
    color: #fff;
  } */
  .editor:hover {
    cursor: pointer;
  }
  #footer {
    position: relative;
    color: #7F7675;
    padding: 30px 0;
    background-color: #f6e9e6 ;
    text-align: center;
  }
  #footer .copyright {
    color: #7F7675;
    font-size: 14px;
    line-height: 28px;
    font-weight: 500;
  }
  #footer-menu-primary {
    border-bottom: 3px solid #DCCAC7;
  }
  .footer-menu {
      position: relative;
      padding: 15px 0;
  }
  li{
    list-style: none;
    /* display:inline-block; */
    font-size:14px;
    /* line-height: 15px; */
    font-weight: 500;
  }
  .footer-menu ul li:hover{
    position: relative;
    display: inline-block;
    bottom: 0;
    left: 0;
    right: 0;
    height: 2px;
    transform: translateY(2px);
    transition: .3s ease all;
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
</style>