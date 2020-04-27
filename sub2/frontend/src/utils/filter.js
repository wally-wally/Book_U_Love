import Vue from 'vue'

Vue.filter('authorList', authors => {
  return authors.map(author => author.name).join(' ')
})

Vue.filter('categoryList', categories => {
  if (categories[2].length) {
    return categories.join('>')
  } else {
    return categories.slice(0, 2).join('>')
  }
})