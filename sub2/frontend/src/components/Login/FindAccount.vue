<template>
  <div class="find-wrapper">
    <div class="find-form-title">
      <h2>Find Password</h2>
    </div>
    <div class="find-box">
      <div class="find-box-wrapper">
        <form @submit.prevent="submitForm">
          <div class="find-form-wrapper">
            <div class="username-form">
              <label for="username" />
              <input id="username" v-model="username" type="text" placeholder="ID">
              <small class="logmessage px-2" v-if="!isUsernameValid">
                (한글 이름을 작성하세요.)
              </small>
            </div>
            <div class="email-form">
              <label for="email" />
              <input id="email" v-model="email" type="text" placeholder="E-mail">
              <small class="logmessage px-2" v-if="!isEmailValid">
                (이메일 양식으로 작성하세요.)
              </small>
            </div>
            <v-btn color="warning" block :disabled="!(isEmailValid && isUsernameValid)" type="submit" class="mt-5 btn">비밀번호 찾기</v-btn>
          </div>
        </form>
        <div class="alert-account-message" v-if="issueTempPassword">
          {{ email }} 주소로<br>
          임시 비밀번호를 발급했습니다.<br>
          임시 비밀번호로 로그인 후 <span>'MY PAGE'에서</span><br>
          <span>비밀번호 변경을 꼭 해주세요!</span>
        </div>
        <v-btn v-if="issueTempPassword" color="error" block class="mt-3 btn" @click="goLoginPage()">로그인 페이지로 이동</v-btn>
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
      email: '',
      issueTempPassword: false
    }
  },
  computed: {
    isUsernameValid() {
      return validateUserName(this.username)
    },
    isEmailValid() {
      return validateEmail(this.email)
    }
  },
  methods: {
    async submitForm() {
      try {
        const responseData = await this.$store.dispatch('FIND_PASSWORD', {
          username: this.username,
          email: this.email
        })
        if (responseData.status === 200) {
          this.issueTempPassword = true
        } else {
          alert('예기치 못한 오류가 발생했습니다. 관리자에게 문의하세요.')
        }
      } catch (error) {
        console.log(error)
        alert('이름과 이메일을 올바르게 다시 작성해주세요.')
      }
    },
    goLoginPage() {
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.find-form-title {
  margin: 1em 0;
}

.find-form-title h2 {
  font-family: 'Quicksand';
  text-align: center;
}

.find-box {
  font-family: 'Noto Sans KR';
  margin: 3em auto 1em;
  width: 100%;
  max-width: 600px;
}

.find-box-wrapper {
  width: 60%;
  margin: 0 auto;
}

.username-form,
.email-form {
  margin-bottom: 0.5em;
}

.find-form-wrapper input {
  background-color: lightgray;
  border-radius: 30px;
  height: 3em;
  width: 100%;
  max-width: 600px;
  padding: 0 0.5em;
}

.alert-account-message {
  margin: 20px 0;
  border: 1px solid silver;
  border-radius: 20px;
  font-size: 14px;
  font-family: 'Nanum Gothic';
  text-align: center;
  line-height: 1.8;
  padding: 10px 0;
  background-color: #eee;
}

.alert-account-message span {
  color: crimson;
  font-weight: 600;
}

@media (max-width: 600px) {
  .find-box {
    margin-top: 2em;
  }

  .find-box-wrapper {
    width: 85%;
  }

  .find-form-wrapper input {
    font-size: 0.8em;
  }
}
</style>