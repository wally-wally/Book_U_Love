const state = {
  onMobileDrawer: false,
  showYoutubeVideo: false,
  youtubeVideoData: {}
}

const mutations = {
  showDrawer(state, status) {
    state.onMobileDrawer = status
  },
  showYoutubeVideo(state, videoData) {
    state.showYoutubeVideo = videoData.videoId ? true : false
    state.youtubeVideoData = videoData
  }
}

export default {
  state,
  mutations
}