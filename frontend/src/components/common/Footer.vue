<template>
  <footer id="footer">
    <div class="footer-title">
      <img src="../../assets/images/team_logo/logo.png" width="280">
    </div>
    <nav id="footer-menu-primary" class="footer-menu" style="width:60%; margin:0 auto;">
      <ul class="pl-0">
        <li id="menu-item-92" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-92" @click.stop="toggleDialog(0)"><span style="padding:30px;">Introduction</span></li>
        <li id="menu-item-93" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-93" @click.stop="toggleDialog(1)"><span style="padding:30px;">Team</span></li>
      </ul>
    </nav>
    <p class="copyright pt-3">Copyright ⓒ 2020 by <span class="editor" @click="goGitlab()">Damungbissa</span>. All rights reserved.</p>
    <v-dialog v-model="introDialog" width="900">
      <v-card>
        <v-card-title>
          <strong class="team-name">Book U Love Introduction</strong>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <div class="intro-contents">
            <div class="service-intro pb-4">
              <div class="intro-title">✔️서비스 소개</div>
              <img src="../../assets/images/team_logo/logo.png" alt="service-logo">
              <div class="service-contents">
                <div class="service-summery">
                  <i>읽고는 싶지만 무엇을 읽어야 할 지 모르겠다면!<br>
                  "이제 저희가 추천해드릴게요."<br>
                  빅데이터로 추천받는 맞춤 도서로 함께 교양 쌓아요<br>
                  도서 추천 서비스, 'Book_U_Love'</i>
                </div>
                <ul>
                  <li>📍 BOOK_U_LOVE 서비스는 유저 데이터를 기반으로 하여 협업필터링(Collaborative Filtering)을 이용해 유저별 맞춤 도서를 추천해주는 서비스이에요</li>
                  <li>📍 유저의 정보를 바탕으로 선호 성향이 비슷한 사용자들을 그룹화하여 동일 그룹 내에서 선호하는 도서를 추천하는 방식이에요</li>
                </ul>
                <hr class="my-3">
                <ul class="service-captures">
                  <li>
                    <p>📍 로그인 후 회원님에게 적합한 도서를 추천받아보세요</p>
                    <img :src="imgUrl('01')" alt="service-contents-1">
                  </li>
                  <li>
                    <p>📍 처음 로그인하거나 리뷰를 적게 작성한 회원님은 리뷰 데이터 수집 페이지를 통해 리뷰를 작성한 후 다양한 책들을 추천 받을 수 있어요</p>
                    <img :src="imgUrl('05')" alt="service-contents-1">
                  </li>
                  <li>
                    <p>📍 도서 뿐만 아니라 도서 추천 관련 Youtube 영상들도 볼 수 있어요.</p>
                    <img :src="imgUrl('02')" alt="service-contents-1">
                  </li>
                  <li>
                    <p>📍 도서 상세 정보와 리뷰는 당연히 볼 수 있고요</p>
                    <img :src="imgUrl('03')" alt="service-contents-1">
                  </li>
                  <li>
                    <p>📍 도서 빅데이터를 분석해서 동년배들이 선호하는 책들도 만나보세요.</p>
                    <img :src="imgUrl('04')" alt="service-contents-1">
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="warning" @click.stop="toggleDialog(0)" :style="{ fontFamily: 'Noto Sans KR', fontSize: '12px' }" small>닫기</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="teamDialog" width="900">
      <v-card>
        <v-card-title>
          <strong class="team-name">Team Introduction</strong>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <div class="intro-contents">
            <div class="service-intro pb-4">
              <div class="intro-title">✔️Book U Love 만든이들</div>
              <div class="team-contents">
                <img src="../../assets/images/members/teamintro.jpg" alt="team-members">
              </div>
              <div class="team-mobile-contents">
                <div class="team-info-card" v-for="n in 5" :key="n">
                  <img :src="memberImgUrl(n)" :alt="`member${n}`">
                  <div class="team-info">
                    <div>{{ members[n - 1].name }}</div>
                    <div>{{ members[n - 1].position }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="warning" @click.stop="toggleDialog(1)" :style="{ fontFamily: 'Noto Sans KR', fontSize: '12px' }" small>닫기</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </footer>
</template>

<script>
import members from '@/assets/json/members.json'

export default {
  data() {
    return {
      members,
      introDialog: false,
      teamDialog: false
    }
  },
  methods: {
    goGitlab() {
      window.open('https://lab.ssafy.com/s02-bigdata-sub2/s02p22b205')
    },
    toggleDialog(val) {
      if (!val) {
        this.introDialog = !this.introDialog
      } else {
        this.teamDialog = !this.teamDialog
      }
    },
    imgUrl(idx) {
      return require(`../../assets/images/service_information/capture${idx}.jpg`)
    },
    memberImgUrl(idx) {
      return require(`../../assets/images/members/member${idx}.jpg`)
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
    display:inline-block;
    font-size:14px;
    line-height: 15px;
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
  color: black;
  padding: 0 16px;
}

.intro-contents div[class$='-contents'] > ul > li {
  padding-bottom: 3px;
  line-height: 1.8;
}

.service-intro img {
  width: 60%;
  display: block;
  margin: 0 auto;
}

.service-intro ul.service-captures img {
  width: 90%;
  margin-bottom: 30px;
}

.service-intro ul.service-captures li > p {
  margin-bottom: 6px;
}

.service-intro .service-summery {
  margin: 1.4em auto;
  text-align: center;
  line-height: 1.9;
  font-size: 15px;
}

.team-contents img {
  width: 70%;
}

.team-mobile-contents,
.featuring-mini {
  display: none;
}

@media (max-width: 600px) {
  .service-intro img {
    width: 90%;
  }

  .team-contents,
  .featuring {
    display: none;
  }

  .team-mobile-contents,
  .featuring-mini {
    display: block;
  }

  .team-mobile-contents .team-info {
    font-family: 'Gothic A1';
    font-size: 17px;
    font-weight: 600;
    color: black;
    margin: 10px auto;
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
  }

  .team-mobile-contents .team-info > div {
    margin: 0 10px;
  }

  .team-info-card img {
    margin: 20px auto;
  }

  .team-mobile-contents .team-info p {
    margin-bottom: 6px;
    text-align: center;
  }

  .team-info-card {
    border: 1px solid silver;
    box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.15);
    border-radius: 20px;
    margin: 20px auto;
  }
}
</style>