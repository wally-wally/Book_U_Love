<template>
  <div>
    <div class="image-slider-wrapper">
      <div class="image-section">
        <img :src="imgUrl(nowImageIdx)" :alt="`image-slide-${nowImageIdx}`" aspect-ratio="2">
        <div class="move-btn">
          <span class="left-btn" @click="changeImage(0)">
            <i class="fas fa-arrow-left"></i>
          </span>
          <span class="right-btn" @click="changeImage(1)">
            <i class="fas fa-arrow-right"></i>
          </span>
        </div>
        <div class="image-btn">
          <span v-for="i in 3" :key="i">
            <i :class="`fas fa-circle ${nowImageIdx === i ? 'selected-image' : ''}`" @click="nowImageIdx = i"></i>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ImageSlider',
  data() {
    return {
      nowImageIdx: 1,
      imageCount: 3
    }
  },
  // mounted() {
  //   var autoChangeEvent = setInterval(() => {
  //     this.changeImage(1)
  //   }, 5000)
  // },
  methods: {
    imgUrl(idx) {
      return require(`../../assets/images/image_slider/main0${idx}.jpg`)
    },
    // clickChangeImageBtn(arrow) {
    //   clearInterval(autoChangeEvent)
    //   changeImage(arrow)
    // },
    changeImage(arrow) {
      let addValue = arrow ? 1 : -1
      let calcValue = this.nowImageIdx + addValue
      this.nowImageIdx = calcValue === this.imageCount + 1 || calcValue === 0 ? (arrow ? 1 : this.imageCount) : calcValue
    }
  }
}
</script>

<style scoped>
.image-section {
  position: relative;
  display: block;
  width: 100%;
  height: 500px;
  overflow: hidden;
}

.image-section img {
  position: absolute;
  width: 100%;
  top: -25%;
  opacity: 0.5;
}

.image-section .move-btn span{
  position: absolute;
  top: 45%;
  font-size: 1.5em;
  color: rgb(51, 50, 50);
  text-shadow: 3px 6px 6px rgba(0, 0, 0, 0.3);
  margin: 0 0.25em;
}

.image-section .move-btn span:hover {
  cursor: pointer;
}

.image-section .move-btn span[class='right-btn'] {
  right: 0;
}

.image-btn {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  font-size: 14px;
}

.image-btn span {
  margin: 0 0.15em;
}

.image-btn:hover {
  cursor: pointer;
}

.fa-circle {
  color: darkgray;
}

.selected-image {
  color: black;
}

@media (min-width: 900px) and (max-width: 1200px) {
  .image-section {
    height: 390px;
  }
}

@media (min-width: 600px) and (max-width: 900px) {
  .image-section {
    height: 280px;
  }
}

@media (max-width: 600px) {
  .image-section {
    height: 170px;
  }
}
</style>