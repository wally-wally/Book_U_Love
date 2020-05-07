<template>
  <div>
    <div class="book-detail-wrapper" v-if="!loadingStatus">
      <div class="book-info">
        <div class="book-header">
          <div class="book-title">
            {{ book.title }}
          </div>
          <div class="book-score">
            {{book.avg}} ({{book.r_cnt}}명)
          </div>
        </div>
        <div class="book-basic-info">
          <div class="book-cover-img">
            <img :src="book.coverLargeUrl" :title="book.title" :alt="book.title">
          </div>
          <div class="book-more-info">
            <div class="more-row">
              <div class="more-cell">Author</div>
              <div class="more-cell">
                <router-link  v-for="author in book.author" :key="author.id" :to="`/author/${author.id}`" class="author-link">
                  {{author.name}}
                </router-link>
              </div>
            </div>
            <div class="more-row">
              <div class="more-cell">Publisher</div>
              <div class="more-cell">{{book.publisher}}</div>
            </div>
            <div class="more-row">
              <div class="more-cell">Publish Date</div>
              <div class="more-cell">{{book.pubDate.slice(0,4)}}.{{book.pubDate.slice(4,6)}}.{{book.pubDate.slice(6,8)}}</div>
            </div>
            <div class="more-row">
              <div class="more-cell">Price</div>
              <div class="more-cell">{{book.priceStandard}}원</div>
            </div>
          </div>
        </div>
        <div class="like-btn" v-if="this.$store.state.user.isLogin" @click="this.jjim" style="margin-bottom:40px">
          <div v-if="book.my" class="like-content">
            <button class="btn-secondary like-review">
              <i class="fa fa-heart" aria-hidden="true"></i> 찜에서 제거
            </button>
          </div>
          <div v-else class="like-content">
            <button class="btn-secondary like-review">
              <i class="fa fa-heart" aria-hidden="true"></i> 책 추가하기
            </button>
          </div>
        </div>
        <div class="book-detail-info">
          <v-card v-if="book.description" class="mb-5">
            <v-card-title class="pt-5 pb-10 book-detail-card-title">
            책소개
            </v-card-title>
            <v-card-text v-html="book.description" class="book-detail-contents">
            </v-card-text>
          </v-card>
          <v-card v-if="book.contents" class="mb-5">
            <v-card-title class="pt-5 pb-10 book-detail-card-title">
            목차
            </v-card-title>
            <v-card-text class="book-detail-contents">
              <div v-html="book.contents"></div>
            </v-card-text>
          </v-card>
          <v-card v-if="book.publisherReview" class="mb-5">
            <v-card-title class="pt-5 pb-10 book-detail-card-title">
            출판사 서평
            </v-card-title>
            <v-card-text class="book-detail-contents">
              <div v-html="book.publisherReview"></div>
            </v-card-text>
          </v-card>
        </div>
      </div>
      <div class="book-review">
        <div class="review-box">
          <div class="review-form-title main-title">📚 도서 리뷰</div>
          <div class="review-form">
            <input type="text" v-model="this.time" class="d-none">
            <form v-if="this.$store.state.user.isLogin && (!myReview.length || editMode)">
              <div class="star-score">
                <v-rating v-model="score" color="orange" background-color="orange lighten-3" half-increments dense class="d-inline"></v-rating>
                <span class="score-text">({{ score * 2 }}점)</span>
                <!-- <fieldset class="score">
                  <input v-model="score" type="radio" id="star10" name="score" value="10"/>
                  <label class="full" for="star10" title="최고의 책입니다. 10점"></label>
                  <input v-model="score" type="radio" id="star9" name="score" value="9"/>
                  <label class="half" for="star9" title="훌륭한 책입니다. 9점"></label>
                  <input v-model="score" type="radio" id="star8" name="score" value="8"/>
                  <label class="full" for="star8" title="괜찮은 책입니다. 8점"></label>
                  <input v-model="score" type="radio" id="star7" name="score" value="7"/>
                  <label class="half" for="star7" title="적당한 책입니다. 7점"></label>
                  <input v-model="score" type="radio" id="star6" name="score" value="6"/>
                  <label class="full" for="star6" title="음... 6점"></label>
                  <input v-model="score" type="radio" id="star5" name="score" value="5"/>
                  <label class="half" for="star5" title="나름 읽을만했어요 5점"></label>
                  <input v-model="score" type="radio" id="star4" name="score" value="4"/>
                  <label class="full" for="star4" title="그닥 재미없는 책이네요. 4점"></label>
                  <input v-model="score" type="radio" id="star3" name="score" value="3"/>
                  <label class="half" for="star3" title="별로 재미없어요! 3점"></label>
                  <input v-model="score" type="radio" id="star2" name="score" value="2"/>
                  <label class="full" for="star2" title="다신 안봐요. 2점"></label>
                  <input v-model="score" type="radio" id="star1" name="score" value="1"/>
                  <label class="half" for="star1" title="다시 보라면 당신을 한대 때리겠습니다. 1점"></label>
                </fieldset> -->
              </div>
              <textarea v-model="content" placeholder="리뷰를 입력해주세요."/>
              <div class="review-btn-group">
                <v-checkbox v-model="spoiler" label="스포일러 있음" class="ma-0 pa-0" color="warning" />
                <div @click="this.addBookReview" v-if="this.$store.state.user.isLogin" class="review-register">
                  <span v-if="!editMode">리뷰등록</span>
                  <span v-else>리뷰수정</span>
                </div>
              </div>
            </form>
          </div>
          <div class="review-contents">
            <div class="no-review-data" v-if="!myReview.length && !remainReview.length">
              <i class="fas fa-pencil-alt"></i>
              <p>작성된 리뷰가 없습니다.</p>
            </div>
            <div class="my-review-section px-3 mt-2" v-if="myReview.length">
              <div class="review-section-title mb-2">✏️ <span>내가 쓴 리뷰</span></div>
              <BookReview :review="myReview[0]" :index="0" @deleteSign="deleteSign" @toggleEditMode="toggleEditMode" />
            </div>
            <div class="review-section px-3 pb-3" style="width:95%;margin:0 auto" v-if="remainReview.length">
              <div class="review-section-title other-review my-2">
                <div>✏️ <span>다른 유저의 리뷰</span></div>
                <div class="sort-group">
                  <span @click="sortReview(0)">평점순</span>
                  <span @click="sortReview(1)">최신순</span>
                  <span @click="sortReview(2)">좋아요순</span>
                </div>
              </div>
              <div v-for="(review,index) in remainReview.slice((reviewPageNm - 1) * 5, reviewPageNm * 5)" :key="index">
                <BookReview :review="review" :index="(reviewPageNm - 1) * 5 + index" /> <!-- :index="(myReview.length ? index + 1 : index) + ((reviewPageNm - 1) * 5)" -->
              </div>
            </div>
            <div class="review-pagination" v-if="remainReview.length">
              <i :class="reviewPageNm === 1 ? 'fas fa-chevron-left limit-page-nm' : 'fas fa-chevron-left'" @click="changeReviewPageNm(-1)"></i>
              <span>{{ reviewPageNm }}</span>
              <span>/</span>
              <span>{{ parseInt(remainReview.length / 5) + (!(remainReview.length % 5) ? 0 : 1) }}</span>
              <i :class="reviewPageNm === parseInt(remainReview.length / 5) + (!(remainReview.length % 5) ? 0 : 1) ? 'fas fa-chevron-right limit-page-nm' : 'fas fa-chevron-right'" @click="changeReviewPageNm(1)"></i>
            </div>
          </div>
          <div class="review-form-title chart-title" v-if="myReview.length || remainReview.length">📊 평점 그래프</div>
          <div class="review-chart" v-if="myReview.length || remainReview.length">
            <Chart :chartData="this.stat" :chartLabels=[1,2,3,4,5,6,7,8,9,10] chartType="bar" style="width:95%;margin:0 auto"></Chart>
          </div>
        </div>
      </div>
      <div class="other-wrapper">
        <div class="other-title">
          <span class="other-alert">✔️ 이 도서는 어떠세요?</span>
          <i class="fas fa-undo" @click="getRecommendOtherBooks"></i>
        </div>
        <div class="other-books" v-if="!otherLoading">
          <div v-for="book in otherBooks" :key="book.id">
            <BookCard :bookData="book"/>
          </div>
        </div>
        <div class="other-books loading" v-else>
          <div class="service-logo">
            <img src="../../assets/images/team_logo/books.png" alt="team-logo">
          </div>
          <div class="loading-message">데이터를 불러오는 중 입니다.</div>
        </div>
      </div>
    </div>
    <div class="loading" v-else>
      <div class="service-logo">
        <img src="../../assets/images/team_logo/books.png" alt="team-logo">
      </div>
      <div class="loading-message">데이터를 불러오는 중 입니다.</div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import BookReview from '@/components/Books/BookReview'
