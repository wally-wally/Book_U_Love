<template>
    <div>
      <div class="page-description">
        🔖 연령대와 성별에 따른 동년배들의 리뷰가 많은 책들을 볼 수 있습니다
      </div>
      <div class="">
        <div class="d-flex">
          <v-select
          v-model="age"
          :items="ages"
          menu-props="auto" 
          label="연령대"
          class="mx-2"
          ></v-select>
          <v-select
          v-model="gender"
          :items="genders"
          menu-props="auto"
          class="mx-2"
          label="성별"
          ></v-select>
        </div>
        <div class="books-list">
            <div v-for="book in books" :key="book.id">
                <div class="book-box">
                    <BookCard :bookData="book[0]"/>
                    <v-chip color="error" class="mb-3">+ {{book[1]}} 개</v-chip>
                </div>
            </div>
        </div>

      </div>
    </div>
</template>

<script>
import { mapState } from 'vuex'
import { fetchReviewFilter } from '@/api/index.js'
import BookCard from '@/components/Books/BookCard'

export default {
  components : {BookCard},
  data() {
    return  {
      books : [],
      age : '전체',
      gender : '전체',
      ages : ['전체',10,20,30,40,50,60,70] ,
      genders : ['전체','남자','여자'],
      tableHeaders: [
        { text: '카테고리', value: 'book__detailCategory__name' },
        { text: '리뷰개수', value: 'id__count' },
      ],
      // chartID: -1
    }
  },
  created() {
    // this.resetChart()
    this.fetchMyInfo()
    this.getreviewfilter()
    // this.updateChart()
    // this.getData()
  },
  computed: {
    ...mapState({
      isLogin: state => state.user.isLogin
    })
  },
  watch : {
    age() {
      const params = {}
      if (this.gender != "전체") {
        params.gender = this.gender
      }
      if (this.age != "전체") {
        params.age = this.age
      }
      this.getreviewfilter(params)
      // this.resetChart()
    },
    gender(){ 
      const params = {}
      if (this.gender != "전체") {
        params.gender = this.gender
      }
      if (this.age != "전체") {
        params.age = this.age
      }
      this.getreviewfilter(params)
      // this.resetChart()
    }
  },
  methods : {
    // resetChart() {
    //   const canvasTag = document.querySelector('canvas')
    //   this.chartID += 1
    //   canvasTag.id = `barChart${this.chartID}`
    // },
    async fetchMyInfo() {
      if (this.isLogin) {
        const myInfo = await this.$store.dispatch('GET_MYINFO')
        this.gender = myInfo.gender === 'M' ? '남자' : '여자'
        this.age = parseInt(myInfo.age / 10) * 10
      }
    },
    async getreviewfilter(params) {
      const { data } = await fetchReviewFilter(params)
      this.books = data
    },
    goCategoryPage(data) {
      this.$router.push(`/category/detail/${data.book__detailCategory}/`)
    },
  }
}
</script>
<style scoped>
.page-description {
  font-size: 17px;
  font-family: 'Nanum Gothic';
  font-weight: 600;
  margin: 30px 0;
}

@media (max-width: 900px) {
  .page-description {
    font-size: 15px;
    margin-top: 10px;
  }
}

.books-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(20%, auto));
}

@media (max-width: 1264px) {
  .books-list {
    grid-template-columns: repeat(auto-fill, minmax(33.33333%, auto));
  }
}
@media (max-width: 960px) {
  .books-list {
    grid-template-columns: repeat(auto-fill, minmax(50%, auto));
  }
}
@media (max-width: 600px) {
  .books-list {
    grid-template-columns: repeat(auto-fill, minmax(100%, auto));
  }
}

.book-box {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.book-box > div:last-child {
    text-align: center;
}

.variable-count {
    font-weight: 600;
    font-family: 'Gothic A1';
}
</style>