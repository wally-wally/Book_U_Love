<template>
  <div>
    <v-carousel height="400" show-arrows-on-hover>
      <v-carousel-item
        v-for="(image,i) in images"
        :key="i"
        :src="image.src"
        reverse-transition="fade-transition"
        transition="fade-transition">
        <div class="carousel-item-wrapper">
          <div class="carousel-title">{{ image.contents.title }}</div>
          <div class="seperate-line"></div>
          <div class="carousel-body">{{ image.contents.body }}</div>
          <div class="carousel-btn">
            <v-btn v-if="image.contents.moreIcon" color="error" large>READ MORE</v-btn>
          </div>
        </div>
      </v-carousel-item>
    </v-carousel>
  </div>
</template>

<script>
export default {
  name: 'ImageSlider',
  data() {
    return {
      images: [
        {
          src: 'https://user-images.githubusercontent.com/52685250/78128664-3e9ef800-7451-11ea-9145-c00d7f34b7a3.jpg',
          contents: {
            title: 'Book_U_Love',
            body: 'We recommend you a book that you might like.',
            moreIcon: false
          }
        },
        {
          src: 'https://user-images.githubusercontent.com/52685250/78128668-4068bb80-7451-11ea-974a-b6ed4a209ba6.jpg',
          contents: {
            title: 'Book Recommendation',
            body: 'We recommend you a book considering your age, interests, writers, etc.',
            moreIcon: true
          }
        },
        {
          src: 'https://user-images.githubusercontent.com/52685250/78128670-41015200-7451-11ea-8fd1-09928821d29d.jpg',
          contents: {
            title: 'Best Sellers',
            body: 'We introduce you to the bestseller.',
            moreIcon: true
          }
        },
      ]
    }
  }
}
</script>

<style scoped>
.carousel-item-wrapper {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 100%;
  transform: translate(-50%, -50%);
  font-family: 'Inria Serif';
  color: #fff;
  text-align: center;
  text-shadow: 3px 5px 5px rgba(0, 0, 0, 0.3);
}

.carousel-item-wrapper .carousel-title {
  font-size: 4em;
  font-weight: 600;
}

.carousel-item-wrapper .seperate-line {
  margin: 0.9em auto;
  border-bottom: 1px solid lightgray;
  box-shadow: 3px 5px 5px rgba(0, 0, 0, 0.3);
  width: 70%;
}

.carousel-item-wrapper .carousel-body {
  font-size: 1.5em;
  margin: 0.8em 0;
}

@media (min-width: 600px) and (max-width: 960px) {
  .carousel-item-wrapper .carousel-title {
    font-size: 3em;
  }

  .carousel-item-wrapper .carousel-body {
    font-size: 1.25em;
  }
}

@media (max-width: 600px) {
  .carousel-item-wrapper .carousel-title {
    font-size: 2em;
  }

  .carousel-item-wrapper .carousel-body {
    font-size: 0.9em;
  }
}
</style>