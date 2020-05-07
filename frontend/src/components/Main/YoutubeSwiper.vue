<template>
  <div>
    <div class="book-swiper-title">
      <span><i class="fab fa-youtube" :style="{ color: 'crimson'}"></i>도서 추천 관련 Youtube 영상</span>
      <i class="fas fa-undo" @click="reSearchYoutube"></i>
    </div>
    <div v-if="loadingStatus" class="youtube-loading">
      <div class="youtube-logo">
        <i class="fab fa-youtube"></i>
      </div>
      <div class="loading-message">
        <span>데이터를 불러오는 중 입니다.</span>
      </div>
    </div>
    <swiper v-else ref="youtubeSwiper" :options="swiperOptions" class="youtube-swiper-wrapper">
      <swiper-slide v-for="(video, idx) in youtubeVideos" :key="idx">
        <div class="video-section">
          <div>
            <img :src="video.thumbnail" alt="thumbnail" @click="showYoutubeDialog(video)">
            <div class="video-title" v-html="video.title"></div>
          </div>
          <div class="video-channel-info">
            <div class="youtube-channel">
              <i class="fab fa-youtube"></i>
              <span @click="goChannel(video.channelId)">{{ video.channelTitle }}</span>
            </div>
          </div>
        </div>
      </swiper-slide>
      <div class="swiper-pagination" slot="pagination"></div>
      <div class="swiper-button-next" slot="navigation"></div>
      <div class="swiper-button-prev" slot="navigation"></div>
    </swiper>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import axios from 'axios'
import tempYoutube from '@/assets/json/tempYoutube.json'

export default {
  data() {
    return {
      tempYoutube,
      youtubeVideos : [],
      swiperOptions: {
        slidesPerView: 1,
        spaceBetween: 5,
        loop: true,
        loopFillGroupWithBlank: true,
        pagination: {
          el: '.swiper-pagination',
          clickable: true,
        },
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev',
        },
        breakpoints: {
          0: {
            slidesPerView: 1,
            spaceBetween: 0,
          },
          630: {
            slidesPerView: 2,
            spaceBetween: 0,
          },
          970: {
            slidesPerView: 3,
            spaceBetween: 0,
          }
        }
      },
      loadingStatus: false,
      searchKeyword: '도서 추천',
      nowIdx: 0
    }
  },
  computed: {
    ...mapState({
      storeYoutube: state => state.common.storeYoutube,
      checkIdxGroup: state => state.common.checkIdxGroup
    })
  },
  mounted() {
    this.getYoutubes()
  },
  methods : {
    getRandomIntInclusive(min, max) {
      min = Math.ceil(min)
      max = Math.floor(max)
      return Math.floor(Math.random() * (max - min + 1)) + min
    },
    reSearchYoutube() {
      const keywordSet = ['도서 추천', '책 추천', '최신 책 추천', '인생책', '도서 베스트셀러', '도서 스테디셀러', '인생을 바꾼 책']
      if (this.checkIdxGroup.length < 3) {
        while (true) {
          let randomIdx = this.getRandomIntInclusive(0, 6)
          if (!this.checkIdxGroup.includes(randomIdx)) {
            this.nowIdx = randomIdx
            this.$store.commit('storeCheckIdx', randomIdx)
            break
          }
        }
        this.searchKeyword = keywordSet[this.nowIdx]
      }
      this.getYoutubes()
    },
    getYoutubes() {
      this.loadingStatus = true
      this.youtubeVideos = []
      if (this.storeYoutube.length >= 15) {
        let idxGroup = []
        while (idxGroup.length < 5) {
          let randomIdx = this.getRandomIntInclusive(0, this.storeYoutube.length - 1)
          if (!idxGroup.includes(randomIdx)) {
            idxGroup.push(randomIdx)
            this.youtubeVideos.push(this.storeYoutube[randomIdx])
          }
        }
        this.loadingStatus = false
        return
      }
      const API_KEY = process.env.VUE_APP_YOUTUBE_API_KEY
      const API_URL = 'https://www.googleapis.com/youtube/v3/search'
      axios.get(API_URL, {
        params: {
          key: API_KEY,
          type: 'video',
          part: 'snippet',
          q: this.searchKeyword
        }
      })
      .then(response => {
        let videoData = response.data.items
        let youtubeData = []
        for (let i = 0; i < 5; i++) {
          let youtubeObj = {}
          youtubeObj['videoId'] = videoData[i].id.videoId
          youtubeObj['title'] = videoData[i].snippet.title
          youtubeObj['channelId'] = videoData[i].snippet.channelId
          youtubeObj['channelTitle'] = videoData[i].snippet.channelTitle
          youtubeObj['thumbnail'] = videoData[i].snippet.thumbnails.high.url
          youtubeObj['description'] = videoData[i].snippet.description
          youtubeData.push(youtubeObj)
          this.$store.commit('storeYoutube', youtubeObj)
        }
        this.youtubeVideos = youtubeData
        this.loadingStatus = false
      })
      .catch(error => {
        console.log(error)
        this.loadingStatus = true
        this.youtubeVideos = []
        let idxGroup = []
        while (idxGroup.length < 5) {
          let randomIdx = this.getRandomIntInclusive(0, 14)
          if (!idxGroup.includes(randomIdx)) {
            idxGroup.push(randomIdx)
            this.youtubeVideos.push(this.tempYoutube[randomIdx])
          }
        }
        this.loadingStatus = false
      })
    },
    goChannel(channelId) {
      window.open(`https://www.youtube.com/channel/${channelId}`)
    },
    showYoutubeDialog(videoData) {
      this.$store.commit('showYoutubeVideo', videoData)
    }
  }
}
</script>

<style scoped>
.book-swiper-title {
  font-family: 'Gothic A1';
  font-weight: 600;
  font-size: 17px;
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}

.fa-undo {
  padding: 0 8px;
  font-size: 15px;
  border: 1px solid silver;
  border-radius: 10px;
  background-color: rgba(0, 0, 0, 0.07);
  box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.15);
  line-height: 1.5;
}

.fa-undo:hover {
  cursor: pointer;
}

.fa-undo:after {
  content: ' 새로고침';
  font-family: 'Gothic A1';
}

.youtube-swiper-wrapper {
  padding-bottom: 40px;
  margin-bottom: 40px;
}

.video-section {
  text-align: center;
  width: 95%;
  margin: 0 auto;
}

.video-section img,
.video-title {
  width: 100%;
}

.video-title {
  margin: 0 auto;
  text-align: left;
  font-family: 'Gothic A1';
  font-size: 15px;
  font-weight: 600;
}

.video-channel-info {
  text-align: right;
}

.video-channel-info > .youtube-channel > span:hover {
  cursor: pointer;
}

.youtube-channel {
  font-size: 14px;
  margin-top: 8px;
}

.youtube-channel > i {
  color: crimson;
}

.youtube-loading {
  text-align: center;
}

.youtube-logo > i {
  font-size: 100px;
  color: crimson;
  text-shadow: 3px 3px 5px rgba(0, 0, 0, 0.15);
}

.youtube-loading .loading-message {
  text-align: center;
  font-size: 18px;
  font-weight: 600;
  font-family: 'Noto Sans KR';
  margin-bottom: 40px;
}
</style>