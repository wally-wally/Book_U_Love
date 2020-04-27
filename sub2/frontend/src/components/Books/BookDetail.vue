<template>
  <div class="book-deatil-wrapper row mt-5">
    <div class="bookdetail" v-if="!loadingStatus">
      <div class="ctr-80">
        <div>
          <span class="booktitle">{{book.title}}</span>
          <a href="/#" class="pr-5"><img src="//image.aladin.co.kr/img/shop/2018/icon_top_search.png" style="margin-bottom:-4px;"></a>
          {{book.categoryname}}
        </div>
        <div class="rating my-4 py-3">
          <span style="color:#f9d71c">★</span>{{book.avg}} ({{book.review_cnt}}명)
        </div>
          <div class="row detailbody pb-10">
            <div class="col-4">
              <img style="width:70%" :src="book.coverLargeUrl" :title="book.title" :alt="book.title">
            </div>
            <div class="col-8 row">
              <!-- <div class="col-2">Description</div><div class="col-10">{{book.description}} </div> -->
              <div class="col-2">Author</div>
                <div class="col-10">
                <router-link  v-for="author in book.author" :key="author.id" :to="`/author/${author.id}`">
                  {{author.name}}
                </router-link>
              </div>
              <div class="col-2">Publisher</div><div class="col-10">{{book.publisher}} </div>
              <div class="col-2">Publish Date</div><div class="col-10">{{book.pubDate.slice(0,4)}}.{{book.pubDate.slice(4,6)}}.{{book.pubDate.slice(6,8)}}</div>
              <div class="col-2">Price</div><div class="col-10">{{book.priceStandard}}원 </div>
            </div>
          </div>
          <div v-if="this.$store.state.user.isLogin" @click="this.jjim" style="margin-bottom:40px">
              <!-- <i class="fas fa-bookmark mr-5" style="font-size:20px; color:#fff;"></i>
              <div v-if="book.my" class="jjimtxt">
                찜에서 제거
              </div>
              <div v-else class="jjimtxt">
                책 추가하기
              </div> -->
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
          <v-card v-if="book.description" class="ctr-80 mb-5" style="width:100%;">
            <v-card-title class="pt-10 pb-10 book-sub" style="text-align:center;">
            책소개
            </v-card-title>
            <v-card-text v-html="book.description" style="text-align:center;padding:0 4em 2em 4em;">
            </v-card-text>
          </v-card>
          <v-card v-if="book.contents" class="ctr-80 mt-5 mb-5" style="width:100%;">
            <v-card-title class="pt-10 pb-10 book-sub" style="text-align:center;">
            목차
            </v-card-title>
            <v-card-text style="padding:0 3em 2em 3em;">
            <div v-html="book.contents"></div>
            </v-card-text>
          </v-card>
      </div>
    </div>

    <div class="review" v-if="!loadingStatus">
      <div class="py-5 reviewbox">
        <h2 class="pt-3 review-title">도서 리뷰</h2>
        <input type="text" v-model="this.time" class="time-section">
          <form v-if="this.$store.state.user.isLogin && !myReview.length">
            <div class="row">
              <fieldset class="score" style="margin-left:7%">
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
            <textarea v-model="content" placeholder=" 리뷰를 입력해주세요."/> 
            <div @click="this.addBookReview" v-if="this.$store.state.user.isLogin" class="review-register"> 리뷰등록</div>
          </form>
          <div class="my-review-section px-3" v-if="myReview.length">
            <BookReview :review="myReview[0]" :index="0" @deleteSign="deleteSign" />
          </div>
          <div class="px-3 pb-3" style="width:95%;margin:0 auto" v-if="remainReview.length">
            <div v-for="(review,index) in remainReview" :key="index">
              <BookReview :review="review" :index="index + myReview.length ? 1 : 0"/>
            </div>
          </div>
        <h2 class="pt-3 review-title">평점 그래프</h2>
          <Chart :chartData="this.stat" :chartLabels=[1,2,3,4,5,6,7,8,9,10] chartType="bar" style="width:95%;margin:0 auto"></Chart>
      </div>
    </div>
    <div class="loading" v-if="loadingStatus">
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
    // stat() {
    //   for (review in book.review_set){
    //     this.stat[review.score] ++
    //     console.log(review.score)
    //   } 
    // },
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
    // async getBookReview(id) {
    //   const data = await this.$store.dispatch('GET_REVIEWS', id)
    //   this.reviews = data
    // },
    async addBookReview() {
      if (this.time == 0){
        if (this.score){
        const formData = new FormData()
        formData.append('user', this.$store.getters.info.user_id)
        formData.append('content',this.content)
        formData.append('score',this.score)
        formData.append('book',this.id)
        await this.$store.dispatch('ADD_REVIEWS',formData)
        this.getBookDetail(this.id)
        this.initForm()
        this.time = 5
        } else {
          alert('평점을 입력해주세요')
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
.book-detail-wrapper {
  width: 90%;
  margin: 0 auto;
}
.ctr-80 {
  margin: 0 auto;
  width: 85%;
}

.bookdetail {
  width : 66%
}
.review {
  width : 33%
}
@media (max-width: 1000px) {
.bookdetail {
  width : 100%;
}
.review {
  width : 80%;
  margin : 0 auto;
  margin-bottom : 10%
}
}
li {
  list-style: none;
}

.booktitle{
  font-size : 2rem;
  font-family: 'Noto Sans KR';
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

.review-input-box {
  border: 1px solid black;
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

.review-input-box{ border: 1px solid black; }

.jjim{
  width: 200px;
  height: 40px;
  background: #9779e7;
  border-radius: 6px;
  cursor: pointer;
  padding:10px;
  text-align:center;
  margin:0 0 20px 0
}

.jjimtxt{
  color:#fff;
  font-size: 17px;
  font-weight: 500;
  letter-spacing: -0.7px;
  line-height: 22px;
  text-align: center;
  display: inline-block;
}

.rating{
  font-size: 17px;
  font-weight: 400;
  letter-spacing: -0.7px;
  line-height: 22px;
  border-top:1px solid lightgray;
  border-bottom:1px solid lightgray;
}
.review-title{
  font-size: 1.5em;
  font-weight: bold;
  font-family: 'Noto Sans KR';
  margin-bottom: 0.5em;
  margin-left:5%;
}
.review-register{
  display:block;
  text-align:right;
  margin-right:5%;
  margin-top:0.4em;
}
.book-sub{
  font-size: 1.5em;
  font-weight: bold;
  font-family: 'Noto Sans KR';
  margin-left:1%;
}
.reviewbox{
  margin-right:50px;
  background-color:white;
  border-radius: 15px;
  border: 1px solid lightgray;
  box-shadow: 3px 5px 5px rgba(0, 0, 0, 0.05);
}
.like-content {
    display: inline-block;
    width: 100%;
    padding: 0 20px 0 0;
    font-size: 18px;
    border-bottom: 9px dashed #eee;
    text-align: center;
}
.like-content .btn-secondary {
    display: block;
    margin:0 auto 30px;
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
.animate-like {
    animation-name: likeAnimation;
    animation-iteration-count: 1;
    animation-fill-mode: forwards;
    animation-duration: 0.65s;
}

.time-section {
  display: none;
}

.my-review-section {
  width: 95%;
  margin: 0 auto;
  /* border-bottom: 1.5px dotted rgba(0, 0, 0, 0.1); */
}

textarea {
  background-color: white;
  border: 1px solid gray;
  display: block;
  width: 90%;
  margin-left: 5%;
  height: 100px;
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
}

@keyframes likeAnimation {
  0%   { transform: scale(30); }
  100% { transform: scale(1); }
}
</style>