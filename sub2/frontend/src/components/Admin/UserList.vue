<template>
  <div class="mt-3 mb-6">
    <v-data-table
      :headers="tableHeaders"
      :items="users"
      :items-per-page="itemsPerPage"
      :page.sync="page"
      item-key="noticeIdx"
      hide-default-footer
      color="#E6CC00"
      @page-count="pageCount = $event"
      class="elevation-1">
      <template v-slot:item.gender="{ item }">
        {{ item.gender | filteredGender }}
      </template>
      <template v-slot:item.categorys="{ item }">
        {{ item.categorys | firstCategory }}
      </template>
    </v-data-table>
    <div class="text-center pt-2">
      <v-pagination v-model="page" :length="parseInt(userCount / 10) + (userCount / 10 === 0 ? 0 : 1)" :total-visible="7" circle color="#E6CC00"></v-pagination>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      users: [],
      userCount: 0,
      tableHeaders: [
        { text: '이름', value: 'username' },
        { text: '나이', value: 'age' },
        { text: '성별', value: 'gender' },
        { text: 'e-mail', value: 'email' },
        { text: '관심 카테고리', value: 'categorys' }
      ],
      page: 1,
      pageCount: parseInt(this.userCount / 10) + (this.userCount / 10 === 0 ? 0 : 1),
      itemsPerPage: 10,
    }
  },
  created() {
    this.$store.commit('togglePostReviewLoading', true)
    this.getAllUsers()
  },
  methods: {
    async getAllUsers() {
      let userData = await this.$store.dispatch('GET_ALL_USERS', {
        limit: 10, offset: 0
      })
      this.userCount = userData.count
      let allUsers = await this.$store.dispatch('GET_ALL_USERS', {
        limit: this.userCount, offset: 0
      })
      this.users = allUsers.results
      await this.$store.commit('togglePostReviewLoading', false)
    }
  },
  filters: {
    filteredGender(val) {
      return val === 'M' ? '남' : '여'
    },
    firstCategory(val) {
      let categoryCnt = val.length
      if (!categoryCnt) {
        return '등록 안 함'
      } else {
        return val[0] + (categoryCnt >= 2 ? `외 ${categoryCnt - 1}개` : '')
      }
    },
  }
}
</script>

<style>

</style>