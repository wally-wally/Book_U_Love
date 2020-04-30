const state = {
  onMobileDrawer: false
}

const mutations = {
  showDrawer(state, status) {
    state.onMobileDrawer = status
  }
}

export default {
  state,
  mutations
}