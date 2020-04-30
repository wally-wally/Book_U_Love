<template>
  <div>
    <div class="signup-form">
      <div class="signup-title">
        <h2>SignUp</h2>
      </div>
      <div class="signup-form-box">
        <div class="signup-form-box-wrapper">
          <div class="signup-form-wrapper">
            <div class="username-form">
              <label for="username" class="d-block">이름</label>
              <input id="username" v-model="username" type="text" placeholder="이름을 작성하세요.">
              <div class="logmessage" v-if="!isUserNameValid && clickedSignupBtn">
                {{ logMessage[0] }}
              </div>
              <div class="logmessage" v-if="errormessage.username.length > 0">{{errormessage.username[0]}}</div>
            </div>
            <div class="email-form">
              <label for="email" class="d-block">ID(E-mail)</label>
              <input id="email" v-model="email" type="text" placeholder="가입할 이메일 주소를 작성하세요.">
              <div class="logmessage" v-if="!isEmailValid && clickedSignupBtn">
                {{ logMessage[1] }}
              </div>
              <div class="logmessage" v-if="errormessage.email.length > 0">{{errormessage.email[0]}}</div>
            </div>
            <div class="password-form">
              <label for="password" class="d-block">비밀번호</label>
              <input id="password" v-model="password" type="password" placeholder="비밀번호를 작성하세요.">
              <small class="d-block">(영문소문자(4자 이상) + 숫자(2자 이상) + 특수문자(!, ?, @, % 중 1개)로 조합해서 총 9자 이상 작성할 것)</small>
              <div class="logmessage" v-if="!isPasswordValid && clickedSignupBtn">
                {{ logMessage[2] }}
              </div>
            </div>
            <div class="re-password-form">
              <label for="re-password" class="d-block">비밀번호 확인</label>
              <input id="re-password" v-model="rePassword" type="password" placeholder="비밀번호를 한 번 더 작성하세요.">
              <small class="d-block">(위에서 작성한 비밀번호와 동일하게 한 번 더 작성하세요.)</small>
              <div class="logmessage" v-if="!isRePasswordValid && clickedSignupBtn">
                {{ logMessage[3] }}
              </div>
            </div>
            <div class="gender-form">
              <label for="gender" class="d-block">성별</label>
              <v-radio-group v-model="gender" row id="gender" class="pa-0">
                <v-radio label="남성" value="M" color="primary"></v-radio>
                <v-radio label="여성" value="F" color="primary"></v-radio>
              </v-radio-group>
              <div class="logmessage" v-if="!gender && clickedSignupBtn">
                {{ logMessage[4] }}
              </div>
            </div>
            <div class="age-form">
              <label for="age" class="d-block">나이</label>
              <input id="age" v-model="age" type="number" min="1">
              <div class="logmessage" v-if="!isNumberValid && clickedSignupBtn">
                {{ logMessage[5] }}
              </div>
            </div>
            <div class="signup-btn">
              <v-btn color="warning" block @click="signupWithValid()"><span>회원가입</span></v-btn>
            </div>
          </div>
        </div>
      </div>
    </div>
    <CheckSignUpDialog v-if="showDialog" :showDialog="showDialog" :userData="userData" @closeDialog="checkSignup"></CheckSignUpDialog>
  </div>
</template>

<script>
import { validateUserName } from '@/utils/validation/userNameValidation.js'
import { validateEmail } from '@/utils/validation/emailValidation.js'
import { validatePassword } from '@/utils/validation/passwordValidation.js'
import { validateNumber } from '@/utils/validation/numberValidation.js'
import { registerUser } from '@/api/index.js'
import CheckSignUpDialog from '@/components/Login/CheckSignUpDialog'

export default {
  components: {
    CheckSignUpDialog
  },
  data() {
    return {
      username: '',
      email: '',
      password: '',
      rePassword: '',
      gender: '',
      age: '',
      logMessage: [
        '한글로만 작성해주세요.',
        '이메일 양식으로 작성해주세요.',
        '비밀번호 양식을 지켜서 작성해주세요.',
        '비밀번호가 일치하지 않거나 비밀번호 양식에 어긋납니다.',
        '성별을 선택해주세요.',
        '10세 이상 99세 이하의 나이를 입력해주세요.'
      ],
      clickedSignupBtn: false,
      showDialog: false,
      userData: {},
      errormessage : {
        username : [],
        email : []
      },
    }
  },
  computed: {
    isUserNameValid() {
      return validateUserName(this.username)
    },
    isEmailValid() {
      return validateEmail(this.email)
    },
    isPasswordValid() {
      return validatePassword(this.password)
    },
    isRePasswordValid() {
      return validatePassword(this.rePassword) && this.password === this.rePassword
    },
    isNumberValid() {
      return validateNumber(this.age) && this.age.length === 2
    }
  },
  methods: {
    signupWithValid() {
      this.clickedSignupBtn = true
      if (this.isUserNameValid && this.isEmailValid && this.isPasswordValid && this.isRePasswordValid && this.gender && this.isNumberValid) {
        this.userData = {
          username: this.username,
          email: this.email,
          gender: this.gender,
          age: this.age
        }
        this.showDialog = true
      }
    },
    async checkSignup(check) {
      if (check) {
        try {
          // Signup Logic
          const data = await registerUser({
            username: this.username,
            email: this.email,
            password: this.password,
            gender: this.gender,
            age: this.age
          })
          // Automatic Login after signup success
          await this.$store.dispatch('LOGIN', {
            username: this.email,
            password: this.password
          })
          this.$router.push('/signup/success')
        } catch (error) {
          if (error.status == 400) {
            this.errormessage = error.data
          }
        } finally {
          this.showDialog = false
        }
      } else {
        this.showDialog = false
      }
    },
  },
  watch: {
    email() {
      this.errormessage.email = []
    },
    username() {
      this.errormessage.username = []
    },
    age() {
      if (this.age.length >= 3) {
        alert('10세 이상 99세 이하의 나이로 입력해주세요.')
        this.age = this.age.slice(0, 2)
      }
    }
  }
}
</script>

<style scoped>
.signup-form {
  margin: 0 1em;
}

.signup-title {
  margin: 1em 0;
}

.signup-title h2 {
  font-family: 'Quicksand';
  text-align: center;
}

.signup-form-box {
  font-family: 'Noto Sans KR';
  margin: 3em auto 1em;
  width: 100%;
  max-width: 600px;
}

.signup-form-wrapper > div[class$='form'] {
  margin-bottom: 1.3em;
}

.signup-form-wrapper > div[class$='form'] > label {
  font-size: 1.2em;
  font-weight: 600;
  margin-bottom: 0.5em;
}

.signup-form-wrapper > div[class$='form'] .logmessage {
  font-size: 0.9em;
  font-weight: 600;
  color: crimson;
  margin-top: 0.25em;
}

.signup-form-wrapper input {
  display: block;
  padding: 0.8em 0.4em;
  width: 100%;
  border: 1px solid lightgray;
  border-radius: 5px;
  box-shadow: 2px 4px 4px rgba(0, 0, 0, 0.05);
}

.signup-btn {
  margin: 2.5em 0 5em;
}

.signup-btn span {
  font-size: 1.1em;
}

@media (max-width: 600px) {
  .signup-form-wrapper > div[class$='form'] > label {
    font-size: 1.1em;
  }
}
</style>
