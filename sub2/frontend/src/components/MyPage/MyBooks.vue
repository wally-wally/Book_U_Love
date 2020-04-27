<template>
  <div class="mybooks-wrapper">
    <div class="mybooks">My Books</div>
    <!-- 좋아하는 책 -->
    <div class="add-info">
      <div class="mybooks-sub">💜 내가 읽고 싶은 책</div>
      <div class="row dot-border" style="padding:15px" v-if="!loadingStatus.likes">
        <div v-for="l in likes.slice(10 * (likePageNm - 1), 10 * likePageNm)" :key="l.id" class="col-xl-3 col-lg-4 col-sm-6">
          <BookCard :bookData="l"/>
        </div>
        <v-pagination
          v-model="likePageNm"
          :length="likePageCount"
          :total-visible="7"
          circle
          color="grey"></v-pagination>
      </div>
      <div class="dot-border text-center" v-else>
        <div class="service-logo">
          <img src="../../assets/images/team_logo/books.png" alt="team-logo">
        </div>
        <div class="loading-message">데이터를 불러오는 중 입니다.</div>
      </div>
    </div>

      <!-- 리뷰 책 BookCard 고치면,  text-center옆에 row추가-->
    <div class="add-info">
      <div class="mybooks-sub">📝 내가 리뷰 남긴 책</div>
      <div class="text-center dot-border" v-if="!loadingStatus.reviews">
        <div class="myreview-table">
          <div class="myreview-trow">
            <div class="table-head myreview-thead myreview-tcell tcell-book">도서</div>
            <div class="table-head myreview-thead myreview-tcell tcell-score">내 평점 / 내 리뷰</div>
          </div>
          <div v-for="r in userinfo.review_set.slice(10 * (reviewPageNm - 1), 10 * reviewPageNm)" :key="r.id" class="myreview-trow">
            <BookCard class="myreview-tcell tcell-book" :bookData="r.book"/>
            <div class="myreview-tcell tcell-info">
              <div class="myscore">
                <div class="star-rating">
                  <v-rating
                    v-model="r.score"
                    background-color="orange lighten-3"
                    color="#EAA64F"
                    medium
                    half-increments
                    dense
                    :length="10"
                    :readonly="true"
                  ></v-rating>
                </div>
                <span>{{r.score}}</span></div>
              <div class="myreview myreview-content">{{r.content}}</div>
            </div>
            <!-- <div class="myscore myreview-tcell tcell-score">★{{r.score}}</div>
            <div class="myreview myreview-tcell tcell-review">
              <div class="myreview-content">{{r.content}}</div>
            </div> -->
          </div>
        </div>
        <div class="myreview-table-mobile">
          <div v-for="r in userinfo.review_set.slice(10 * (reviewPageNm - 1), 10 * reviewPageNm)" :key="r.id" class="mb-12">
            <BookCard :bookData="r.book"/>
            <div class="mobile-myreview-info">
              <div class="myscore">
                <div class="mobile-myscore-title">내 평점</div>
                <span>{{r.score}}</span>
              </div>
              <div class="myreview myreview-content">{{r.content}}</div>
            </div>
            <!-- <div class="myscore myreview-tcell tcell-score">★{{r.score}}</div>
            <div class="myreview myreview-tcell tcell-review">
              <div class="myreview-content">{{r.content}}</div>
            </div> -->
          </div>
        </div>
        <v-pagination
          v-model="reviewPageNm"
          :length="reviewPageCount"
          :total-visible="7"
          circle
          color="grey"></v-pagination>
      </div>
      <div class="dot-border text-center" v-else>
        <div class="service-logo">
          <img src="../../assets/images/team_logo/books.png" alt="team-logo">
        </div>
        <div class="loading-message">데이터를 불러오는 중 입니다.</div>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchMyInfo, mylike } from '@/api/index.js'
import BookCard from '@/components/Books/BookCard'

