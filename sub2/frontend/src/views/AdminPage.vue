<template>
  <div class="admin-page-wrapper">
    <h2>Admin Page</h2>
    <UserList />
    <!-- <BookDataList /> -->
  </div>
</template>

<script>
import UserList from '@/components/Admin/UserList'
import BookDataList from '@/components/Admin/BookDataList'

export default {
  components: {
    UserList,
    BookDataList
  }
}
</script>

<style scoped>
.admin-page-wrapper {
  width: 80%;
  margin: 0 auto;
}

.admin-page-wrapper h2 {
  font-family: 'Quicksand';
  padding-bottom: 8px;
}
</style>