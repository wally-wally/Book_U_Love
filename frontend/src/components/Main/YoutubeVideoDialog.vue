<template>
  <div class="youtube-wrapper">
    <div class="youtube-contents">
      <div class="video-header">
        <div class="video-title">
          {{ this.youtubeVideoData.title }}
        </div>
        <div class="video-close-btn">
          <v-btn @click="closeVideo" small>CLOSE</v-btn>
        </div>
      </div>
      <div class="video-section">
        <iframe :src="`https://www.youtube.com/embed/${this.youtubeVideoData.videoId}`" frameborder="0" allowfullscreen class="youtube-video"></iframe>
      </div>
      <div class="video-info">
        <p class="video-description" v-if="this.youtubeVideoData.description" v-html="this.youtubeVideoData.description"></p>
        <hr class="my-2">
        <p class="channel-info text-right">[영상 출처] <i class="fab fa-youtube" :style="{ color: 'crimson' }"></i><span @click="goChannel">{{ this.youtubeVideoData.channelTitle }}</span></p>
      </div>
    </div>
    <div class="youtube-contents mobile-landscape">
      <div class="youtube-mobile-info">
        <div>
          <div class="video-title">
            {{ this.youtubeVideoData.title }}
          </div>
          <hr>
          <div class="video-description" v-if="this.youtubeVideoData.description" v-html="this.youtubeVideoData.description"></div>
        </div>
        <div>
          <hr class="my-2">
          <p class="channel-info text-right">[영상 출처] <i class="fab fa-youtube" :style="{ color: 'crimson' }"></i><span @click="goChannel">{{ this.youtubeVideoData.channelTitle }}</span></p>
          <p class="text-right ma-0"><v-btn @click="closeVideo" small>CLOSE</v-btn></p>
        </div>
      </div>
      <div class="video-section">
        <iframe :src="`https://www.youtube.com/embed/${this.youtubeVideoData.videoId}`" frameborder="0" allowfullscreen class="youtube-video"></iframe>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState({
      youtubeVideoData: state => state.common.youtubeVideoData
    })
  },
  methods: {
    closeVideo() {
      this.loading = false
      this.$store.commit('showYoutubeVideo', {
        videoId: '',
        title: '',
        channelId: '',
        channelTitle: '',
        thumbnail: '',
        description: ''
      })
    },
    goChannel() {
      window.open(`https://www.youtube.com/channel/${this.$store.state.common.youtubeVideoData.channelId}`)
    },
  }
}
</script>

<style scoped>
.youtube-wrapper {
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 10001;
  position: fixed;
  left: 0;
  top: 0;
  width: 100vw;
  height: 100vh;
  color: white;
  overflow: hidden;
}

.video-header {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  margin-bottom: 6px;
}

.video-title {
  font-family: 'Jua';
  font-size: 24px;
  text-align: left;
  text-shadow: 3px 3px 5px rgba(0, 0, 0, 0.2);
}

.youtube-contents {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 70%;
  max-width: 892.5px;
  background-color: rgba(0, 0, 0, 0.25);
  border-radius: 20px;
  box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);
  padding: 10px;
}

.video-section {
  position: relative;
  width: 100%;
  padding: 56.6% 0 15px;
  margin-bottom: 4px;
}

.youtube-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  max-width: 892.5px;
  max-height: 511.141px;
}

.video-info p {
  font-family: 'Gothic A1';
  font-size :15px;
  font-weight: 600;
  margin: 0;
}

.video-info p.video-description {
  margin-top: 8px;
}

.video-info > p > a {
  color: white;
  text-decoration: none;
}

.fa-external-link-alt {
  padding: 0 15px;
}

.fa-external-link-alt:hover {
  cursor: pointer;
}

.channel-info span:hover {
  cursor: pointer;
}

/* mobile landscape version */
.youtube-contents.mobile-landscape {
  display: none;
  width: 95%;
}

.youtube-contents.mobile-landscape .youtube-mobile-info .video-title {
  font-size: 15px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 5px;
}

.youtube-contents.mobile-landscape .youtube-mobile-info .video-description {
  font-size: 15px;
  font-family: 'Gothic A1';
  margin-top: 5px;
  line-height: 1.6;
}

.youtube-contents.mobile-landscape .youtube-mobile-info .channel-info {
  font-size: 14px;
  margin-bottom: 8px;
}

@media (min-width: 601px) {
  .youtube-contents {
    padding: 20px;
  }
}

@media (max-width: 600px) {
  .youtube-contents {
    width: 90%;
    padding: 10px;
  }

  .video-title {
    font-size: 20px;
  }

  .fa-external-link-alt {
    display: block;
    padding: 5px 0 10px 0;
  }
}

@media (max-height: 600px) {
  @media (orientation: landscape) {
    .youtube-contents.mobile-landscape {
      display: grid;
      grid-template-columns: 1fr 2fr;
      gap: 10px;
    }

    .youtube-contents.mobile-landscape .youtube-mobile-info {
      min-width: 160px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }

    .youtube-contents {
      display: none;
    }

    .video-header,
    .video-section {
      margin: 0;
    }

    .video-info p {
      font-size: 13px;
    }

    .fa-external-link-alt {
      display: inline;
      padding: 0 10px;
    }
  }
}
</style>