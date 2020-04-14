<template>
  <div class="account-wrapper">
    <div class="account-page-title">
      <h2>계정관리</h2>
    </div>
    <div class="account-page-contents">
      <div class="add-info">
        <div class="add-info-title">✔️추가정보 입력</div>
        <div class="add-info-form">
          <div class="add-info-gender-age-wrapper">
            <div class="add-info-gender">
              <div class="gender-title">성별</div>
              <v-radio-group v-model="gender" row id="gender" class="pa-0">
                <v-radio label="남성" value="M" color="primary"></v-radio>
                <v-radio label="여성" value="F" color="primary"></v-radio>
              </v-radio-group>
            </div>
            <div class="add-info-age">
              <label for="age" class="d-block age-title">나이</label>
              <input id="age" v-model="age" type="number" min="1">
            </div>
          </div>
          <div class="add-info-category">
            <div class="category-title">관심 카테고리(중복선택 가능)</div>
            <v-select
              v-model="selectedCategories"
              class="pa-0"
              :items="this.categories.map(category => `${category.name}-${category.id}`)"
              multiple
              chips
            ></v-select>
          <v-btn class="mt-2" color="warning" @click="updateMyAddInfo()">추가정보 변경</v-btn>
          </div>
        </div>
      </div>
      <div class="change-password">
        <div class="change-password-title">✔️비밀번호 변경</div>
        <div class="change-password-form">
          <div class="exist-password-form" v-if="!availableNewPassword">
            <label for="exist-password" class="d-block">기존 비밀번호</label>
            <input id="exist-password" v-model="existPassword" type="password" placeholder="기존의 비밀번호를 작성하세요.">
            <div class="logmessage"> <!-- v-if로 비밀번호가 틀렸을 때 logMessage 출력구문 추가 -->
              {{ logMessage[0] }}
            </div>
            <v-btn class="mt-2" color="warning" @click="checkExistPassword()">확인</v-btn>
          </div>
          <div class="new-password-form"> <!-- 로직 완성 후 좌측 div태그 안에 v-if="availableNewPassword" 구문 추가 -->
            <label for="new-password" class="d-block">새로운 비밀번호(기존 비밀번호와 다르게 작성)</label>
            <input id="new-password" v-model="newPassword" type="password" placeholder="새로운 비밀번호를 작성하세요.">
            <small class="d-block">(영문소문자(6자 이상) + 숫자(2자 이상) + 특수문자(!, ?, @, % 중 1개)로 조합해서 총 9자 이상 작성할 것)</small>
            <div class="logmessage"> <!-- v-if로 비밀번호가 틀렸을 때 logMessage 출력구문 추가 -->
              {{ logMessage[1] }}
            </div>
          </div>
          <div class="renew-password-form"> <!-- 로직 완성 후 좌측 div태그 안에 v-if="availableNewPassword" 구문 추가 -->
            <label for="renew-password" class="d-block">새로운 비밀번호 확인</label>
            <input id="renew-password" v-model="renewPassword" type="password" placeholder="동일하게 한 번 더 작성하세요.">
            <div class="logmessage"> <!-- v-if로 비밀번호가 틀렸을 때 logMessage 출력구문 추가 -->
              {{ logMessage[1] }}
            </div>
            <v-btn class="mt-2" color="warning" @click="checkNewPassowrd()">비밀번호 변경</v-btn>
          </div>
        </div>
      </div>
      <div class="out-user">
        <div class="out-user-title">✔️회원탈퇴</div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { checkPassword, changePassword, updateMyInfo } from '@/api/index.js'
import { validatePassword } from '@/utils/validation/passwordValidation.js'

