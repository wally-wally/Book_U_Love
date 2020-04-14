<template>
  <div class="mb-6">
    <div class="weekly-author-title">
      <span>Author of the Week</span>
    </div>
    <div v-for="(author, i) in authors" :key="i" class="weekly-author-list">
      <span class="author-rank mr-2" :style="{ color: setColor(i + 1) }">{{ i + 1 }}</span>
      <span class="author-name d-inline-block">{{ author.name }}</span>
    </div>
  </div>
</template>

<script>
import { rankingColor } from '@/utils/rankingColor.js'

export default {
  data() {
    return {
      authors: [ // 샘플 데이터
        {'name': 'author1'},
        {'name': 'author2'},
        {'name': 'author3'},
        {'name': 'author4'},
        {'name': 'author5'},
      ]
    }
  },
  methods: {
    setColor(rank) {
      return rankingColor(rank)
    }
  }
}
</script>

<style scoped>
.weekly-author-title {
  font-family: 'Julius Sans One';
  font-weight: 600;
  font-size: 1.1em;
  margin-bottom: 0.6em;
}

.weekly-author-list {
  margin-bottom: 0.4em;
}

.weekly-author-list .author-rank {
  font-family: 'Chivo';
}

.weekly-author-list .author-name {
  font-family: 'Sarabun'; 
}
</style>