<template>
  <div>
    <v-alert
      dense
      text
      color="#607D8B"
      :style="{ fontFamily: 'Noto Sans KR' }">
      <i class="fas fa-check alert-message"></i><span class="pl-2 alert-message">각 음식점을 선택하면 해당 음식점의 상세 정보를 볼 수 있습니다.</span>
    </v-alert>
    <v-data-table
      :headers="tableHeaders"
      :items="data"
      :items-per-page="itemsPerPage"
      :page.sync="page"
      item-key="noticeIdx"
      hide-default-footer
      color="#E6CC00"
      @page-count="pageCount = $event"
      @click:row="showStoreDetail($event)"
      class="elevation-1">
      <template v-slot:item.review_mean="{ item }">
        <v-chip :color="getColor(item.review_mean)" dark><strong>{{ item["review_mean"] | roundReviewMean }}</strong></v-chip>
      </template>
    </v-data-table>
    <div class="text-center pt-2">
      <v-pagination
        v-model="page"
        :length="pageCount"
        :total-visible="9"
        circle
        color="black"
        prev-icon="fa-arrow-left"
        next-icon="fa-arrow-right"></v-pagination>
    </div>
    <StoreDetail v-if="showDialog" :selectedStoreData="selectedStoreData" :showDialog="showDialog" @closeDialog="closeDialog"></StoreDetail>
  </div>
</template>

<script>
import StoreDetail from '@/components/ReviewCount/StoreDetail'

export default {
  name: 'RemainStoresData',
  components: {
    StoreDetail
  },
  props: {
    data: Array
  },
  data() {
    return {
      tableHeaders: [
        { text: '이름', value: 'store_name' },
        { text: '카테고리', value: 'category' },
        { text: '주소', value: 'address' },
        { text: '평점', value: 'review_mean' }
      ],
      page: 1,
      pageCount: parseInt(this.data.length / 10),
      itemsPerPage: 9,
      selectedStoreData: {},
      showDialog: false
    }
  },
  methods: {
    showStoreDetail(data) {
      this.selectedStoreData = data
      this.showDialog = true
    },
    closeDialog() {
      this.selectedStoreData = {}
      this.showDialog = false
    },
    getColor(score) {
      if (score >= 4.5) {
        return 'red'
      } else if (score >= 4.0 && score < 4.5) {
        return 'green'
      } else {
        return 'blue'
      }
    }
  },
  filters: {
    roundReviewMean(mean) {
      return mean.toFixed(2)
    }
  }
}
</script>

<style scoped>
  @media(min-width: 600px) {
    .alert-message {
      font-size: 16px;
    }
  }

  @media(max-width: 600px) {
    .alert-message {
      font-size: 13px;
    }
  }
</style>