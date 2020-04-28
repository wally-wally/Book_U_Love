<template>
  <div class="category-wrapper">
    <div class="category-header">
      <div class="category-name my-2 pl-3">
        {{ categoryName }}
      </div>
      <div class="sort-wrapper my-2 pl-3">
        <div class="sort-item" @click="getBookDetail('score')">평점순</div>
        <div class="sort-item" @click="getBookDetail('count')">리뷰순</div>
      </div>
    </div>
    <div class="row" v-if="books.length && !loadingStatus">
      <div v-for="book in books" :key="book.id" class="books-list col-lg-3 col-md-4 col-sm-6">
        <BookCard :bookData="book"/>
      </div>
      <v-pagination
        v-model="pageNm"
        :length="pageCount"
        :total-visible="9"
        circle
        color="grey"
        class="mb-4"></v-pagination>
    </div>
    <div v-else-if="loadingStatus">
      <div class="service-logo">
        <img src="../../assets/images/team_logo/books.png" alt="team-logo">
      </div>
      <div class="loading-message">데이터를 불러오는 중 입니다.</div>
    </div>
    <div v-else class="no-category-books">
      <i class="fas fa-times d-block text-center"></i>
      <p>해당 카테고리의 도서가 없습니다.</p>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import BookCard from '@/components/Books/BookCard'

export default {
  name : "category",
  components: {
    BookCard
  },
  data() {
    return {
      id : this.$route.params.id,
      pageNm: 1,
      pageCount: 0,
      books : [],
      loadingStatus: false,
      categoryName: ''
    }
  },
  computed: {
    ...mapState({
      categories: state => state.data.categories
    })
  },
  created() {
    this.onBookDetail()
  },
  methods : {
    async getBookDetail(sort) {
      const paramsData ={}
      if (sort) {
        this.pageNm = 1
        paramsData['sortby'] = sort
      }
      paramsData['page'] = this.pageNm
      paramsData[this.$route.name] = this.id
      let bookData = await this.$store.dispatch('GET_BOOKS', paramsData)
      this.books = bookData.results
      this.pageCount = parseInt(bookData.count / 10) + (bookData.count % 10 === 0 ? 0 : 1)
      let pathUrl = this.$route.path
      const pageCategoryID = Number(pathUrl.split('/').reverse()[0])
      if (pathUrl.includes('category/main')) {
        let idx = this.categories.find(category => category.id === pageCategoryID).id
        this.categoryName = this.categories[idx - 1].name
      } else if (pathUrl.includes('category/sub')) {
        for (let i = 0; i < this.categories.length; ++i) {
          if (this.categories[i].subcategory_set.some(category => category.id === pageCategoryID)) {
            let subCategory_name = this.categories[i].subcategory_set.find(category => category.id === pageCategoryID).name
            this.categoryName = [this.categories[i].name, subCategory_name].join('>')
            break
          }
        }
      } else {
        let categorySet = bookData.results[0].categorylist
        let sliceIdx = this.$route.path.includes('category/main') ? 1 : this.$route.path.includes('category/sub') ? 2 : 3
        this.categoryName = categorySet.slice(0, sliceIdx).join(' > ')
      }
      this.loadingStatus = false
    },
    onBookDetail() {
      this.loadingStatus = true
      this.getBookDetail()
    },
    goToBookListTop() {
      window.scrollTo(0, 0)
    },
  },
  watch: {
    '$route'() {
      this.id = this.$route.params.id
      this.pageNm = 1
      this.goToBookListTop()
      this.onBookDetail()
    },
    pageNm() {
      this.onBookDetail()
      this.goToBookListTop()
    }
  }
}
</script>

<style scoped>
.category-wrapper {
  width: 90%;
  margin: 0 auto;
}

.category-wrapper .category-name {
  font-family: 'Noto Sans KR';
  font-weight: 600;
  font-size: 1.1em;
}

.category-header {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}

.sort-wrapper {
  font-family: 'Noto Sans KR';
  display: flex;
}

.sort-wrapper .sort-item:last-child {
  margin-left: 12px;
}

.sort-wrapper .sort-item:hover {
  cursor: pointer;
  font-weight: 600;
}

.no-category-books {
  font-family: 'Gothic A1';
  color: crimson;
}

.no-category-books i {
  font-size: 7em;
  margin: 0.2em 0;
}

.no-category-books > p {
  font-weight: 600;
  font-size: 1.1em;
  text-align: center;
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
  text-align: center;
  font-size: 18px;
  font-weight: 600;
  font-family: 'Noto Sans KR';
}
</style>