export default {
  data() {
    return {
      gender: '',
      age: '',
      selectedCategories: [],
      existPassword: '',
      newPassword: '',
      renewPassword: '',
      availableNewPassword: false,
      logMessage: [
        '비밀번호를 잘못 입력했습니다.',
        '비밀번호가 일치하지 않거나 비밀번호 양식에 어긋납니다.'
      ]
    }
  },
  created() {
    // mypage의 account 항목 클릭하면 해당 유저의 추가정보가 있는 경우 추가정보 데이터 불러오는 로직을 가장 먼저 수행
  },
  computed: {
    ...mapState({
      categories: state => state.data.categories.slice(0, 41).filter(category => category.id % 100)
    }),
    isNewPasswordValid() {
      return this.newPassword === this.renewPassword && this.newPassword !== this.existPassword && validatePassword(this.newPassword) && validatePassword(this.renewPassword)
    }
  },
  methods: {
    async updateMyAddInfo() {
      let convertCategoryIDs = this.selectedCategories.map(category => category.split('-')[1])
      const userAddData = {
        gender: this.gender,
        age: this.age,
        favoriteCategory: convertCategoryIDs
      }
      // 추가정보 등록 로직 작성(추가정보 입력 후 backend로 userAddData 보낸 후
      // 기존 token에 유저 정보가 담겨 있던 내용에서 추가정보를 추가하여 새로운 token값을 frontend 쪽으로 전송 => jwt-decode로 getters에 반영)
    },
    checkExistPassword() { // 기존 비밀번호를 올바르게 입력해야 새로운 비밀번호 작성가능
      // 비밀번호 확인 로직 작성(api 폴더에 작성한 checkPassword() 함수 불러와서 사용)
      // api 폴더의 checkPassword() 함수에서 요청주소 작성해야 함
    },
    checkNewPassowrd() {
      // 새로운 비밀번호가 비밀번호 validation에 맞는지 확인 후 맞는 경우 비밀번호 변경(api 폴더에 작성한 changePassword() 함수 불러와서 사용)
      // api 폴더의 changePassword() 함수에서 요청주소 작성해야 함
      if (isNewPasswordValid) {
        // 비밀번호 변경 로직 작성
        alert('비밀번호가 변경되었습니다.')
        this.initPasswordForm() // 비밀번호 변경 성공 후 비밀번호 변경 양식 초기화
      }
    },
    initPasswordForm() {
      this.existPassword = ''
      this.newPassword = ''
      this.renewPassword = ''
      this.availableNewPassword = false
    }
  }
}
</script>

<style scoped>
.account-wrapper {
  margin: 0 auto;
  width: 70%;
}

.account-wrapper .account-page-title {
  margin-bottom: 1.5em;
}

.account-wrapper .account-page-title h2 {
  font-family: 'Noto Sans KR';
}

.account-wrapper .account-page-contents > div div[class$='-title'],
.account-wrapper .account-page-contents > div label[class$='-title'] {
  font-family: 'Nanum Gothic';
  font-weight: 600;
  font-size: 1.1em;
  padding-bottom: 0.8em;
}

.add-info,
.change-password {
  margin-bottom: 2em;
}

.add-info-form,
.change-password-form {
  border: 2px dashed rgba(0, 0, 0, 0.17);
  border-radius: 20px;
  box-shadow: 3px 5px 5px rgba(0, 0, 0, 0.05);
}

.add-info-form > div {
  padding: 0.65em;
}

.add-info-gender-age-wrapper {
  display : flex;
  justify-content: space-between;
}

.add-info-gender-age-wrapper input {
  margin-top: 16px;
  border: 1px solid silver;
}

.change-password-form > div[class$='form'] {
  padding: 1em 0.65em;
}

.change-password-form > div[class$='form'] > label {
  font-size: 1.1em;
  font-weight: 600;
  font-family: 'Noto Sans KR';
  margin-bottom: 0.5em;
}

.change-password-form > div[class$='form'] input {
  display: block;
  padding: 0.8em 0.4em;
  width: 100%;
  border: 1px solid lightgray;
  border-radius: 5px;
  box-shadow: 2px 4px 4px rgba(0, 0, 0, 0.05);
}

.logmessage {
  font-size: 0.9em;
  font-weight: 600;
  font-family: 'Noto Sans KR';
  color: crimson;
  margin-top: 0.25em;
}

@media (max-width: 900px) {
  .account-wrapper {
    width: 100%;
  }
}
</style>