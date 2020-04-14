<template>
  <v-dialog v-model="showDialog" width="600" persistent>
    <v-card>
      <v-card-title :style="{ fontFamily: 'Nanum Gothic', fontSize: '22px', fontWeight: 600 }">
        {{ selectedStoreData['store_name'] }}
        </v-card-title>
      <v-divider></v-divider>
      <v-card-text class="pb-3" :style="{ fontFamily: 'Noto Sans KR', fontSize: '15px' }">
        <div class="store-data">
          <v-row>
            <v-col cols="3" class="py-2">Tel.</v-col>
            <v-col cols="9" class="py-2">{{ selectedStoreData['tel']}}</v-col>
          </v-row>
          <v-row>
            <v-col cols="3" class="py-2">Category</v-col>
            <v-col cols="9" class="py-2">{{ selectedStoreData['category']}}</v-col>
          </v-row>
          <v-row>
            <v-col cols="3" class="py-2">address</v-col>
            <v-col cols="9" class="py-2">{{ selectedStoreData['address']}}</v-col>
          </v-row>
        </div>
        <div class="review-contents">
          <div class="review-count">
            <div class='review-count-title'>Reivew Count</div>
            <div class="review-count-body">
              {{ selectedStoreData['review_cnt'] }}
            </div>
          </div>
          <div class="review-mean">
            <div>Review Average</div>
            <div class="review-mean-body">
              {{ selectedStoreData['review_mean'].toFixed(2) }}
            </div>
          </div>
        </div>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="closeDialog()" small color="warning" :style="{ fontFamily: 'Gothic A1'}">닫기</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'StoreDetail',
  props: {
    showDialog: Boolean,
    selectedStoreData: Object
  },
  methods: {
    closeDialog() {
      this.$emit('closeDialog')
    }
  }
}
</script>

<style scoped>
  .review-contents {
    display: flex;
    justify-content: space-around;
    margin-top: 0.7rem;
  }

  .review-count-body,
  .review-mean-body {
    font-size: 1.65em;
    font-weight: 600;
    color: #F06453;
    text-align: center;
    margin: 0.4rem 0;
  }
</style>