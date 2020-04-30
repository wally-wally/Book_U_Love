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
          <div class="review-form-title">도서 리뷰</div>
          <div class="review-form">
            <input type="text" v-model="this.time" class="d-none">
            <form v-if="this.$store.state.user.isLogin && !myReview.length">
              <div class="star-score">
                <fieldset class="score">
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
                </fieldset>
              </div>
              <textarea v-model="content" placeholder="리뷰를 입력해주세요."/> 
              <v-checkbox v-model="spoiler" label="스포일러 있음" />
              <div @click="this.addBookReview" v-if="this.$store.state.user.isLogin" class="review-register"><span>리뷰등록</span></div>
            </form>
          </div>
          <div class="review-contents">
            <div class="my-review-section px-3" v-if="myReview.length">
              <BookReview :review="myReview[0]" :index="0" @deleteSign="deleteSign" />
            </div>
            <div class="review-section px-3 pb-3" style="width:95%;margin:0 auto" v-if="remainReview.length">
              <div v-for="(review,index) in remainReview" :key="index">
                <BookReview :review="review" :index="myReview.length ? index + 1 : index"/>
              </div>
            </div>
          </div>
          <div class="review-form-title">평점 그래프</div>
          <div class="review-chart">
            <Chart :chartData="this.stat" :chartLabels=[1,2,3,4,5,6,7,8,9,10] chartType="bar" style="width:95%;margin:0 auto"></Chart>
          </div>
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
import Chart from '@/components/common/Chart'
import { fetchjjim } from '@/api/index.js'

export default {
  name : "BookDetail",
  components : {
    BookReview,Chart
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
      remainReview: []
    }
  },
  computed: {
    ...mapGetters(['info'])
  },
  created() {
    this.loadingStatus = true
    this.getBookDetail(this.id)
  },
  watch : {
    book : function () {
      this.stat = [0,0,0,0,0,0,0,0,0,0]
      const reviews = this.myReview.concat(this.remainReview)
      for (var i in reviews) {
        this.stat[reviews[i].score-1] ++ 
      }
    }
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
          formData.append('score',this.score)
          formData.append('book',this.id)
          formData.append('spoiler',this.spoiler)
          await this.$store.dispatch('ADD_REVIEWS',formData)
          this.getBookDetail(this.id)
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
  grid-template-columns: 2fr 1fr;
  gap: 12px;
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
  font-size: 21px;
  font-weight: 600;
  margin-bottom: 6px;
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
  position: fixed;
  z-index: 10000;
  width: 24%;
  transform: translateX(8px);
  border: 1px solid silver;
  border-radius: 20px;
  padding: 10px;
  background-color: #fff;
}

.review-form-title {
  font-family: 'Noto Sans KR';
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 6px;
  width: 90%;
  margin: 0 auto;
}

@media (max-width: 1100px) {
  .review-box {
    position: static;
    width: 100%;
    z-index: 1;
    transform: translateX(0);
  }
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
  padding-right: 0;
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

.review-register{
  float: right;
  margin:0.8em 5% 0.8em 0;
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

.my-review-section {
  clear: both;
  width: 95%;
  margin: 0 auto;
}

.review-section {
  clear: both;
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
</style>