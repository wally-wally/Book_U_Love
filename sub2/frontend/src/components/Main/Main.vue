<template>
  <div class="main-wrapper">
    <ImageSlider />
    <div class="my-6 main-contents">
      <div class="main-sidebar">
        <WeeklyAuthor />
        <BooksRanking />
      </div>
      <div class="main-book-section">
        <BooksHeader />
        <BooksList />
      </div>
    </div>
  </div>
</template>

<script>
import ImageSlider from '@/components/Main/ImageSlider'
import WeeklyAuthor from '@/components/Main/WeeklyAuthor'
import BooksRanking from '@/components/Main/BooksRanking'
import BooksHeader from '@/components/Main/BooksHeader'
import BooksList from '@/components/Main/BooksList'

export default {
  name: 'Main',
  components: {
    ImageSlider,
    WeeklyAuthor,
    BooksRanking,
    BooksHeader,
    BooksList
  }
}
</script>

<style scoped>
.main-wrapper {
  width: 90%;
  margin: 0 auto;
  box-sizing: border-box;
}

.main-contents {
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 4fr;
  gap: 0.75em;
}

.main-contents .main-sidebar {
  min-width: 250px;
}

@media (max-width: 800px) {
  .main-contents {
    display: block;
  }
}
</style>