import BookCard from '@/components/Books/BookCard'
import Chart from '@/components/common/Chart'
import { fetchjjim } from '@/api/index.js'

export default {
  name : "BookDetail",
  components : {
    BookReview,
    Chart,
    BookCard
  },
  data() {
    return {
      spoiler : false,
      book: {},
      content : '',
      score : 0,
      id :this.$route.params.id,
      like : 0,
      stat : [0,0,0,0,0,0,0,0,0,0],
      time : 0,
      loadingStatus: false,
      myReview: [],
      remainReview: [],
      reviewPageNm: 1,
      editMode: 0,
      editReviewPK: 0,
      otherBooks: [],
      otherLoading: false
    }
  },
  computed: {
    ...mapGetters(['info'])
  },
  created() {
    this.loadingStatus = true
    this.getBookDetail(this.id)
    this.getRecommendOtherBooks()
  },
  methods : {
    async getBookDetail(id) {
      let bookData = await this.$store.dispatch('GET_BOOK_DETAIL', id)
      this.book = bookData.results[0]
      let reviewData = this.book.review_set
      for (let i = 0; i < reviewData.length; ++i) {
        if (reviewData[i].username === this.info.username) {
          this.myReview = reviewData.splice(i, i + 1)
          this.remainReview = reviewData
          this.loadingStatus = false
          return
        }
      }
      this.remainReview = reviewData
      this.loadingStatus = false
    },
    async addBookReview() {
      if (this.time == 0){
        if (this.score && this.content){
          const formData = new FormData()
          formData.append('user', this.$store.getters.info.user_id)
          formData.append('content',this.content)
          formData.append('score',this.score * 2)
          formData.append('book',this.id)
          formData.append('spoiler',this.spoiler)
          if (!this.editMode) {
            await this.$store.dispatch('ADD_REVIEWS', formData)
            this.getBookDetail(this.id)
          } else {
            await this.$store.dispatch('EDIT_REVIEWS', [this.editReviewPK, formData])
            this.getBookDetail(this.id)
          }
          this.editMode = 0
          this.initForm()
          this.time = 5
        } else {
          alert('평점과 리뷰 내용을 작성해주세요')
        }
      } else {
        alert(this.time + '초 후에 시도해 주세요')
      }
      this.timego()
    },
    getRandomIntInclusive(min, max) {
      min = Math.ceil(min)
      max = Math.floor(max)
      return Math.floor(Math.random() * (max - min + 1)) + min
    },
    async getRecommendOtherBooks() {
      this.otherLoading = true
      this.otherBooks = []
      let otherBooks = []
      let data = await this.$store.dispatch('GET_RECOMMEND_OTHER_BOOKS', {other_books: this.id, page: 1})
      let pageMax = parseInt(data.count / 10) === 0 ? 1 : parseInt(data.count / 10) + (data.count % 10 === 0 ? 0 : 1)
      let adjustPageMax = pageMax <= 5 ? pageMax : 6
      for (let i = 1; i < adjustPageMax; ++i) {
        let data = await this.$store.dispatch('GET_RECOMMEND_OTHER_BOOKS', {other_books: this.id, page: i})
        otherBooks.push(...data.results)
      }
      let idxGroup = []
      while (idxGroup.length < 12) {
        let randomIdx = this.getRandomIntInclusive(0, otherBooks.length - 1)
        if (!idxGroup.includes(randomIdx)) {
          idxGroup.push(randomIdx)
          this.otherBooks.push(otherBooks[randomIdx])
        }
      }
      this.otherLoading = false
    },
    initForm() {
      this.content = ''
      this.score = 0
    },
    timego(){
      setTimeout(() => {
        if (this.time){
          this.time = this.time -1
          this.timego()
        }
      },1000)
    },
    deleteSign() {
      this.myReview = []
    },
    async jjim() {
      const formData = new FormData()
      formData.append('user', this.$store.getters.info.user_id)
      formData.append('book',this.id)
      const data = await fetchjjim(formData)
      this.book.my = !this.book.my
    },
    changeReviewPageNm(val) {
      let condition = (this.reviewPageNm < parseInt(this.remainReview.length / 5) + (!(this.remainReview.length % 5) ? 0 : 1) && val === 1)
                      || (this.reviewPageNm > 1 && val === -1)
      if (condition) {
        this.reviewPageNm += val
      }
    },
    toggleEditMode(reviewData) {
      this.editMode = 1
      this.score = reviewData.score / 2
      this.content = reviewData.content
      this.editReviewPK = reviewData.id
      this.spoiler = reviewData.spoiler
    },
    async sortReview(val) {
      await this.getBookDetail(this.id)
      await this.sortFunc(val)
    },
    sortFunc(val) {
      let data = this.remainReview
      switch (val) {
        case 0: // 평점순
          this.remainReview = data.sort((a, b) => b.score - a.score)
          this.reviewPageNm = 1
          break
        case 1: // 최신순
          this.remainReview = data.sort((a, b) => Date.parse(b.updated_at) - Date.parse(a.updated_at))
          this.reviewPageNm = 1
          break
        case 2: // 좋아요순
          this.remainReview = data.sort((a, b) => b.like_user.length - a.like_user.length)
          this.reviewPageNm = 1
          break
      }
    }
  },
  watch : {
    book : function () {
      this.stat = [0,0,0,0,0,0,0,0,0,0]
      const reviews = this.myReview.concat(this.remainReview)
      for (var i in reviews) {
        this.stat[reviews[i].score-1] ++ 
      }
    }
  }
}
</script>

