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
              :items="this.categories.map(category => `${category.id}-${category.mainCatsName}-${category.subCatsName}-${category.name}`)"
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
            <div class="logmessage" v-if="showErrorMessage">
              {{ logMessage[0] }}
            </div>
            <v-btn class="mt-2" color="warning" @click="checkExistPassword()">확인</v-btn>
          </div>
          <div class="new-password-form" v-if="availableNewPassword">
            <label for="new-password" class="d-block">새로운 비밀번호(기존 비밀번호와 다르게 작성)</label>
            <input id="new-password" v-model="newPassword" type="password" placeholder="새로운 비밀번호를 작성하세요.">
            <small class="d-block">(영문소문자(4자 이상) + 숫자(2자 이상) + 특수문자(!, ?, @, % 중 1개)로 조합해서 총 9자 이상 작성할 것)</small>
            <div class="logmessage" v-if="showErrorMessage">
              {{ logMessage[1] }}
            </div>
          </div>
          <div class="renew-password-form" v-if="availableNewPassword">
            <label for="renew-password" class="d-block">새로운 비밀번호 확인</label>
            <input id="renew-password" v-model="renewPassword" type="password" placeholder="동일하게 한 번 더 작성하세요.">
            <div class="logmessage" v-if="showErrorMessage">
              {{ logMessage[1] }}
            </div>
            <v-btn class="mt-2" color="warning" @click="checkNewPassword()">비밀번호 변경</v-btn>
          </div>
        </div>
      </div>
      <div class="out-user">
        <div class="out-user-title">✔️회원탈퇴</div>
        <div class="out-user-form">
          <div class="out-user-section">
            <div class="out-user-question">
              <span class="mr-4">회원을 탈퇴하시겠습니까?</span>
            <v-btn @click="withdrawalAlert" color="error" small>탈퇴 진행</v-btn></div>
            <v-alert
              class="alert-box"
              dense
              type="error"
              border="left"
              prominent>
              회원을 탈퇴하면 {{ this.info.username }}님의 정보가 모두 삭제됩니다.<br>상단 '탈퇴 진행' 버튼을 누르면 회원 탈퇴가 진행됩니다.
            </v-alert>
          </div>
        </div>
      </div>
      <v-dialog v-model="withdrawalDialog" width="600" persistent>
        <v-card>
          <v-card-text class="pb-0">
            <div class="text-center out-user-dialog-text">
              <i class="fas fa-user-minus"></i>
              <div>정말로 탈퇴를 진행하시려면 <span style="color: crimson;">'탈퇴'</span> 버튼을 눌러주세요.</div>
              <div>탈퇴를 취소하시려면 <span style="color: orange;">'닫기'</span> 버튼을 눌러주세요.</div>
            </div>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="error" @click="goWithdrawal" :style="{ 'fontFamily': 'Stylish', 'fontSize': '17px' }">탈퇴</v-btn>
            <v-btn color="warning" @click="withdrawalDialog = false" :style="{ 'fontFamily': 'Stylish', 'fontSize': '17px' }">닫기</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
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
      showErrorMessage: false,
      logMessage: [
        '비밀번호를 잘못 입력했습니다.',
        '비밀번호가 일치하지 않거나 비밀번호 양식에 어긋납니다.'
      ],
      withdrawalDialog: false
    }
  },
  created() {
    // mypage의 account 항목 클릭하면 해당 유저의 기존 추가정보 데이터 불러오는 로직을 가장 먼저 수행
    this.fetchMyInfo()
  },
  computed: {
    ...mapState({
      categories: state => state.data.detailCategories
    }),
    ...mapGetters(['info']),
    isNewPasswordValid() {
      return this.newPassword === this.renewPassword &&
             this.newPassword !== this.existPassword &&
             this.renewPassword !== this.existPassword &&
             validatePassword(this.newPassword) &&
             validatePassword(this.renewPassword)
    }
  },
  methods: {
    async fetchMyInfo() {
      const myInfo = await this.$store.dispatch('GET_MYINFO')
      this.gender = myInfo.gender
      this.age = myInfo.age
      this.getMyCategory(myInfo.categorys)
    },
    getMyCategory(favoriteCategory) {
      this.selectedCategories = this.categories.filter(category => favoriteCategory.includes(category.name)).map(item => `${item.id}-${item.mainCatsName}-${item.subCatsName}-${item.name}`)
    },
    async updateMyAddInfo() {
      let convertCategoryIDs = this.selectedCategories.map(category => category.split('-')[3])
      const userAddData = {
        username: this.info.username,
        email: this.info.email,
        gender: this.gender,
        age: this.age,
        categorys: convertCategoryIDs
      }
      try {
        await this.$store.dispatch('CHANGE_USER_INFO', userAddData)
        alert('추가정보가 수정되었습니다.')
        this.fetchMyInfo() // 추가정보 수정 후 수정된 추가정보 불러오기
      } catch(error) {
        console.log(error)
        alert('예기치 못한 오류가 발생했습니다. 관리자에게 문의하세요.')
      }
    },
    async checkExistPassword() { // 기존 비밀번호를 올바르게 입력해야 새로운 비밀번호 작성가능
      // (1) 기존 비밀번호 확인 로직(기존에 구현한 LOGIN 로직을 활용하여 작성됨)
      try {
        await this.$store.dispatch('LOGIN', {
          username: this.$store.getters.info.username,
          password: this.existPassword
        })
        this.availableNewPassword = true
        this.showErrorMessage = false
      } catch (error) {
        if (error.status === 400) {
          alert('비밀번호를 잘못 입력하셨습니다.')
          this.showErrorMessage = true
        }
      }
    },
    async checkNewPassword() {
      // (2) 새로운 비밀번호 변경 로직
      // 새로운 비밀번호가 비밀번호 validation에 맞는지 확인 후 맞는 경우 비밀번호 변경(api 폴더에 작성한 changePassword() 함수 불러와서 사용)
      // api 폴더의 changePassword() 함수에서 요청주소 작성해야 함
      // 비밀번호 변경 validation : 새로운 비번 === 새로운 비번 재확인 && 새로운 비번이 기존 비번과 달라야 함 && 새로운 비번이 비밀번호 양식에 맞는지 확인
      if (this.isNewPasswordValid) {
        try {
          // 비밀번호 변경 로직 작성
          // const userData = {}  =>  object 안에 비밀번호 변경시 보내야 하는 데이터 key-value 쌍 형태로 작성
          await this.$store.dispatch('CHANGE_PASSWORD', userData)
          alert('비밀번호가 변경되었습니다.')
          this.initPasswordForm() // 비밀번호 변경 성공 후 비밀번호 변경 양식 초기화 
        } catch (error) {
          console.log(error)
          alert('예기치 못한 오류가 발생했습니다. 관리자에게 문의하세요.')
        }
      } else {
        this.showErrorMessage = true
      }
    },
    initPasswordForm() {
      this.existPassword = ''
      this.newPassword = ''
      this.renewPassword = ''
      this.availableNewPassword = false
      this.showErrorMessage = false
    },
    withdrawalAlert() {
      this.withdrawalDialog = true
    },
    async goWithdrawal() {
      await this.$store.dispatch('DELETE_USER')
      this.$store.commit('logout')
      this.$router.push('/')
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
.change-password,
.out-user {
  margin-bottom: 2em;
}

.add-info-form,
.change-password-form,
.out-user-form {
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

.change-password-form > div[class$='form'],
.out-user-section {
  padding: 1em 0.65em;
}

.change-password-form > div[class$='form'] > label,
.out-user-question {
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

.out-user-dialog-text {
  font-family: 'Stylish';
  font-weight: 600;
}

.out-user-dialog-text i {
  font-size: 100px;
  margin-bottom: 12px;
}

.out-user-dialog-text > div {
  font-size: 18px;
  line-height: 2;
}

@media (max-width: 900px) {
  .account-wrapper {
    width: 100%;
  }
}
</style>