<template>
  <div class="category-wrapper">
    <div class="category-header">
      <div>
        <div class="category-name my-2">
          {{ categoryName }}
        </div>
        <div class="book-count">
          총 {{ count }} 권의 책이 있습니다
        </div>
      </div>
      <div>
        <div class="sort-wrapper my-2">
          <div :class="sortItem === 'score' ? 'sort-item now-sort' : 'sort-item'" @click="getBookDetail('score')"><i class="fas fa-star" style="color: yellow"></i>평점순</div>
          <div :class="sortItem === 'count' ? 'sort-item now-sort' : 'sort-item'" @click="getBookDetail('count')"><i class="fas fa-user-edit" style="color: skyblue"></i>리뷰 개수순</div>
        </div>
        <!-- <div class="text-right">
          <v-rating v-model="reviewscore" color="orange" background-color="orange lighten-3" half-increments dense class="d-inline"></v-rating>({{ reviewscore * 2 }}점)
        </div> -->
      </div>
    </div>
    <div v-if="books.length && !loadingStatus">
      <div class="books-list">
        <div v-for="book in books" :key="book.id">
          <BookCard :bookData="book"/>
        </div>
      </div>
      <v-pagination
        v-model="pageNm"
        :length="pageCount"
        :total-visible="9"
        circle
        color="grey"
        class="my-4"></v-pagination>
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
import { filterCategoryBooks } from '@/api/index.js'
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
      categoryName: '',
      count : 0,
      sortItem: '',
      reviewscore: 0,
      mainCategoryID: 0,
      subCategoryID: 0,
      detailCategoryID: 0
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
      this.sortItem = sort
      const paramsData ={}
      if (sort) {
        this.pageNm = 1
        paramsData['sortby'] = sort
      }
      paramsData['page'] = this.pageNm
      paramsData[this.$route.name] = this.id
      // paramsData['reviewscore'] = this.reviewscore * 2 === 0 ? '' : this.reviewscore * 2
      if (this.$route.name.includes('category')) {
        paramsData['categorypage'] = 'categorypage'
      }
      let bookData = await this.$store.dispatch('GET_BOOKS', paramsData)
      this.books = bookData.results
      this.count = bookData.count
      this.pageCount = parseInt(bookData.count / 10) + (bookData.count % 10 === 0 ? 0 : 1)
      let pathUrl = this.$route.path
      const pageCategoryID = Number(pathUrl.split('/').reverse()[0])
      if (pathUrl.includes('category/main')) {
        let idx = this.categories.find(category => category.id === pageCategoryID).id
        this.categoryName = this.categories[idx - 1].name
        this.mainCategoryID = this.categories[idx - 1].id
      } else if (pathUrl.includes('category/sub')) {
        for (let i = 0; i < this.categories.length; ++i) {
          if (this.categories[i].subcategory_set.some(category => category.id === pageCategoryID)) {
            let subCategory_name = this.categories[i].subcategory_set.find(category => category.id === pageCategoryID).name
            this.subCategoryID = this.categories[i].subcategory_set.find(category => category.id === pageCategoryID).id
            this.categoryName = [this.categories[i].name, subCategory_name].join('>')
            break
          }
        }
      } else {
        let categorySet = bookData.results[0].categorylist
        let sliceIdx = this.$route.path.includes('category/main') ? 1 : this.$route.path.includes('category/sub') ? 2 : 3
        this.detailCategoryID = Number(this.$route.path.split('/')[3])
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
    async showSortBookData() {
      this.loadingStatus = true
      const paramsData ={}
      paramsData['sortby'] = this.sortItem
      paramsData['page'] = this.pageNm
      // paramsData['reviewscore'] = this.reviewscore * 2 === 0 ? '' : this.reviewscore * 2
      paramsData[this.$route.name] = this.id
      if (this.$route.name.includes('category')) {
        paramsData['categorypage'] = 'categorypage'
      }
      let bookData = await this.$store.dispatch('GET_BOOKS', paramsData)
      this.books = bookData.results
      this.loadingStatus = false
    },
    async higherThanBooks() {
      this.loadingStatus = true
      const paramsData ={}
      paramsData['maincategory'] = this.mainCategoryID
      paramsData['subcategory'] = this.subCategoryID
      paramsData['detailcategory'] = this.detailCategoryID
      paramsData['r_score'] = this.reviewscore * 2
      let bookData = await filterCategoryBooks(paramsData)
      console.log(bookData)
      this.loadingStatus = false
    }
  },
  watch: {
    '$route'() {
      this.id = this.$route.params.id
      this.pageNm = 1
      this.goToBookListTop()
      this.onBookDetail()
    },
    pageNm() {
      if (this.sortItem) {
        this.showSortBookData()
      } else {
        this.onBookDetail()
        this.goToBookListTop()
      }
    },
    reviewscore() {
      this.pageNm = 1
      this.higherThanBooks()
      // if (this.sortItem.length) {
      //   // this.showSortBookData()
      //   this.higherThanBooks()
      // } else {
      //   this.onBookDetail()
      //   this.goToBookListTop()
      // }
    }
  }
}
</script>

<style scoped>
.category-wrapper {
  width: 80%;
  margin: 0 auto;
}

.category-wrapper .category-header > div:first-child {
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

.sort-wrapper .sort-item.now-sort {
  font-weight: 600;
}

.category-book-cnt {
  font-family: 'Noto Sans KR';
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

.books-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(25%, auto));
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

  .category-wrapper {
    width: 90%;
  }
}
</style>