<style scoped>
a {
  color: black;
  text-decoration: none;
}
.book-detail-wrapper {
  width: 80%;
  margin: 10px auto;
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 16px;
}

@media (max-width: 1100px) {
  .book-detail-wrapper {
    display: block;
  }
}

.book-header,
.book-basic-info,
.jjim-btn {
  font-family: 'Noto Sans KR';
}

.book-header {
  padding-bottom: 20px;
  margin-bottom: 40px;
  border-bottom: 9px dashed #eee;
}

.book-header .book-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 6px;
}

@media (max-width: 600px) {
  .book-header .book-title {
    font-size: 20px;
  }
}

.book-header .book-score {
  font-size: 17px;
}

.book-score:before {
  content: '★';
  color: #f9d71c;
}

.book-basic-info {
  display: grid;
  grid-template-columns: 1fr 3fr;
  gap: 6px;
}

.book-cover-img > img {
  vertical-align: top;
  width: 90%;
  margin-right: 10px;
}

.book-more-info {
  display: table;
  height: 100%;
}

.more-row {
  display: table-row;
}

.more-cell {
  display: table-cell;
  vertical-align: middle;
  font-size: 17px;
}

@media (max-width: 600px) {
  .book-basic-info {
    display: block;
  }

  .book-cover-img > img {
    margin: 0 auto;
    width: 65%;
  }

  .more-cell {
    font-size: 15px;
    display: table-cell;
    padding: 6px 0;
  }

  .book-detail-wrapper {
    width: 90%;
  }
}

