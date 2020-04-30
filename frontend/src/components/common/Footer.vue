<template>
  <footer id="footer">
    <div class="footer-title">
      (BOOK_U_LOVE logo here)
    </div>
    <nav id="footer-menu-primary" class="footer-menu" style="width:60%; margin:0 auto;">
      <ul>
        <li id="menu-item-91" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-91"><span style="padding:30px;">About</span></li>
        <li id="menu-item-92" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-92"><span style="padding:30px;">Information</span></li>
        <li id="menu-item-93" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-93"><span style="padding:30px;">Contact</span></li>
      </ul>
    </nav>
    <p class="copyright pt-3">Copyright ⓒ 2020 by <span class="editor" @click="goGitlab()">Damungbissa</span>. All rights reserved.</p>
    
  </footer>
</template>

<script>
export default {
  methods: {
    goGitlab() {
      window.open('https://lab.ssafy.com/s02-bigdata-sub2/s02p22b205')
    }
  }
}
</script>

<style scoped>
  /* .editor {
    color: #fff;
  } */
  .editor:hover {
    cursor: pointer;
  }
  #footer {
    position: relative;
    color: #7F7675;
    padding: 30px 0;
    background-color: #f6e9e6 ;
    text-align: center;
  }
  #footer .copyright {
    color: #7F7675;
    font-size: 14px;
    line-height: 28px;
    font-weight: 500;
  }
  #footer-menu-primary {
    border-bottom: 3px solid #DCCAC7;
  }
  .footer-menu {
      position: relative;
      padding: 15px 0;
  }
  li{
    list-style: none;
    display:inline-block;
    font-size:14px;
    line-height: 15px;
    font-weight: 500;
  }
  .footer-menu ul li:hover{
    position: relative;
    display: inline-block;
    bottom: 0;
    left: 0;
    right: 0;
    height: 2px;
    transform: translateY(2px);
    transition: .3s ease all;
    cursor: pointer;
  }

</style>