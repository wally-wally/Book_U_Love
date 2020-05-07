<template>
  <div class="mypage-main-wrapper">
    <div class="mypage-intro">
      
      <div class="mypage-menu">
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
      <div class="mypage-menu">
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
      <div class="mypage-menu">
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
      <div class="mypage-menu" v-if="this.info.user_id <= 4">
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
              <router-link to="/admin/users">Go to Admin Page</router-link>
            </td>
          </tr>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'


export default {
  computed: {
    ...mapGetters(['info'])
  }
}
</script>

<style scoped>
.mypage-main-wrapper {
  margin: 0 auto;
  width: 85%;
}

table {
  margin-bottom: 40px;
}

table img {
  width: 130px;
  margin-top: 4px;
}

table > tr:first-child > td:first-child {
  padding-right: 15px;
}

table > tr > td {
  vertical-align: top;
}

table > tr > td:last-child > div {
  font-size: 1.15rem;
  font-family: 'Quicksand';
  font-weight: 600;
  padding-bottom: 2px;
  margin-bottom: 4px;
  border-bottom: 1px solid silver;
  display: inline-block;
}

table > tr > td:last-child > p {
  font-size: 0.95rem;
  font-family: 'Gothic A1';
  color: grey;
}

a {
  position: relative;
  display: inline-block;
  padding: 6px 18px;
  color: #fff;
  text-decoration: none;
  font-size: 14px;
  font-family: 'Sarabun';
  letter-spacing: 1px;
  border-radius: 40px;
  overflow: hidden;
  background: linear-gradient(90deg, #755bea, #ff72c0);
}

a:hover {
  border: 1px solid silver;
  box-shadow: 3px 5px 5px rgba(0, 0, 0, 0.15);
}

@keyframes animate {
  0% {
    width: 0px;
    height: 0px;
    opacity: 0.5;
  }
  100% {
    width: 500px;
    height: 500px;
    opacity: 0;
  }
}

@media (max-width: 900px) {
  .mypage-main-wrapper {
    width: 100%;
  }
}

@media (max-width: 490px) {
  table img {
    width: 80px;
  }

  table > tr:first-child > td:first-child {
    padding-right: 10px;
  }

  table > tr > td:last-child > div {
    font-size: 1rem;
  }

  table > tr > td:last-child > p {
    font-size: 0.85rem;
  }
}
</style>
