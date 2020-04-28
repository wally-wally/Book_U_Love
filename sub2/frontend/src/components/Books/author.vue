<template>
  <div class="author_wrapper">
      <div class="author_intro">작가 소개</div>
      <hr>
      <div class="author_area_wrapper">
        <div class="author_profile">
          <div class="profile_right">
            <div class="author_name_wrapper">
              <h4 class="author_name">
                <router-link :to='`/author/${author.id}`'><span class="lang_kor">{{author.name}}</span></router-link>
              </h4>
            </div>
            <img style="width:200px;height:265px;" :src="this.imgUrl" alt="author-image">
            <ul class="profile_list_wrapper">
              <li class="profile_list list_birth ">
                <span class="list_title">출생</span>
                <span class="list_contents">{{author.boneDate}}<br>{{author.region}}</span>
              </li>
            </ul>
        </div>
      </div>
      <div class="author_biography">
        <p class="biography_paragraph ">{{author.name}}<br>{{author.description}}</p>
      </div>
    </div>
    <h4 class="header_title">총 종</h4>
    <div v-for="book in books" :key="book.id" class="row">
      <BookCard class="books-list col-lg-3 col-md-4 col-sm-6" :bookData="book"/>
    </div>
  </div>
</template>

<script>
import { fetchauthor } from '@/api/index.js'
import BookCard from '@/components/Books/BookCard'

export default {
    components: {BookCard},
    name  : 'author',
    data() {
        return {
            author: {},
            books : [],
        }
    },
    mounted() {
        this.getauthor(this.$route.params.id)
        this.getauthorbook(this.$route.params.id)
    },
    methods : {
      async getauthorbook(id) {
        let bookData = await this.$store.dispatch('GET_BOOKS', {author:id})
        this.books = bookData.results
      },
        async getauthor(id) {
            const data = await fetchauthor(id)
            console.log(data)
            this.author = data.data
        }
    },
    computed:{
      imgUrl(){
        let url = this.author.imgUrl
        let noImageCondition = [' ','http://bimage.interpark.com/bookpinion/add_images/noimg_70_98.gif']
        return noImageCondition.includes(url) ? require('../../assets/images/no_image/no_image.png') : url
      }
    }
}
</script>

<style>
.author_intro{
  font-size: 1.5em;
  font-weight: bold;
  font-family: 'Noto Sans KR';
  margin-bottom: 0.5em;
}
.author_wrapper{
  width:45%;
  margin:0 auto 30px;
}
.author_wrapper .author_area_wrapper {
  padding: 20px 20px 0 20px;
  border: 10px solid #eee;
  margin-top: 30px;
}
.author_wrapper .author_area_wrapper .author_profile .profile_right .author_name_wrapper .author_name .lang_kor {
  font-size: 20px;
  font-weight: 700;
  color: #333;
  word-break: break-all;
  line-height: 1.3em;
}
ul {
  list-style-type: none;
  margin: 10px 0;
  padding: 0;
}
.author_wrapper .author_area_wrapper .author_profile .profile_right .profile_list_wrapper .profile_list .list_title {
  display: table-cell;
  padding-right: 7px;
  width: 2em;
  font-size: 13px;
  color: #808991;
  line-height: 1.8em;
  white-space: nowrap;
}
.author_wrapper .author_area_wrapper .author_profile .profile_right .profile_list_wrapper .profile_list .list_contents {
  display: table-cell;
  font-size: 13px;
  color: #333;
  line-height: 1.8em;
}
.author_wrapper .author_area_wrapper .author_profile .profile_right .author_name_wrapper .author_name .lang_kor {
  font-size: 20px;
  font-weight: 700;
  color: #333;
  word-break: break-all;
  line-height: 1.3em;
}
.author_wrapper .author_area_wrapper .author_profile .profile_right .author_name_wrapper .author_name {
  display: inline-block;
  vertical-align: top;
  padding: 0 10px 17px 0;
}
.author_wrapper .author_area_wrapper .author_biography {
  padding: 20px 0;
}
.author_wrapper .author_area_wrapper .author_biography {
  border-top: 1px solid #eee;
}
.author_wrapper .author_area_wrapper .author_biography .biography_paragraph {
  line-height: 1.8em;
  font-size: 13px;
  color: #333;
  word-break: break-all;
}
.author_biography .biography_paragraph{
  color: #666;
  font-size: 12px;
  line-height: 1em;
  letter-spacing: -.03em;
  -webkit-font-smoothing: antialiased;
}
</style>