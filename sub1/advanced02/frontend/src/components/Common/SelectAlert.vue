<template>
  <div>
    <p class="select-alert">
      <i class="fas fa-check-circle d-block"></i>
      <span class="select-alert-message">원하는 차트 항목을 선택하고 '차트 보기'를 클릭하세요.</span>
    </p>
  </div>
</template>

<style scoped>
  .select-alert {
    margin: 20px 0;
    text-align: center;
  }

  .select-alert .fas {
    font-size: 130px;
    color: #838704;
    margin-bottom: 20px;
    animation: emphasis 1s linear infinite alternate;
  }

  .select-alert .select-alert-message {
    display: inline-block;
    font-family: 'Gothic A1';
    font-weight: 600;
    font-size: 1.1em;
    letter-spacing: -0.02em;
    margin-top: 20px;
  }

  @keyframes emphasis {
    from {
      transform: scale(1);
    }
    to {
      transform: scale(1.15);
    }
  }
</style>