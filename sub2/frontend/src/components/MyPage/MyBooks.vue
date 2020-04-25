<template>
  <div class="mybooks-wrapper">
    <div class="mybooks">My Books</div>
    <!-- 좋아하는 책 -->
    <div class="add-info">
      <div class="mybooks-sub">💜 내가 읽고 싶은 책</div>
      <div class="text-center row dot-border" style="padding:15px">
        <div v-for="l in likes" :key="l.id">
          <BookCard class="col-10" :bookData="l"/>
        </div>
      </div>
    </div>

      <!-- 리뷰 책 BookCard 고치면,  text-center옆에 row추가-->
    <div class="add-info">
      <div class="mybooks-sub">📝 내가 리뷰 남긴 책</div>
      <div class="text-center dot-border">
        <div class="row">
          <div class="table-head col-3">도서</div>
          <div class="table-head col-2">내 평점</div>
          <div class="table-head col-7">내 리뷰</div>
        </div>
        <div v-for="r in userinfo.review_set" :key="r.id" class="row">
            <BookCard class="col-3" :bookData="r.book"/>
            <div class="myscore col-1" style="margin:auto;">★{{r.score}}</div>
            <div class="myreview col-6" style="margin:auto;">{{r.content}}</div>
        </div>
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
      userinfo : {},
      likes : [],
    }
  },
  mounted() {
    this.myinfo()
    this.mylikes()
  },
  methods : {
    async myinfo() {
      const data = await fetchMyInfo()
      this.userinfo = data.data
    },
    async mylikes() {
      const data = await mylike()
      this.likes = data.data
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
</style>