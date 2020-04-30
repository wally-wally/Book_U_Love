<template>
  <div>
    This is User List Section.
  </div>
</template>

<script>
export default {
  data() {
    return {
      users: [],
      userCount: 0
    }
  },
  created() {
    this.$store.commit('togglePostReviewLoading', true)
    this.getAllUsers()
  },
  methods: {
    async getAllUsers() {
      let allUserData = await this.$store.dispatch('GET_ALL_USERS', {
        limit: 10, offset: 0
      })
      this.userCount = allUserData.count
      this.users = allUserData.results
      if (this.userCount > 10) {
        let maxPageNm = parseInt((this.userCount - 1) / 10)
        for (let i = 10; i < (maxPageNm + 1) * 10; i += 10) {
          let moreUsers = await this.$store.dispatch('GET_ALL_USERS', {
            limit: 10, offset: i
          })
          for (const data in moreUsers.results) {
            this.users.push(data)
          }
        }
      }
      await this.$store.commit('togglePostReviewLoading', false)
    }
  }
}
</script>

<style>

</style>