<template>
  <v-dialog v-model="showDialog" width="600" persistent>
    <v-card>
      <v-card-title><strong>회원가입 작성양식 재확인</strong></v-card-title>
      <v-divider></v-divider>
      <v-card-text class="pb-0">
        <div class="signup-body" v-for="(item, i) in this.userData" :key="i">
          <div class="signup-title">✔️{{ i }}</div>
          <p class="signup-contents">{{ item }}</p>
        </div>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="warning" @click="closeDialog(1)">회원가입 진행</v-btn>
        <v-btn color="error" @click="closeDialog(0)">취소</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    showDialog: {
      type: Boolean,
      required: true
    },
    userData: {
      type: Object,
      required: true
    }
  },
  methods: {
    closeDialog(check) {
      this.$emit('closeDialog', check)
    }
  }
}
</script>

<style scoped>
.v-card__title,
.v-card__actions {
  font-family: 'Noto Sans KR';
  font-size: 21px;
  padding: 16px;
}

.v-card__text {
  font-family: 'Nanum Gothic';
}

.signup-body {
  margin-bottom: 2em;
}

.signup-body .signup-title {
  font-size: 1.3em;
  font-weight: 600;
  color: black;
  margin-bottom: 0.3em;
}

.signup-body .signup-contents {
  font-size: 1.1em;
  color: darkslategrey;
}
</style>