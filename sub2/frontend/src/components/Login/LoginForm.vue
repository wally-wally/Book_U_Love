<template>
  <div>
    <div class="form-title">
      <h2>Login</h2>
    </div>
    <div class="login-box">
      <div class="login-box-wrapper">
        <form @submit.prevent="submitForm">
          <div class="login-form-wrapper">
            <div class="email-form">
              <label for="email" />
              <input id="email" v-model="username" type="text" placeholder="ID">
              <small class="logmessage px-2" v-if="!(isEmailValid || isUsernameValid)">
                (이름 또는 이메일 양식으로 입력하세요.)
              </small>
            </div>
            <div class="password-form">
              <label for="password" />
              <input id="password" v-model="password" type="password" placeholder="Password">
            </div>
            <v-btn color="warning" block :disabled="!(isEmailValid || isUsernameValid) || !password" type="submit" class="mt-5 btn">로그인</v-btn>
          </div>
        </form>
        <div class="find-account-box">
          <span @click="goSignupPage">회원가입</span>
          <span @click="goFindAccount">비밀번호 찾기</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { validateUserName } from '@/utils/validation/userNameValidation.js'
import { validateEmail } from '@/utils/validation/emailValidation.js'

export default {
  data() {
    return {
      username: '',
      password: ''
    }
  },
  computed: {
    isEmailValid() {
      return validateEmail(this.username)
    },
    isUsernameValid() {
      return validateUserName(this.username)
    }
  },
  methods: {
    async submitForm() {
      try {
        await this.$store.dispatch('LOGIN', {
          username: this.username,
          password: this.password
        })
        this.$router.push('/')
        this.initForm()
      } catch (error) {
        let errorMessage = ''
        if (error.status === 400) {
          errorMessage = '아이디와 비밀번호를 다시 확인하세요.'
        } else if(error.status === 500) {
          errorMessage = '등록되지 않은 아이디입니다.'
        } else {
          errorMessage = '예기치 못한 오류가 발생했습니다. 관리자에게 문의해주세요.'
        }
        alert(errorMessage)
      }
    },
    initForm() {
      this.email = ''
      this.password = ''
    },
    goSignupPage() {
      this.$router.push('/signup')
    },
    goFindAccount(type) {
      this.$router.push('/login/findaccount')
    }
  }
}
</script>

<style scoped>
.form-title {
  margin: 1em 0;
}

.form-title h2 {
  font-family: 'Quicksand';
  text-align: center;
}

.login-box {
  font-family: 'Noto Sans KR';
  margin: 3em auto 1em;
  width: 100%;
  max-width: 600px;
}

.login-box-wrapper {
  width: 60%;
  margin: 0 auto;
}

.email-form,
.password-form {
  margin-bottom: 0.5em;
}

.login-form-wrapper input {
  background-color: lightgray;
  border-radius: 30px;
  height: 3em;
  width: 100%;
  max-width: 600px;
  padding: 0 0.5em;
}

.find-account-box {
  display: flex;
  justify-content: center;
  margin: 1.5em 0;
  font-size: 0.85rem;
  color: gray;
}

.find-account-box > span {
  padding: 0 0.5em;
}

.find-account-box > span:not(:last-child) {
  border-right: 1px solid rgb(117, 117, 117);
}

.find-account-box > span:hover {
  cursor: pointer;
  color: black;
  font-weight: 600;
}

.sns-login-title {
  text-align: center;
}

.sns-login-title p {
  margin-bottom: 0.5em;
  font-family: 'Gothic A1';
  letter-spacing: -0.02em;
}

.sns-login-buttons {
  display: flex;
  justify-content: center;
  align-items: center;
}

.sns-login-buttons > span {
  background-position: center;
  width: 70px;
  height: 70px;
  margin: 0 0.3em;
  transform: scale(0.6);
}

.sns-login-buttons > span[id="kakao-auth"] {
  background-image: url('../../assets/images/social_icon/kakao-talk.png');
}

.sns-login-buttons > span:hover {
  cursor: pointer;
}

.sns-login-buttons > div {
  padding: 10px 20px;
  background-color: #ffe500;
  border-radius: 5px;
  box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  transform: translateY(0);
  transition: all .2s;
}

.sns-login-buttons > div:hover {
  cursor: pointer;
  transform: translateY(-2px);
  box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.2);
}

@media (max-width: 600px) {
  .login-box {
    margin-top: 2em;
  }

  .login-form-wrapper input,
  .find-account-box {
    font-size: 0.8em;
  }

  .sns-login-title p {
    margin: 0;
    font-size: 0.9em;
  }

  .sns-login-buttons > span {
    margin: 0 0.2em;
    transform: scale(0.6);
  }
}
</style>
