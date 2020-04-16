<template>
  <div class="success-wrapper">
    <div class="success-title">
      <div class="success-img" data-aos="zoom-in-up" data-aos-anchor="#example-anchor" data-aos-offset="500" data-aos-duration="500">
        <img src="../../assets/images/signup/success.png" alt="success-signup">
      </div>
      <div class="success-signup-title">
        {{ info.username }}님 환영합니다!
      </div>
    </div>
    <div class="welcome-service">
      <div class="contents">
        <p>추가정보를 입력하고</p>
        <p>{{ info.username }}님에게 적합한 책을 추천받아보세요.</p>
      </div>
    </div>
    <div class="btn-groups">
      <v-btn color="success" rounded block class="my-3" @click="goAdditionalForm()">추가정보 입력</v-btn>
      <v-btn color="primary" rounded block class="my-3" @click="goMain()">메인 페이지로 가기</v-btn>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters(['info'])
  },
  methods: {
    goMain() {
      this.$router.push('/')
    },
    goAdditionalForm() {
      this.$router.push('/myinfo/account')
    }
  },
  beforeDestroy() {
    this.$store.state.user.agreeToS = false
  }
}
</script>

<style scoped>
.success-wrapper {
  font-family: 'Noto Sans KR';
  margin: 1em auto;
  width: 100%;
  max-width: 500px;
}

.success-title .success-img {
  text-align: center;
}

.success-title .success-img img {
  margin: 0.5em 0;
  width: 200px;
  height: 200px;
}

.success-signup-title {
  font-size: 1.5em;
  font-weight: 600;
  text-align: center;
  margin-top: 0.6em;
}

.welcome-service {
  margin: 1em 0;
  text-align: center;
}

.welcome-service .contents p {
  font-size: 0.95em;
  margin-bottom: 0.5em;
}

.btn-groups {
  text-align: center;
  margin: 1.5em auto;
  width: 75%;
}
</style>