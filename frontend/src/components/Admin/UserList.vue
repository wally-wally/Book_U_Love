<template>
  <div class="mt-3 mb-6">
    <v-data-table
      :headers="tableHeaders"
      :items="users"
      :items-per-page="itemsPerPage"
      :page.sync="page"
      :single-expand="true"
      :search="searchKeyword"
      show-expand
      item-key="email"
      hide-default-footer
      color="#E6CC00"
      @page-count="pageCount = $event"
      class="elevation-1">
      <template v-slot:top>
        <v-text-field v-model="searchKeyword" append-icon="fa-search" label="회원 검색" single-line hide-details class="mx-4" color="#f7b157"></v-text-field>
      </template>
      <template v-slot:item.gender="{ item }">
        {{ item.gender | filteredGender }}
      </template>
      <template v-slot:item.categorys="{ item }">
        {{ item.categorys | firstCategory }}
      </template>
      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length">
          <div class="ma-2">
            <div class="favorite-category-title">📎{{ item.username }}님의 관심 카테고리</div>
            <div v-if="item.categorys.length" class="category-group">
              <span v-for="(category, idx) in item.categorys" :key="idx">
                <v-chip color="gray" small>{{ category }}</v-chip>
              </span>
            </div>
            <div v-else class="category-group">
              관심 카테고리를 등록하지 않았습니다.
            </div>
            <div class="email-title">✉️{{ item.username }}님에게 E-mail 보내기</div>
            <div class="email-section">
              {{ item.email }}로 e-mail 보내기 <v-btn color="error" small><a :href="`mailto:${item.email}`">전송</a></v-btn>
            </div>
          </div>
        </td>
      </template>
    </v-data-table>
    <div class="text-center pt-2">
      <v-pagination v-model="page" :length="parseInt(userCount / 10) + (userCount % 10 === 0 ? 0 : 1)" :total-visible="7" circle color="#E6CC00"></v-pagination>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      users: [],
      searchKeyword: '',
      userCount: 0,
      tableHeaders: [
        { text: '이름', value: 'username' },
        { text: '나이', value: 'age' },
        { text: '성별', value: 'gender' },
        { text: 'e-mail', value: 'email' }
      ],
      page: 1,
      pageCount: parseInt(this.userCount / 10) + (this.userCount % 10 === 0 ? 0 : 1),
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

<style scoped>
a {
  text-decoration: none;
  color: white;
}

.favorite-category-title,
.email-title {
  display: inline-block;
  font-size: 16px;
  font-family: 'Nanum Gothic';
  font-weight: 600;
  padding-bottom: 4px;
  margin: 4px 0;
  border-bottom: 1px solid silver;
}

.category-group {
  margin: 8px 0 20px;
}

.category-group > span {
  padding-right: 8px;
}

.email-section {
  margin-bottom: 8px;
}
</style>