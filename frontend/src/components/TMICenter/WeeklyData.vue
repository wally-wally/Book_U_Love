<template>
  <div class="page-wrapper">
    <div class="page-description">
        🔖 이번주 가장 많은 리뷰가 작성된 책 TOP 10을 볼 수 있습니다.
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
</template>


<script>
import { fetchweekly } from '@/api/index.js'
import BookCard from '@/components/Books/BookCard'

export default {
    components : {BookCard},
    data() {
        return {
            books: []
        }
    },
    methods : {
        async getweekly(){
            const { data } = await fetchweekly()
            this.books = data.sort((a, b) => b[1] - a[1])
        }
    },
    mounted() {
        this.getweekly()
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