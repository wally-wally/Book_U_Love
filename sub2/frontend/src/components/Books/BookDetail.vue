<template>
  <div class="ctr-80">
    <div>
      <span class="booktitle">{{book.title}}</span>
      <a href="/#" class="pr-5"><img src="//image.aladin.co.kr/img/shop/2018/icon_top_search.png" style="margin-bottom:-4px;"></a>
      {{book.category}}
    </div>
    <hr>
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
      <v-card class="ctr-80" style="width:100%;">
        <v-card-title class="pt-10 pb-10" style="text-align:center;">
        Description
        </v-card-title>
        <v-card-text style="text-align:center;">
          {{book.description}}
        </v-card-text>
      </v-card>
                    {{myreview}}
    <form class="ml-4 row">
        <fieldset class="score col-3">
        <input v-model="myreview.score" type="radio" id="star10" name="score" value="10"/>
        <label class="full" for="star10" title="최고의 책입니다. 10점"></label>
        <input v-model="myreview.score" type="radio" id="star9" name="score" value="9"/>
        <label class="half" for="star9" title="훌륭한 책입니다. 9점"></label>
        <input v-model="myreview.score" type="radio" id="star8" name="score" value="8"/>
        <label class="full" for="star8" title="괜찮은 책입니다. 8점"></label>
        <input v-model="myreview.score" type="radio" id="star7" name="score" value="7"/>
        <label class="half" for="star7" title="적당한 책입니다. 7점"></label>
        <input v-model="myreview.score" type="radio" id="star6" name="score" value="6"/>
        <label class="full" for="star6" title="음... 6점"></label>
        <input v-model="myreview.score" type="radio" id="star5" name="score" value="5"/>
        <label class="half" for="star5" title="나름 읽을만했어요 5점"></label>
        <input v-model="myreview.score" type="radio" id="star4" name="score" value="4"/>
        <label class="full" for="star4" title="그닥 재미없는 책이네요. 4점"></label>
        <input v-model="myreview.score" type="radio" id="star3" name="score" value="3"/>
        <label class="half" for="star3" title="별로 재미없어요! 3점"></label>
        <input v-model="myreview.score" type="radio" id="star2" name="score" value="2"/>
        <label class="full" for="star2" title="다신 안봐요. 2점"></label>
        <input v-model="myreview.score" type="radio" id="star1" name="score" value="1"/>
        <label class="half" for="star1" title="다시 보라면 당신을 한대 때리겠습니다. 1점"></label>
    </fieldset>
    <input v-model="myreview.content" type="textaria" class="col-8"/>
    <div @click="this.addBookReview"> 리뷰등록</div>
  </form>
      <div v-for="(review,index) in reviews" :key="index">
        <BookReview :review="review" :index="index"/>
      </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import BookReview from '@/components/Books/BookReview'

export default {
  name : "BookDetail",
  components : {
    BookReview
  },
  data() {
    return {
      book: {},
      myreview : {
        content : '',
        score : 0
        },
      reviews : [{score:'9',content:'좋은책',username:'나나'},
      {score:'6',content:'6점정도면 딱이지',username:'뚜비'},
      ],
      id :this.$route.params.id
    }
  },
  created() {
    this.getBookDetail(this.$route.params.id)
  },
  methods : {
    async getBookDetail(id) {
      let bookData = await this.$store.dispatch('GET_BOOK_DETAIL', {id:id})
      this.book = bookData.results[0]
    },
    getBookReview(id) {
      let reviews = this.$store.dispatch('GET_REVIEWS', id)
      this.reviews = reviews
    },
    async addBookReview() {
      console.log('review')
      const data = await this.$store.dispatch('ADD_REVIEWS',
      {
        id : this.id,
        data : {
          content: this.myreview.content,
          score : this.myreview.score
        }
      })
      console.log(data)
    }
  }
}
</script>

<style scoped>
.ctr-80 {
  margin: 0 auto;
  width: 60%;
}

li {
  list-style: none;
}

.booktitle{
  font-size : 2rem;
}

.score {
  border: none;
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
  content: "\f005 ";
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
  color: rgb(255, 228, 73);
}

.score > input:checked + label:hover,
.score > input:checked ~ label:hover,
.score > label:hover ~ input:checked ~ label,
.score > input:checked ~ label:hover ~ label {
  color: rgb(255, 220, 24);
}
</style>