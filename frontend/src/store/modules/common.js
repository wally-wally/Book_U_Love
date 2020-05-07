const state = {
  onMobileDrawer: false,
  showYoutubeVideo: false,
  youtubeVideoData: {},
  storeYoutube: [],
  storeYoutubeID: [],
  checkIdxGroup: [0]
}

const mutations = {
  showDrawer(state, status) {
    state.onMobileDrawer = status
  },
  showYoutubeVideo(state, videoData) {
    state.showYoutubeVideo = videoData.videoId ? true : false
    state.youtubeVideoData = videoData
  },
  storeYoutube(state, videoData) {
    state.storeYoutube.push(videoData)
    state.storeYoutubeID.push(videoData['videoId'])
  },
  storeCheckIdx(state, idx) {
    state.checkIdxGroup.push(idx)
  }
}

export default {
  state,
  mutations
}