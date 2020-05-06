<template>
  <div class="collect-form-wrapper">
    <div class="collect-form-title">
      <span>20권의 리뷰를 작성해주세요.</span>
    </div>
    <div class="collect-form-desc">
      작성한 리뷰 데이터와 {{ info.username }}님의 정보를 종합하여<br>
      Book_U_Love에서 도서를 추천해드릴께요<br>
      <div class="my-3">최소 10권 이상의 리뷰 작성을 권장합니다.</div>
    </div>
    <v-alert
      class="alert-box"
      dense
      type="error"
      border="left"
      outlined
      prominent>
      데이터 유형을 변경하면 이 페이지에서 작성된 리뷰 데이터가 삭제됩니다.
    </v-alert>
    <v-select
      class="select-box"
      v-model="selectType"
      :items="types"
      label="데이터 유형"
      dense
      outlined>
    </v-select>
    <div class="progress-box">
      <v-progress-linear
        :value="(writtenReviewCnt / 20) * 100"
        color="blue-grey"
        height="25" 
        reactive>
        <template v-slot="{ value }">
          <strong>{{ value.toFixed(0) }}%</strong>
        </template>
      </v-progress-linear>
    </div>
    <v-row v-if="!loading" class="book-data-section">
      <v-col>
        <v-stepper v-model="e1">
          <v-stepper-header>
            <template v-for="n in steps">
              <v-stepper-step ref="stepper" :key="`${n}-step`" :complete="e1 > n" :step="n + 5 * completePage" color="warning">
                <span class="step-text">Book{{ n + 5 * completePage }}</span>
              </v-stepper-step>
              <v-divider v-if="n !== steps" :key="n" ></v-divider>
            </template>
          </v-stepper-header>
          <v-stepper-items>
            <v-stepper-content v-for="n in steps" :key="`${n}-content`" :step="n">
              <div class="book-wrapper">
                <div class="book-category">{{ bookData[writtenReviewCnt].categorylist  | categoryList }}</div>
                <img :src="bookData[writtenReviewCnt].coverLargeUrl" alt="book-image">
                <p class="book-title">
                  {{ bookData[writtenReviewCnt].title }}
                </p>
                <div class="book-small-info">
                  <p>작가: {{ bookData[writtenReviewCnt].author | authorList }}</p>
                  <p>출판사: {{ bookData[writtenReviewCnt].publisher }}</p>
                </div>
              </div>
              <div class="review-form">
                <v-rating v-model="score" color="orange" background-color="orange lighten-3" half-increments dense class="d-inline"></v-rating><span class="score-text">({{ score * 2 }}점)</span>
                <textarea v-model="content" class="review-textarea" placeholder="리뷰를 입력해주세요."/>
              </div>
              <div class="d-flex justify-space-between">
                <v-btn color="yellow" @click="toggleDialog" small><span class="more-info-text">Information</span></v-btn>
                <v-btn color="warning" @click="storeReview(n, 1)" small>리뷰 등록</v-btn>
              </div>
              <div class="no-read-btn">
                <v-btn color="error" @click="storeReview(n, 0)" small>
                  이 책은 아직 읽지 않았어요
                </v-btn>
              </div>
            </v-stepper-content>
          </v-stepper-items>
        </v-stepper>
      </v-col>
      <v-dialog v-model="dialog" max-width="700" persistent>
        <v-card>
          <v-card-title class="book-dialog-title">
            <strong>도서 상세정보</strong>
            <v-btn color="error" small @click="toggleDialog">닫기</v-btn>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="pb-0">
            <div class="book-dialog">
              <img :src="bookData[writtenReviewCnt].coverLargeUrl" alt="book-cover-img">
              <p class="book-title">
                {{ bookData[writtenReviewCnt].title }}
              </p>
              <div class="book-small-info">
                <p>카테고리: {{ bookData[writtenReviewCnt].categorylist | categoryList }}</p>
                <p>작가: {{ bookData[writtenReviewCnt].author | authorList }}</p>
                <p>출판사: {{ bookData[writtenReviewCnt].publisher }}</p>
              </div>
              <div v-if="bookData[writtenReviewCnt].description.length" class="description-title">상세정보</div>
              <div v-if="bookData[writtenReviewCnt].description.length" class="book-description" v-html="bookData[writtenReviewCnt].description"></div>
              <div v-if="bookData[writtenReviewCnt].contents.length" class="contents-title">목차</div>
              <div v-if="bookData[writtenReviewCnt].contents.length" class="book-contents" v-html="bookData[writtenReviewCnt].contents"></div>
            </div>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="error" small @click="toggleDialog">닫기</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
    <div v-else class="book-data-seciton">
      <img src="../../assets/images/team_logo/books.png" alt="team-logo">
      <p>데이터를 가져오는 중입니다.</p>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data() {
    return {
      selectType: '평점 기준 TOP20',
      types: ['평점 기준 TOP20', '리뷰 개수 기준 TOP20'],
      writtenReviewCnt: 0,
      realReviewCnt: 0,
      bookData: [],
      reviewData: [],
      loading: false,
      e1: 1,
      steps: 5,
      user: '',
      score: 0,
      content: '',
      book: '',
      completePage: 0,
      dialog: false
    }
  },
  computed: {
    ...mapGetters(['info'])
  },
  created() {
    this.loading = true
    this.fetchBooks(this.selectType)
  },
  methods: {
    loadingComplete() {
      this.loading = false
    },
    async fetchBooks(type) {
      const myReviewData = await this.$store.dispatch('GET_MYINFO')
      const myReviewIDs = myReviewData.review_set.map(data => data.book.id)
      let sortTag = type === '리뷰 개수 기준 TOP20' ? 'count' : 'score'
      let pageIdx = 1
      while(true) {
        const pageData = await this.$store.dispatch('GET_BOOKS', {page: pageIdx, sortby: sortTag})
        for (const data of pageData['results']) {
          if (!myReviewIDs.includes(data.id)) {
            await this.bookData.push(data)
          }
          if (this.bookData.length === 20) {
            await this.loadingComplete()
            return
          }
        }
        pageIdx += 1
      }
    },
    addReviewCnt(val) {
      if (this.writtenReviewCnt < 19) {
        this.writtenReviewCnt += 1
      }
      this.realReviewCnt += val
    },
    storeReview(n, readStatus) {
      if (readStatus) {
        if (this.score && this.content.length) {
          this.user = this.info.user_id
          this.book = this.bookData[this.writtenReviewCnt].id
          const data = {
            user: this.user,
            book : this.book,
            score: this.score * 2,
            content: this.content
          }
          this.postReview(data)
          setTimeout(() => {
            this.addReviewCnt(1)
            this.nextStep(n)
            this.initForm()
          }, 0)
        } else {
          alert('평점(1점 이상)과 내용을 작성해주세요.')
        }
      } else {
        this.addReviewCnt(0)
        this.nextStep(n)
        setTimeout(() => {
          this.initForm()
        }, 0)
      }
    },
    async postReview(data) {
      const formData = new FormData()
      formData.append('user', data.user)
      formData.append('content', data.content)
      formData.append('score', data.score)
      formData.append('book', data.book)
      await this.$store.dispatch('ADD_REVIEWS', formData)
    },
    nextStep(n) {
      if (n === this.steps) {
        if (this.completePage === 3) {
          alert(`20권 중 ${this.realReviewCnt}권의 리뷰 등록이 끝났습니다. 메인 페이지로 이동합니다.`)
          this.$router.push('/')
          return
        }
        this.e1 = 1
        this.completePage += 1
      } else {
        this.e1 = n + 1
      }
      this.changeStepperColor()
    },
    changeStepperColor() {
      this.$refs.stepper[this.e1 - 1].isActive = true
      this.$refs.stepper[this.e1 - 1].isInactive = false
      this.$refs.stepper[this.e1 - 1].classes['v-stepper__step--active'] = true
      this.$refs.stepper[this.e1 - 1].classes['v-stepper__step--complete'] = false
      this.$refs.stepper[this.e1 - 1].classes['v-stepper__step--inactive'] = false
    },
    toggleDialog(n) {
      this.dialog = !this.dialog
    },
    initForm() {
      this.user = ''
      this.score = 0
      this.content = ''
      this.book = ''
    }
  },
  watch: {
    selectType() {
      this.loading = true
      this.fetchBooks(this.selectType)
      this.initForm()
      this.writtenReviewCnt = 0
      this.bookData = []
      this.reviewData = []
      this.e1 = 1
      this.completePage = 0
    }
  }
}
</script>

