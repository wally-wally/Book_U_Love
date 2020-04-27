import Vue from 'vue'

Vue.filter('authorList', authors => {
  return authors.map(author => author.name).join(' ')
})