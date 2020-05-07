<template>
  <div class="account-wrapper">
    <div class="account-page-title">
      <div class="account-title">🚶 계정관리</div>
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
            <div class="category-subtitle">'대분류' 선택 후 하위 '중분류'에서 관심 카테고리 설정 가능</div>
            <div class="cats-chips">
              <div v-if="myFavoriteSubCats.length">
                <v-chip v-for="(category, idx) in myFavoriteSubCats" :key="idx" class="ma-1">{{ category }}<i class="far fa-window-close ml-1" @click="deleteCats(idx)"></i></v-chip>
              </div>
              <div v-else class="no-cats-list">
                <i class="fas fa-list"></i>
                <p>관심 카테고리를 설정해주세요.</p>
              </div>
            </div>
            <div class="select-section">
              <div class="main-select">
                <v-select
                  v-model="selectedMainCategories"
                  class="px-2"
                  :items="this.maincategory"
                  label="대분류"
                  color="warning"
                ></v-select>
              </div>
              <div class="sub-select">
                <v-select
                  ref="sub-select-box"
                  v-model="selectedSubCategories"
                  class="px-2"
                  :items="this.selectSubs"
                  label="중분류"
                  color="warning"
                  @mouseup="checkSelectMainCats"
                ></v-select>
              </div>
            </div>
          <div class="btn-group">
            <v-btn class="mb-2" color="warning" @click="updateMyAddInfo()">추가정보 변경</v-btn>
            <div class="mb-2">추가정보 입력 또는 변경 후 반드시 좌측 '추가정보 변경' 버튼을 눌러야 변경된 내용이 반영됩니다!</div>
          </div>
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
            <v-btn class="mt-2" color="warning" @click="checkNewPassword()" :disabled="!isNewPasswordValid">비밀번호 변경</v-btn>
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
              <div v-if="!outCheck">회원탈퇴를 하시려면 {{ this.info.username }}님의 비밀번호를 입력해주세요.</div>
              <input v-if="!outCheck" id="out-password" v-model="outPassword" type="password" placeholder="비밀번호를 작성하세요.">
              <div v-if="outCheck">인증되었습니다.</div>
              <div v-if="outCheck">정말로 탈퇴를 진행하시려면 <span style="color: crimson;">'탈퇴'</span> 버튼을 눌러주세요.</div>
              <div v-if="outCheck"><span style="color: crimson;">'탈퇴'</span> 버튼을 누르면 {{ this.info.username }} 님의 모든 정보가 삭제됩니다.</div>
              <div v-if="outCheck">탈퇴를 취소하시려면 <span style="color: orange;">'닫기'</span> 버튼을 눌러주세요.</div>
            </div>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn v-if="!outCheck" color="error" @click="checkOutPassword" :style="{ 'fontFamily': 'Stylish', 'fontSize': '17px' }">비밀번호 확인</v-btn>
            <v-btn v-if="outCheck" color="error" @click="goWithdrawal" :style="{ 'fontFamily': 'Stylish', 'fontSize': '17px' }">탈퇴</v-btn>
            <v-btn color="warning" @click="closeWithDrawalDialog" :style="{ 'fontFamily': 'Stylish', 'fontSize': '17px' }">닫기</v-btn>
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
      selectedMainCategories: null,
      selectedSubCategories: null,
      existPassword: '',
      newPassword: '',
      renewPassword: '',
      availableNewPassword: false,
      showErrorMessage: false,
      logMessage: [
        '비밀번호를 잘못 입력했습니다.',
        '비밀번호가 일치하지 않거나 비밀번호 양식에 어긋납니다.'
      ],
      withdrawalDialog: false,
      maincategory : [], 
      mainindex : {},
      subcategory : [], 
      subindex : {},
      subcategoryset : [],
      selectSubs: [],
      myFavoriteSubCats: [],
      outPassword: '',
      outCheck: false
    }
  },
  created() {
    this.getCategory()
    this.fetchMyInfo()
  },
  computed: {
    ...mapState({
      categories: state => state.data.categories
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
    async getCategory() {
      await this.$store.dispatch('GET_CATEGORIES')
      await this.setSubCategory()
    },
    setSubCategory() {
      for (const i in this.categories){
        const main = this.categories[i]
        this.maincategory.push(main.name)
        this.mainindex[main.name] = main.id
        let subCats = []
        for (const j in main.subcategory_set){
          const sub = main.subcategory_set[j]
          subCats.push(sub.name)
          this.subcategory.push(sub.name)
          this.subindex[sub.name] = sub.id
        }
        this.subcategoryset.push(subCats)
      }
    },
    async fetchMyInfo() {
      const myInfo = await this.$store.dispatch('GET_MYINFO')
      this.gender = myInfo.gender
      this.age = myInfo.age
      this.getMyCategory(myInfo.categorys)
    },
    getMyCategory(favoriteCategory) {
      let sortedCategory = []
      let favoriteCnt = favoriteCategory.length
      for (const categoryList of this.subcategoryset) {
        for (const category of categoryList) {
          if (favoriteCategory.includes(category)) {
            sortedCategory.push(category)
            if (sortedCategory.length === favoriteCnt) {
              this.myFavoriteSubCats = sortedCategory
              return
            }
          }
        }
      }
    },
    checkSelectMainCats() {
      if (this.selectSubs[0] === '') {
        alert('대분류를 먼저 선택해주세요.')
      }
    },
    deleteCats(idx) {
      this.myFavoriteSubCats.splice(idx, 1)
    },
    async updateMyAddInfo() {
      let convertCategoryIDs = []
      for (const i in this.myFavoriteSubCats){
        convertCategoryIDs.push(this.subindex[this.myFavoriteSubCats[i]])
      }
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
        await this.fetchMyInfo()
      } catch(error) {
        alert('예기치 못한 오류가 발생했습니다. 관리자에게 문의하세요.')
      }
    },
    async checkExistPassword() {
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
      if (this.isNewPasswordValid) {
        try {
          const userData = {
            password: this.newPassword
          }
          await this.$store.dispatch('CHANGE_PASSWORD', userData)
          alert('비밀번호가 변경되었습니다.')
          this.initPasswordForm()
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
    async checkOutPassword() {
      try {
        await this.$store.dispatch('LOGIN', {
          username: this.$store.getters.info.username,
          password: this.outPassword
        })
        this.outCheck = true
      } catch (error) {
        if (error.status === 400) {
          alert('비밀번호를 잘못 입력하셨습니다.')
        } else {
          alert('예기치 못한 오류가 발생했습니다. 관리자에게 문의하세요.')
        }
      }
    },
    withdrawalAlert() {
      this.withdrawalDialog = true
    },
    closeWithDrawalDialog() {
      this.withdrawalDialog = false
      this.outPassword = ''
      this.outCheck = false
    },
    async goWithdrawal() {
      await this.$store.dispatch('DELETE_USER')
      this.$store.commit('logout')
      this.$router.push('/')
    }
  },
  watch: {
    selectedMainCategories() {
      if (this.selectedMainCategories !== null && this.selectedMainCategories !== '') {
        let mainIdx = this.mainindex[this.selectedMainCategories]
        this.selectSubs = this.subcategoryset[mainIdx - 1]
        this.selectedSubCategories = ''
      } else {
        this.selectSubs = []
      }
    },
    selectedSubCategories() {
      if (this.selectedSubCategories !== null && this.selectedSubCategories !== '') {
        if (!this.myFavoriteSubCats.includes(this.selectedSubCategories)) {
          this.myFavoriteSubCats.push(this.selectedSubCategories)
          this.$refs['sub-select-box'].initialValue = ''
          this.$refs['sub-select-box'].lazyValue = ''
          this.$refs['sub-select-box'].isFocused = false
          this.$refs['sub-select-box'].hasColor = false
          this.$refs['sub-select-box'].hasFocused = false
          this.$refs['sub-select-box'].hasInput = false
          this.selectedMainCategories = ''
          this.selectedSubCategories = ''
          this.selectSubs = []
        } else {
          alert('해당 카테고리는 이미 선택되었습니다.')
        }
      }
    }
  }
}
</script>

<style scoped>
.account-wrapper {
  margin: 0 auto;
  width: 85%;
}

.account-wrapper .account-page-title {
  margin-bottom: 1.5em;
}

.account-wrapper .account-title {
  font-size: 1.5em;
  font-weight: bold;
  font-family: 'Noto Sans KR';
  margin-bottom: 1.5em;
}

.account-wrapper .account-page-contents > div div[class$='-title'],
.account-wrapper .account-page-contents > div label[class$='-title'] {
  font-family: 'Nanum Gothic';
  font-weight: 600;
  font-size: 1.1em;
}

.account-wrapper .account-page-contents > div div[class$='-title']:not(.category-title),
.account-wrapper .account-page-contents > div label[class$='-title'] {
  padding-bottom: 0.8em;
}

.category-subtitle {
  font-size: 14px;
  font-weight: 600;
  color: gray;
  padding: 0.4em 0 0.8em;
}

.select-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 5px;
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

.change-password-form > div[class$='form'] input,
#out-password {
  display: block;
  padding: 0.8em 0.4em;
  width: 100%;
  border: 1px solid lightgray;
  border-radius: 5px;
  box-shadow: 2px 4px 4px rgba(0, 0, 0, 0.05);
}

#out-password {
  width: 100%;
  margin: 0 auto;
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

.no-cats-list {
  font-family: 'Noto Sans KR';
  font-weight: 600;
  text-align: center;
}

.no-cats-list i {
  font-size: 90px;
}

.no-cats-list p {
  font-size: 17px;
  margin: 6px 0;
}

.cats-chips {
  padding: 8px;
  border: 1px solid silver;
  box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

.btn-group {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
}

.btn-group > div {
  font-size: 13.5px;
  font-family: 'Gothic A1';
  font-weight: 600;
  color: crimson;
  margin-left: 8px;
}

@media (max-width: 900px) {
  .account-wrapper {
    width: 100%;
  }
}

@media (max-width: 600px) {
  .select-section {
    display: block;
  }
}
</style>