<template>
  <div class="wrapper">
    <p><i class="far fa-chart-bar"></i></p>
    <p>Book_U_Love 서비스의</p>
    <p>다양한 데이터를 볼 수 있는</p>
    <p>TMI Center 입니다.</p>
    <div class="select-message">
      원하시는 메뉴를 상단에서 골라주세요.
    </div>
  </div>
</template>

<script>
export default {

}
</script>

<style scoped>
.wrapper {
  text-align: center;
}

i {
  font-size: 140px;
  margin-top: 40px;
}
.wrapper > p {
  margin-bottom: 10px;
}
.wrapper > p:not(:first-child) {
  margin-bottom: 4px;
  font-size: 18px;
  font-family: 'Gothic A1';
  font-weight: 600;
}

.select-message {
  font-size: 17px;
  font-weight: 600;
  font-family: 'Noto Sans KR';
  margin-top: 12px;
}
</style>