<style scoped>
.collect-form-wrapper {
  width: 90%;
  margin: 0 auto;
}

.collect-form-title,
.collect-form-desc {
  font-family: 'Noto Sans KR';
  text-align: center;
}

.collect-form-title {
  width: 100%;
  margin: 1em 0 1.5em;
}

.collect-form-title span{
  font-size: 22px;
  padding-bottom: 10px;
  border-bottom: 1.5px dotted silver;
}

.collect-form-desc {
  color: grey;
  font-size: 14px;
  padding-top: 4px;
  line-height: 1.6;
}

.alert-box,
.select-box {
  max-width: 500px;
  margin: 1.5em auto 0;
  font-family: 'Noto Sans KR';
}

.progress-box {
  max-width: 500px;
  margin: 0 auto;
}

.book-data-seciton {
  max-width: 500px;
  margin: 2em auto;
  text-align: center;
}

.book-data-seciton img {
  width: 150px;
  vertical-align: top;
}

.book-data-seciton p {
  font-family: 'Noto Sans KR';
  font-weight: 600;
  margin: 8px 0;
}

/* book information */
.book-data-section {
  max-width: 500px;
  padding: 1em auto;
  margin: 30px auto;
}

.col {
  padding: 0;
}

p {
  margin-bottom: 8px;
}

