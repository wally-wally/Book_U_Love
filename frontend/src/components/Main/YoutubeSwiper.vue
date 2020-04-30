<template>
  <div>
    {{YoutubeVideos}}
  </div>
</template>

<script>
import axios from 'axios'
const API_KEY = "AIzaSyATVxlcYKoAefs4we-UMRDxjaBZe9A7VUo"
export default {
  data() {
    return {
      YoutubeVideos : [],
    }
  },
  mounted() {
    this.getYoutubes()
  },
  methods : {
    getYoutubes() {
    axios.get('https://www.googleapis.com/youtube/v3/search', {
      params : {
        q : 'book',
        key : API_KEY,
        part : 'snippet',
        type:'video',
      }
    }).then(response => {
      this.YoutubeVideos = response.data.items
    }).catch(error => {
      console.log(error)
    })
    }
  }
}
</script>

<style>

</style>