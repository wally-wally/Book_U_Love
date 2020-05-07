<template>
  <div>
    <div class="book-swiper-title">
      <span v-if="this.theme === 'favoriteCategory'">🔖{{ `${this.info.username}님을 위한 맞춤 추천 도서` }}</span>
      <span v-else-if="this.theme === 'age_gender'">🔖{{ `${age} ${gender} 추천 도서` }}</span>
      <span v-else-if="this.theme === 'sortScore'">🔖평점순 TOP 10 도서</span>
      <span v-else>🔖리뷰 개수순 TOP 10 도서</span>
    </div>
    <swiper v-if="!loadingStatus && books.length" ref="mySwiper" :options="swiperOptions" class="swiper-wrapper">
      <swiper-slide v-for="(book, idx) in books" :key="idx">
        <BookCard :bookData="book" />
      </swiper-slide>
      <div class="swiper-pagination" slot="pagination"></div>
      <div class="swiper-button-next" slot="navigation"></div>
      <div class="swiper-button-prev" slot="navigation"></div>
    </swiper>
    <div v-else>
      <div class="service-logo">
        <img src="../../assets/images/team_logo/books.png" alt="team-logo">
      </div>
      <div class="loading-message">
        <span v-if="loadingStatus">데이터를 불러오는 중 입니다.</span>
        <span v-else>해당 데이터가 없습니다.<br>관심 카테고리 설정과 리뷰를 많이 작성해주시면<br>{{ this.info.username }}님을 위한 맞춤 도서를 추천해드릴께요!</span>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import { recommend } from '@/api/index.js'
import BookCard from '@/components/Books/BookCard'

export default {
  props: {
    theme: {
      type: String
    }
  },
  components: {
    BookCard
  },
  data() {
    return {
      swiperOptions: {
        slidesPerView: 1,
        spaceBetween: 5,
        loop: true,
        loopFillGroupWithBlank: true,
        pagination: {
          el: '.swiper-pagination',
          clickable: true,
        },
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev',
        },
        breakpoints: {
          0: {
            slidesPerView: 1,
            spaceBetween: 0,
          },
          550: {
            slidesPerView: 2,
            spaceBetween: 0,
          },
          970: {
            slidesPerView: 4,
            spaceBetween: 0,
          },
          1300: {
            slidesPerView: 6,
            spaceBetween: 0,
          },
        }
      },
      gender: '',
      age: '',
      books: [],
      loadingStatus: false
    }
  },
  computed: {
    ...mapState({
      isLogin: state => state.user.isLogin
    }),
    ...mapGetters(['info']),
    swiper() {
      return this.$refs.mySwiper.$swiper
    }
  },
  created() {
    this.getBooks()
  },
  methods: {
    getBooks() {
      this.loadingStatus = true
      if (this.isLogin && this.theme === 'age_gender') {
        this.fetchMyInfo()
      }
      this.getBooksData()
    },
    async fetchMyInfo() {
      const myInfo = await this.$store.dispatch('GET_MYINFO')
      this.gender = myInfo.gender === 'M' ? '남성' : '여성'
      this.age = parseInt(myInfo.age / 10).toString() + '0대'
    },
    async getBooksData() {
      if (this.theme === 'sortScore') {
        let scoredata = await this.$store.dispatch('GET_BOOKS', {sortby: "score",top:10})
        this.books = scoredata["results"]
        this.loadingStatus = false
        return
      } else if (this.theme === 'sortReviewCnt') {
        let reviewdata =  await this.$store.dispatch('GET_BOOKS', {sortby: "count",top:10})
        this.books = reviewdata["results"]
        this.loadingStatus = false
        return
      } else if (this.theme === 'favoriteCategory') {
        let bookdata = await this.$store.dispatch('GET_RECOMMEND_BOOKS')
        this.books = bookdata
        this.loadingStatus = false
        return
      }
    },
    // async shuffleBooks() {
    //   this.loadingStatus = true
    //   this.books = []
    //   await this.getBooksData()
    //   await this.shuffle()
    // },
    // getRandomIntInclusive(min, max) {
    //   min = Math.ceil(min)
    //   max = Math.floor(max)
    //   return Math.floor(Math.random() * (max - min + 1)) + min
    // },
    // shuffle() {
    //   let idxGroup = []
    //   let bookData = []
    //   while (idxGroup.length < 10) {
    //     let randomIdx = this.getRandomIntInclusive(0, 9)
    //     if (!idxGroup.includes(randomIdx)) {
    //       idxGroup.push(randomIdx)
    //       bookData.push(this.books[randomIdx])
    //     }
    //   }
    //   this.books = bookData
    //   this.loadingStatus = false
    // }
  },
  filters: {
    filteredAuthor(author) {
      if (!author.length) {
        return '작가 미등록'
      } else {
        let authorCnt = author.length
        let firstAuthorName = author[0].name
        return firstAuthorName + (authorCnt >= 2 ? ` 외 ${authorCnt - 1}명` : '')
      }
    }
  }
}
</script>

<style scoped>
.service-logo {
  text-align: center;
}

.service-logo img {
  margin: 30px 0 20px;
  width: 150px;
  height: 150px;
}

.loading-message {
  text-align: center;
  font-size: 18px;
  font-weight: 600;
  font-family: 'Noto Sans KR';
  margin-bottom: 40px;
}

.book-swiper-title {
  font-family: 'Gothic A1';
  font-weight: 600;
  font-size: 17px;
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}

.swiper-wrapper {
  padding-bottom: 40px;
  margin-bottom: 40px;
}

.swiper-pagination {
  bottom: 0;
}

.swiper-pagination-bullet {
  width: 20px;
  height: 20px;
  text-align: center;
  line-height: 20px;
  font-size: 12px;
  color:#000;
  opacity: 1;
  margin: 0 20px;
  background: rgba(0,0,0,0.2);
}

.swiper-pagination-bullet-active {
  color:#fff;
  background: #007aff;
}

.swiper-slide {
  text-align: center;
  font-size: 18px;
  display: -webkit-box;
  display: -ms-flexbox;
  display: -webkit-flex;
  display: flex;
  -webkit-box-pack: center;
  -ms-flex-pack: center;
  -webkit-justify-content: center;
  justify-content: center;
  -webkit-box-align: center;
  -ms-flex-align: center;
  -webkit-align-items: center;
  align-items: center;
}

.fa-undo {
  padding: 0 8px;
  font-size: 15px;
  border: 1px solid silver;
  border-radius: 10px;
  background-color: rgba(0, 0, 0, 0.07);
  box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.15);
  line-height: 1.5;
}

.fa-undo:hover {
  cursor: pointer;
}

.fa-undo:after {
  content: ' 새로고침';
  font-family: 'Gothic A1';
}

@media (max-width: 500px) {
  .book-swiper-title {
    font-size: 15px;
  }

  .loading-message > span,
  .fa-undo {
    font-size: 13px;
  }
}
</style>