.step-text {
  font-size: 15px;
  letter-spacing: -1px;
}

.book-wrapper {
  font-family: 'Noto Sans KR';
  margin-bottom: 16px;
}

.book-category {
  font-size: 14px;
  color: grey;
  margin-bottom: 8px;
}

.book-title {
  font-weight: 600;
  font-size: 18px;
  color: black;
}

.book-small-info {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.score-text {
  font-size: 14px;
  color: grey;
  vertical-align: bottom;
}

.review-textarea {
  background-color:white;
  border: 1px solid lightgray;
  border-radius: 5px;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.15);
  display:block;
  margin-bottom: 20px;
  padding: 6px;
  width: 100%;
  height: 150px;
  resize: none;
}

.no-read-btn {
  display: flex;
  flex-direction: row-reverse;
  margin-top: 8px;
}

/* dialog */
.book-dialog-title {
  font-family: 'Gothic A1';
  font-weight: 600;
  font-size: 20px;
}

.book-dialog {
  font-family: 'Noto Sans KR';
}

.book-dialog img {
  float: right;
}

.book-dialog > .book-title {
  font-size: 18px;
  margin-bottom: 20px;
}

.book-dialog > .book-small-info {
  display: block;
  font-size: 16px;
  line-height: 2;
}

.description-title {
  clear: both;
}

.book-dialog > .description-title,
.book-dialog > .contents-title {
  font-size: 20px;
  font-weight: 600;
  color: black;
  margin: 20px 0 15px;
  padding-bottom: 5px;
  border-bottom: 1px solid silver;
}

.book-dialog > .book-description,
.book-dialog > .book-contents {
  margin-bottom: 15px;
}

@media (min-width: 450px) {
  .more-info-text:before {
    content: 'More ';
  }
}

@media (max-width: 600px) {
  .book-dialog img {
    float: none;
    width: 60vw;
    margin-bottom: 10px;
  }
}

@media (max-width: 400px) {
  .review-textarea {
    font-size: 14px;
  }
}
</style>