.more-row > .more-cell:first-child {
  width: 33%;
  min-width: 110px;
}

.author-link {
  font-weight: 600;
  color: #007aff;
}

.like-btn {
  padding-bottom: 40px;
  margin-bottom: 20px;
  border-bottom: 9px dashed #eee;
}

.like-content {
  display: inline-block;
  width: 100%;
  font-size: 18px;
  text-align: center;
}

.like-content .btn-secondary {
  display: block;
  margin: 20px auto 0;
  text-align: center;
  background: #ed2553;
  border-radius: 3px;
  box-shadow: 0 10px 20px -8px rgb(240, 75, 113);
  padding: 9px 17px;
  font-size: 18px;
  font-family: 'Noto Sans KR';
  cursor: pointer;
  border: none;
  outline: none;
  color: #ffffff;
  text-decoration: none;
  -webkit-transition: 0.3s ease;
  transition: 0.3s ease;
}

.like-content .btn-secondary:hover {
  transform: translateY(-3px);
}

.like-content .btn-secondary .fa {
  margin-right: 5px;
}

.book-detail-card-title {
  font-family: 'Noto Sans KR';
  font-weight: 600;
}

.review-box {
  border: 1px solid silver;
  border-radius: 20px;
  padding: 10px;
  background-color: #fff;
}

.review-form-title {
  font-family: 'Noto Sans KR';
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 8px;
  width: 90%;
  margin: 0 auto;
  clear: both;
}

.review-form-title.main-title {
  margin-bottom: 18px;
}

.review-form-title.chart-title {
  padding-bottom: 18px;
}

.star-score {
  text-align: right;
}

.score-text {
  font-size: 15px;
  vertical-align: middle;
}

.score {
  border: none;
  padding-bottom: 0.5em;
}

.score > input {
  display: none;
  margin-right:1rem;
}

.score > label {
  float: right;
  transition: 0.15s;
}

.score > label:before {
  font-size: 1em;
  margin-bottom: .5rem;
  display: inline-block;
  padding: .3rem .2rem;
  margin: 0;
  cursor: pointer;
  font-family: FontAwesome;
  content: "\f006";
}