export default {
  components: {BookCard},
  data() {
    return {
      reviewPageNm: 1,
      reviewPageCount: 0,
      likePageNm: 1,
      likePageCount: 0,
      userinfo : {},
      likes : [],
      loadingStatus: {
        'likes': false,
        'reviews': false
      }
    }
  },
  created() {
    this.loadingStatus.likes = true
    this.loadingStatus.reviews = true
    this.myinfo()
    this.mylikes()
  },
  methods : {
    async myinfo() {
      const data = await fetchMyInfo()
      this.userinfo = data.data
      this.reviewPageCount = parseInt(this.userinfo.review_set.length / 10) + (this.userinfo.review_set.length % 10 === 0 ? 0 : 1)
      this.loadingStatus.reviews = false
    },
    async mylikes() {
      const data = await mylike()
      this.likes = data.data
      this.likePageCount = parseInt(this.likes.length / 10) + (this.likes.length % 10 === 0 ? 0 : 1)
      this.loadingStatus.likes = false
    },
    goToBookListTop() {
      window.scrollTo(0, 0)
    }
  },
  watch: {
    likePageNm() {
      this.goToBookListTop()
    }
  }
}
</script>

<style scoped>
.add-info{
  margin-bottom: 2em;
}
.mybooks-wrapper {
  margin: 0 auto;
  width: 70%;
}
.mybooks{
  font-size: 1.5em;
  font-weight: bold;
  font-family: 'Noto Sans KR';
  margin-bottom: 1.5em;
}
.mybooks-sub{
  font-family: 'Nanum Gothic';
  font-weight: 600;
  font-size: 1.1em;
  padding-bottom: 0.8em;
}
.dot-border{
  border: 2px dashed rgba(0, 0, 0, 0.17);
  border-radius: 20px;
  box-shadow: 3px 5px 5px rgba(0, 0, 0, 0.05);
}
.myreview{
  border-radius:5px;
  text-overflow: ellipsis;
  font-family: 'Nanum Gothic';
  font-weight: 600;
  /* padding:50px; */
}
.table-head{
  font-family: 'Nanum Gothic';
  font-weight: 600;
  font-size: 1.1em;
  padding-bottom: 0.8em;
}
.myscore{
  color:#ffa136;
  margin-bottom: 30px;
}

.myscore > span {
  font-size: 1rem;
  padding-left: 4px;
  vertical-align: middle;
}

.service-logo img {
  margin: 30px 0;
  width: 200px;
  height: 200px;
}

.loading-message {
  text-align: center;
  font-size: 18px;
  font-weight: 600;
  font-family: 'Noto Sans KR';
  padding-bottom: 30px;
}

@media (max-width: 900px) {
  .mybooks-wrapper {
    width: 95%;
    transform: translateX(0%);
  }
}

.myreview-table {
  display: table;
  width: 95%;
  margin: 10px auto;
}

.myreview-trow {
  display: table-row;
}

.myreview-tcell {
  display: table-cell;
  vertical-align: middle;
  padding-bottom: 15px;
}

.tcell-book {
  width: 30%;
}

.tcell-info {
  width: 70%;
  padding: 10px;
}

.myreview-content {
  background-color:#f6e9e6;
  padding: 30px 0;
  box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.15);
}

.star-rating {
  display: inline-block;
}

.myreview-table-mobile {
  display: none;
}

.mobile-myreview-info {
  display: flex;
  align-items: center;
}

.mobile-myreview-info > .myscore {
  display: block;
  margin-bottom: 0;
  width: 20%;
}

.mobile-myreview-info > .myscore > span {
  padding: 0;
}

.mobile-myscore-title {
  color: black;
  font-family: 'Nanum Gothic';
}

.mobile-myreview-info > .myreview {
  display: block;
  width: 80%;
}

@media (max-width: 700px) {
  .star-rating {
    display: none;
  }

  .myscore > span {
    font-size: 1.2rem;
  }

  .myscore > span:before {
    content: '★';
  }
}

@media (max-width: 600px) {
  .myreview-table {
    display: none;
  }

  .myreview-table-mobile {
    display: block;
  }
}
</style>