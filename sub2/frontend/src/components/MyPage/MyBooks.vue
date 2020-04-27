<template>
  <div class="mybooks-wrapper">
    <div class="mybooks">My Books</div>
    <!-- 좋아하는 책 -->
    <div class="add-info">
      <div class="mybooks-sub">💜 내가 읽고 싶은 책</div>
      <div class="text-center row dot-border" style="padding:15px" v-if="!loadingStatus.likes">
        <div v-for="l in likes.slice(10 * (likePageNm - 1), 10 * likePageNm)" :key="l.id">
          <BookCard class="col-10" :bookData="l"/>
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
        <div class="row">
          <div class="table-head col-3">도서</div>
          <div class="table-head col-2">내 평점</div>
          <div class="table-head col-7">내 리뷰</div>
        </div>
        <div v-for="r in userinfo.review_set.slice(10 * (reviewPageNm - 1), 10 * reviewPageNm)" :key="r.id" class="row">
          <BookCard class="col-3" :bookData="r.book"/>
          <div class="myscore col-1" style="margin:auto;">★{{r.score}}</div>
          <div class="myreview col-6" style="margin:auto;">{{r.content}}</div>
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
  background-color:#f6e9e6;
  text-overflow: ellipsis;
  font-family: 'Nanum Gothic';
  font-weight: 600;
  padding:50px;
}
.table-head{
  font-family: 'Nanum Gothic';
  font-weight: 600;
  font-size: 1.1em;
  padding-bottom: 0.8em;
}
.myscore{
  color:#ffa136;
  font-size: 1.3em;
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
</style>