.score > .half:before {
  content: "\f089";
  position: absolute;
}

.score > label {
  color: grey;
  float: right;
}

.score > input:checked ~ label,
.score:not(:checked) > label:hover,
.score:not(:checked) > label:hover ~ label {
  color: #f9d71c;
}

.score > input:checked + label:hover,
.score > input:checked ~ label:hover,
.score > label:hover ~ input:checked ~ label,
.score > input:checked ~ label:hover ~ label {
  color:#f9d71c;
}

textarea {
  background-color: white;
  border: 1px solid silver;
  display: block;
  width: 90%;
  margin: 0 auto;
  height: 100px;
  font-size: 15px;
  padding: 4px;
  box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.15);
  font-family: 'Gothic A1';
}

.review-btn-group {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  width: 90%;
  margin: 20px auto 0;
}

.review-register{
  transform: translateY(0);
  transition: all .2s;
}

.review-register > span {
  padding: 4px 6px;
  border: 1px solid silver;
  border-radius: 6px;
  font-family: 'Gothic A1';
  background-color: rgba(0, 0, 0, 0.03);
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.05);
}

.review-register:hover {
  cursor: pointer;
  transform: translateY(-5%);
}

.review-register:hover > span {
  box-shadow: 3px 3px 6px rgba(0, 0, 0, 0.15);
}

.review-section-title {
  font-size: 16px;
  font-weight: 600;
  font-family: 'Gothic A1';
  display: inline-block;
}

.review-section-title > span,
.review-section-title.other-review > div:first-child > span:first-child {
  padding-bottom: 3px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.review-section-title.other-review {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  align-items: center;
}

.review-section-title.other-review .sort-group {
  font-size: 14px;
}

.review-section-title.other-review .sort-group > span {
  font-weight: 500;
}

.review-section-title.other-review .sort-group > span:not(:first-child) {
  padding-left: 8px;
}

.review-section-title.other-review .sort-group > span:hover {
  cursor: pointer;
  font-weight: 600;
}

.no-review-data {
  clear: both;
  text-align: center;
}

.no-review-data > i {
  font-size: 100px;
  color:rgba(0, 0, 0, 0.7);
}

.no-review-data > p {
  font-family: 'Gothic A1';
  font-weight: 600;
  margin: 16px 0 8px;
}

.my-review-section {
  clear: both;
  width: 95%;
  margin: 0 auto;
}

.review-section {
  clear: both;
}

.review-pagination {
  text-align: center;
  letter-spacing: 0.3em;
  font-weight: 600;
  font-family: 'Gothic A1';
  margin-bottom: 8px;
}

.review-pagination > i {
  padding: 0 8px;
}

.review-pagination > i:not(.limit-page-nm) {
  cursor: pointer;
}

.fas.limit-page-nm {
  color: lightgray;
}

.star-score,
.review-chart {
  width: 90%;
  margin: 0 auto;
}

.loading {
  margin: 0 auto;
}

.service-logo {
  text-align: center;
}

.service-logo img {
  margin: 34px 0;
  width: 200px;
  height: 200px;
}

.loading-message {
  font-family: 'Noto Sans KR';
  font-size: 18px;
  font-weight: 600;
  text-align: center;
}
.book-detail-contents{
  color:rgb(65, 65, 65) !important;
  line-height: 1.8em;
}

.other-wrapper {
  grid-column: 1 / 3;
  grid-row : 2 / 3;
}

.other-title {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  margin: 20px 0;
}

.other-books {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(25%, auto));
}

.other-books.loading {
  display: block;
}

.other-alert {
  font-size: 22px;
  font-weight: 600;
  font-family: 'Noto Sans KR';
}

.fa-undo {
  padding: 8px;
  font-size: 15px;
  border: 1px solid silver;
  border-radius: 10px;
  background-color: rgba(0, 0, 0, 0.07);
  box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.15);
}

.fa-undo:hover {
  cursor: pointer;
}

.fa-undo:after {
  content: ' 새로고침';
  font-family: 'Gothic A1';
}

@media (max-width: 1264px) {
  .other-books {
    grid-template-columns: repeat(auto-fill, minmax(33.33333%, auto));
  }
}
@media (max-width: 960px) {
  .other-books {
    grid-template-columns: repeat(auto-fill, minmax(50%, auto));
  }
}
@media (max-width: 600px) {
  .other-books {
    grid-template-columns: repeat(auto-fill, minmax(100%, auto));
  }

  .other-alert {
    font-size: 19px;
  }

  .fa-undo {
    font-size: 14px;
    padding: 6px;
  }
}
</style>