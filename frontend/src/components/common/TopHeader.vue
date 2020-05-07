<template>
  <div class="top-header">
    <div class="top-header-wrapper">
      <div class="homepage-title">
        <router-link to="/">
          <span class="link-text">Book U Love</span>
        </router-link>
        <span v-if="Object.keys(info).length" class="login-user-name ml-2">({{ info.username }}<span class="greeting">님 환영합니다</span>)</span>
      </div>
      <div class="team-intro">
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data() {
    return {
      showDialog: false
    }
  },
  computed: {
    ...mapGetters(['info'])
  },
  methods: {
    toggleDialog() {
      this.showDialog = !this.showDialog
    }
  }
}
</script>

<style scoped>
.v-application a {
  text-decoration: none;
  color: black;
}

.top-header {
  background-color: black;
}

.top-header-wrapper {
  display: flex;
  justify-content: space-between;
  width: 80%;
  margin: 0 auto;
  padding: 0.2em 0;
}

.link-text,
.login-user-name {
  font-family: 'Sarabun';
  color: white;
}

.login-user-name {
  font-size: 0.9em;
}

.homepage-title .link-text {
  font-size: 1.3em;
}

.team-intro .link-text {
  line-height: 2.05em;
}

.link-text:hover {
  cursor: pointer;
}

/* Introduction dialog style */
.team-name { 
  font-size: 1.2em;
  font-weight: 600;
  font-family: 'Quicksand';
  text-shadow: 3px 6px 6px rgba(0, 0, 0, .1);
}

.intro-contents div[class$='-title'] {
  font-size: 1.1em;
  font-weight: 600;
  font-family: 'Nanum Coding';
  color: black;
  padding-bottom: 0.25em;
}

.intro-contents div[class$='-contents'] > ul {
  list-style: disc;
}

.intro-contents div[class$='-contents'] > ul > li {
  padding-bottom: 3px;
}

@media (max-width: 600px) {
  .top-header-wrapper {
    width: 90%;
  }
}

@media (max-width: 500px) {
  .login-user-name .greeting {
    display: none;
  }
}
</style>