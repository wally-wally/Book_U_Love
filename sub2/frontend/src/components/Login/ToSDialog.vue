<template>
  <v-dialog v-model="showDialog" width="600" persistent>
    <v-card>
      <v-card-title><strong class="tos-title">{{ this.tosData.title }}</strong></v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <div class="tos-body" v-for="(item, i) in this.tosData.body" :key="i">
          <div class="tos-subtitle">✔ {{ item.subtitle }}</div>
          <p class="tos-contents">{{ item.contents }}</p>
        </div>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="warning" @click="closeDialog(1)">모두 동의하고 닫기</v-btn>
        <v-btn color="error" @click="closeDialog(0)">취소</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'ToSDialog',
  props: {
    showDialog: {
      type: Boolean,
      required: true
    },
    tosData: {
      type: Object,
      required: true
    }
  },
  methods: {
    closeDialog(agree) {
      this.$emit('closeDialog', agree)
    }
  }
}
</script>

<style scoped>
.v-card__title,
.v-card__actions {
  font-family: 'Noto Sans KR';
  padding: 16px;
}

.v-card__text {
  font-family: 'Nanum Gothic';
}

.tos-body {
  margin-bottom: 0.8em;
}

.tos-body .tos-subtitle {
  font-size: 1em;
  font-weight: 600;
  color:#5a5a5a;
  margin-bottom: 0.3em;
}

@media (max-width: 600px) {
  .tos-title {
    font-size: 0.9em;
  }
}
</style>