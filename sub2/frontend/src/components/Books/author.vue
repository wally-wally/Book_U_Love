<template>
  <div>
      author
      <hr>
      {{author}}
</div>
</template>

<script>
import { fetchauthor } from '@/api/index.js'

export default {
    name  : 'author',
    data() {
        return {
            author: {}
        }
    },
    mounted() {
        this.getauthor(this.$route.params.id)
    },
    methods : {
        async getauthor(id) {
            const data = await fetchauthor(id)
            console.log(data)
            this.author = data.data
        }
    }
}
</script>

<style>

</style>