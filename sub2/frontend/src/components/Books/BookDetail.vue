<template>
  <div class="row mt-5">
    <div class="bookdetail">
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
              <div class="col-2">Author</div><div class="col-10">{{book.author}} </div>
              <div class="col-2">Publisher</div><div class="col-10">{{book.publisher}} </div>
              <div class="col-2">Publish Date</div><div class="col-10">{{book.pubDate.slice(0,4)}}.{{book.pubDate.slice(4,6)}}.{{book.pubDate.slice(6,8)}}</div>
              <div class="col-2">Price</div><div class="col-10">{{book.priceStandard}}원 </div>
            </div>
          </div>
          <div v-if="this.$store.state.user.isLogin" @click="this.jjim" class="jjim">
              <i class="fas fa-bookmark mr-5" style="font-size:20px; color:#fff;"></i>
              <div v-if="book.my" class="jjimtxt">
                찜에서 제거
              </div>
              <div v-else class="jjimtxt">
                책 추가하기
              </div>
          </div>
          <v-card v-if="book.description" class="ctr-80 mb-5" style="width:100%;">
            <v-card-title class="pt-10 pb-10" style="text-align:center;">
            Description
            </v-card-title>
            <v-card-text v-html="book.description" style="text-align:center;">
            </v-card-text>
          </v-card>
          <v-card v-if="book.contents" class="ctr-80 mt-5 mb-5" style="width:100%;">
            <v-card-title class="pt-10 pb-10" style="text-align:center;">
            Contents
            </v-card-title>
            <v-card-text>
            <div v-html="book.contents"></div>
            </v-card-text>
          </v-card>
      </div>
    </div>

    <div class="review">
      <div class="py-5" style="margin-right:50px; background-color:white;border-radius: 15px; border: 1px solid lightgray">
        <h2 class="pt-3 review-title">도서 리뷰</h2>
          <form v-if="this.$store.state.user.isLogin">
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
            <textarea v-model="content" style="background-color:white; border:1px solid gray;display:block;width:90%;margin-left:5%;" placeholder=" 리뷰를 입력해주세요."/> 
            <div @click="this.addBookReview" v-if="this.$store.state.user.isLogin" class="review-register"> 리뷰등록</div>
          </form>
          <div class="px-3 py-3" style="width:95%;margin:0 auto">
            <div v-for="(review,index) in book.review_set" :key="index">
              <BookReview :review="review" :index="index"/>
            </div>
          </div>
        <h2 class="pt-3 review-title">평점 그래프</h2>
          <Chart :chartData="this.stat" :chartLabels=[0,1,2,3,4,5,6,7,8,9,10] chartType="bar"></Chart>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
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
      stat : [0,0,0,0,0,0,0,0,0,0,0]
    }
  },
  mounted() {
    this.getBookDetail(this.id)
  },
  watch : {
    book : function () {
      this.stat = [0,0,0,0,0,0,0,0,0,0,0]
      const reviews = this.book.review_set
      for (var i in reviews) {
        this.stat[reviews[i].score] ++ 
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
      console.log(bookData)
      this.book = bookData.results[0]
    },
    // async getBookReview(id) {
    //   const data = await this.$store.dispatch('GET_REVIEWS', id)
    //   this.reviews = data
    // },
    async addBookReview() {
      const formData = new FormData()
      formData.append('user', this.$store.getters.info.user_id)
      formData.append('content',this.content)
      formData.append('score',this.score)
      formData.append('book',this.id)
      await this.$store.dispatch('ADD_REVIEWS',formData)
      this.getBookDetail(this.id)
      this.initForm()
    },
    initForm() {
      this.content = ''
      this.score = 0
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
</style>