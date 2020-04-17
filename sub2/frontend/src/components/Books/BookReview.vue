<template>
  <div v-if="!isdelete">
    <div class="align-items-center container">
        <div class="row">
            <div class="col-2">{{review.username}}</div>
            <div class="col-3">
                <div id="stars">
                    <i class="fa fa-star-o"></i>
                    <i class="fa fa-star-o"></i>
                    <i class="fa fa-star-o"></i>
                    <i class="fa fa-star-o"></i>
                    <i class="fa fa-star-o"></i>
                </div>
            </div>
            <div class="col-6">
                {{review.score}}
            </div>
            <div @click="deletereview" class="col-1">
                <i v-if="this.$store.getters.info.user_id==review.user" class="fas fa-trash-alt"></i>
            </div>
        </div>
        <div style="border-bottom:1px solid lightgray">{{review.content}}</div>
        <div style="margin:10px;"/>
    </div>
</div>
</template>
<script>
import { deleteBookReview } from '@/api/index.js'

export default {
    name:'star',
    props : {
      review :{ type:Object},
      index : {type:Number},
    },
    data() {
        return {
            isdelete : false
        }
    },
    mounted(){
        this.starrating(this.review.score)
    },
    methods :{
        starrating(score){
            var point = 0
            const stars = document.querySelectorAll("#stars")[this.index]
            while (score > point) {
                stars.children[(point/2)].classList.replace('fa-star-o','fa-star')
                point += 2
            }
            if (point != score) {
                stars.children[(parseInt(score)-1)/2].classList.replace('fa-star','fa-star-half-alt')
            }   
        },
        async deletereview(id) {
            const a = confirm("삭제하시겠습니까")
            if (a) {
                const data = await deleteBookReview(this.review.id)
                console.log(data)
                this.isdelete = true
            }
        }
    }
}
</script>

<style scoped>
.fa{
    color:rgb(255, 228, 73);
}
i:hover {
    cursor: pointer;
}
</style>