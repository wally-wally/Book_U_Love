<template>
  <div v-if="!isdelete">
    <div class="align-items-center container">
        <div class="review-header">
            <div class="review-username">
                {{review.username}}
                <div @click="deletereview" style="display:inline;">
                    <i v-if="this.$store.getters.info.user_id==review.user" class="fas fa-trash-alt"></i>
                </div>
            </div>
            <div class="pb-2">
                <div id="stars" style="display:inline">
                    <i class="fa fa-star-o"></i>
                    <i class="fa fa-star-o"></i>
                    <i class="fa fa-star-o"></i>
                    <i class="fa fa-star-o"></i>
                    <i class="fa fa-star-o"></i>
                </div>
                <div class="review-score ml-2">{{review.score}}
                </div>
            </div>
        </div>
        <div v-if="review.spoiler" >스포일러가 있는 리뷰입니다 <br> <small @click="nospoiler()">그래도 볼래요!</small><br> </div>
        <div v-else class="review-content" style="border-bottom:1px solid lightgray;white-space:pre-line">{{review.content}}</div>
        
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
                this.$emit('deleteSign')
            }
        },
        nospoiler() {
            this.review.spoiler = !this.review.spoiler
        }
    }
}
</script>

<style scoped>
.fa{
    color:#f9d71c;
}
i:hover {
    cursor: pointer;
}
.review-score{
    display:inline;
    font-weight:bold;
    font-size:0.9em;
}
.review-username{
    font-size: .875rem;
    line-height: 1.375rem;
    letter-spacing: .0071428571em;
    font-weight: bolder;
}
.review-content{
    padding-bottom: 10px;
    font-size: 13px;
    color: #212529;
    line-height: 1.7em;
    word-break: break-all;
}
.review-header {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
}
</style>