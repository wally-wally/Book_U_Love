<template>
  <div>
    <div class="signup-tos">
      <div class="signup-title">
        <div class="service-logo">
          <img src="../../assets/images/team_logo/books.png" alt="team-logo">
        </div>
        <div class="service-title">
          <div>유저 맞춤 책 추천 서비스</div>
          <div>환영합니다!</div>
        </div>
      </div>
      <div class="tos-section">
        <div class="tos-element">
          <span class="tos-title">이용약관 동의(필수)</span>
          <span class="tos-dialog-btn" @click.stop="showToS(0)">
            <i :class="checkedToS[0] ? 'fas fa-check-circle' : 'far fa-circle'"></i>
          </span>
        </div>
        <hr color="lightgray">
        <div class="tos-element">
          <span class="tos-title">개인정보 수집 및 이용동의(필수)</span>
          <span class="tos-dialog-btn" @click.stop="showToS(1)">
            <i :class="checkedToS[1] ? 'fas fa-check-circle' : 'far fa-circle'"></i>
          </span>
        </div>
        <div class="next-btn">
          <v-btn block color="error" @click="goSignUpForm()" :disabled="!(checkedToS[0] && checkedToS[1])">다음</v-btn>
        </div>
      </div>
    </div>
    <ToSDialog v-if="showDialog" :tosData="tosData[selectedElem]" :showDialog="showDialog" @closeDialog="checkAgree"></ToSDialog>
  </div>
</template>

<script>
import tosData from '@/assets/json/tos.json'
import ToSDialog from '@/components/Login/ToSDialog'

export default {
  components: {
    ToSDialog
  },
  data() {
    return {
      tosData,
      selectedElem: '',
      checkedToS: {
        0: false,
        1: false
      },
      showDialog: false
    }
  },
  methods: {
    showToS(elem) {
      if (!this.checkedToS[elem]) {
        this.showDialog = true
        this.selectedElem = elem
      } else if(this.checkedToS[elem]) {
        this.checkedToS[elem] = false
      }
    },
    checkAgree(agree) {
      this.checkedToS[this.selectedElem] = agree ? true : false
      this.showDialog = false
      this.selectedElem = ''
    },
    goSignUpForm() {
      this.$store.commit('changeToS', true)
      this.$router.push('/signup/register')
    }
  }
}
</script>

<style scoped>
.signup-tos {
  font-family: 'Noto Sans KR';
  margin: 1em auto;
  width: 100%;
  max-width: 500px;
}

.signup-title .service-logo {
  text-align: center;
}

.signup-title .service-logo img {
  margin: 0.5em 0;
  width: 200px;
  height: 200px;
}

.signup-title .service-title {
  text-align: center;
  margin-top: 0.6em;
}

.signup-title .service-title > div:first-child {
  font-size: 1.5em;
  font-weight: 600;
}

.signup-title .service-title > div:last-child {
  font-size: 1.3em;
  padding-top: 0.2em;
}

.tos-section {
  text-align: center;
  width: 60%;
  margin: 1.5em auto 0;
}

.tos-section .tos-element {
  display: flex;
  justify-content: space-between;
  margin: 0.7em 0;
}

.tos-section .tos-element .tos-dialog-btn i:hover {
  cursor: pointer;
}

.tos-section .next-btn {
  margin: 2em 0;
}


@media (max-width: 600px) {
  .signup-title .service-logo img {
    width: 170px;
    height: 170px;
  }

  .signup-title .service-title > div:first-child {
    font-size: 1.3em;
  }

  .signup-title .service-title > div:last-child {
    font-size: 1.1em;
  }

  .tos-title {
    font-size: 0.9em;
    letter-spacing: -0.02em;
  }
}
</style>