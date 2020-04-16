<template>
  <div class="mypage-main-wrapper">
    <div class="mypage-intro">
      <div class="mypage-menu" data-aos="fade-up" data-aos-duration="1500" data-aos-once="true">
        <table>
          <tr>
            <td rowspan="2">
              <img src="../../assets/images/mypage_icon/dashboard.png" alt="dashboard">
            </td>
            <td>
              <div>Dashboard</div>
              <p>{{ info.username }}님과 관련된 각종 정보들을 시각화해서 보여줍니다.</p>
            </td>
          </tr>
          <tr>
            <td>
              <router-link to="/myinfo/dashboard">Go to Dashboard</router-link>
            </td>
          </tr>
        </table>
      </div>
      <div class="mypage-menu" data-aos="fade-up" data-aos-duration="1500" data-aos-once="true">
        <table>
          <tr>
            <td rowspan="2">
              <img src="../../assets/images/mypage_icon/book.png" alt="my_books">
            </td>
            <td>
              <div>My Books</div>
              <p>{{ info.username }}님이 좋아요를 누른 책 리스트, 리뷰 작성한 책 리스트 등 {{ info.username }}님의 책과 관련된 정보들을 볼 수 있습니다.</p>
            </td>
          </tr>
          <tr>
            <td>
              <router-link to="/myinfo/mybooks">Go to My Books</router-link>
            </td>
          </tr>
        </table>
      </div>
      <div class="mypage-menu" data-aos="fade-up" data-aos-duration="1500" data-aos-once="true">
        <table>
          <tr>
            <td rowspan="2">
              <img src="../../assets/images/mypage_icon/account.png" alt="account">
            </td>
            <td>
              <div>Account</div>
              <p>{{ info.username }}님의 개인 정보(계정 관리)를 관리할 수 있습니다.(추가 정보 입력, 비밀번호 변경 등)</p>
            </td>
          </tr>
          <tr>
            <td>
              <router-link to="/myinfo/account">Go to Account</router-link>
            </td>
          </tr>
        </table>
      </div>
      <div class="mypage-menu" data-aos="fade-up" data-aos-duration="1500" data-aos-once="true">
        <table>
          <tr>
            <td rowspan="2">
              <img src="../../assets/images/mypage_icon/admin.png" alt="admin">
            </td>
            <td>
              <div>Admin Page</div>
              <p>회원들의 정보와 DB에 저장된 데이터를 관리할 수 있습니다.(관리자 전용)</p>
            </td>
          </tr>
          <tr>
            <td>
              <router-link to="/admin">Go to Admin Page</router-link>
            </td>
          </tr>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    ...mapGetters(['info'])
  }
}
</script>

<style scoped>
.mypage-main-wrapper {
  margin: 0 0.4em;
}
</style>