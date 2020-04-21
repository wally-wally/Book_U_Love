<template>
  <div class="mybooks-wrapper">
    <div class="mybooks">My Books</div>
    <!-- 좋아하는 책 -->
    <div class="add-info">
      <div class="mybooks-sub">💜 내가 좋아요 누른 책</div>
      <div class="text-center row dot-border">
        <div v-for="l in likes" :key="l.id">
          <BookCard class="col-10" :bookData="l"/>
        </div>
      </div>
    </div>

      <!-- 리뷰 책 BookCard 고치면,  text-center옆에 row추가-->
    <div class="add-info">
      <div class="mybooks-sub">📝 내가 리뷰 남긴 책</div>
      <div class="text-center row dot-border" style="margin:0 auto">
        <div v-for="r in userinfo.review_set" :key="r.id">
          <BookCard class="col-10" :bookData="r.book"/>
          <div class="myreview"><span style="font-size:0.9em;">★{{r.score}} {{r.content}}</span></div>
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
    this.myinfo(this.$store.getters.info.user_id)
    this.mylikes()
  },
  methods : {
    async myinfo(id) {
      const data = await fetchMyInfo(id)
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
  display:inline-block;
  width:190px;
  background-color:#f6e9e6;
  text-overflow: ellipsis;
}
</style>