<template>
  <div v-if="!isdelete">
    <div class="align-items-center container">
        <div class="review-header">
            <div class="review-username">
                {{review.username}}
                <i class="fas fa-edit px-2" v-if="review.user === this.info.user_id" @click="toggleEditMode"></i>
                <div @click="deletereview" style="display:inline;">
                    <i v-if="this.$store.getters.info.user_id==review.user" class="fas fa-trash-alt"></i>
                </div>
            </div>
            <div class="pb-2 review-info-right">
                <i class="fas fa-heart" v-if="review.user !== this.info.user_id && ifliked && this.isLogin" @click="likeReview"></i>
                <i class="far fa-heart" v-else-if="review.user !== this.info.user_id && !ifliked && this.isLogin" @click="likeReview"></i>
                <span class="review-cnt">({{ likecount }}명) | </span>
                <div class="review-score">{{review.score}}점
                </div>
            </div>
        </div>
        <div v-if="review.spoiler && this.info.user_id !== review.user" class="spoiler-contents"><span>스포일러가 있는 리뷰입니다</span> <br> <small @click="nospoiler()" class="open-spoiler-btn">그래도 볼래요!</small><br> </div>
        <div v-else class="review-content">{{review.content}}</div>
        <div class="review-date" style="border-bottom:1px solid lightgray;white-space:pre-line">{{ review.updated_at | dateFilter }}</div>
        <div style="margin:10px;"/>
    </div>
</div>
</template>
<script>
import { mapState, mapGetters } from 'vuex'
import { deleteBookReview } from '@/api/index.js'

export default {
    name:'star',
    props : {
      review :{ type:Object},
      index : {type:Number},
    },
    data() {
        return {
            ifliked : false,
            isdelete : false,
            reviewScore: 0,
            likecount : this.review.like_user.length
        }
    },
    computed: {
        ...mapState({
            isLogin: state => state.user.isLogin
        }),
        ...mapGetters(['info']),
        reviewCheck() {
            return this.review.like_user.includes(this.$store.getters.info.user_id)
        }
    },
    created() {
        this.ifliked = this.review.like_user.includes(this.$store.getters.info.user_id)
        this.likecount = this.review.like_user.length
    },
    mounted(){
        this.reviewScore = this.review.score / 2
    },
    methods :{
        async deletereview(id) {
            const a = confirm("삭제하시겠습니까")
            if (a) {
                const data = await deleteBookReview(this.review.id)
                this.isdelete = true
                this.$emit('deleteSign')
            }
        },
        nospoiler() {
            this.review.spoiler = !this.review.spoiler
        },
        async likeReview() {
            const formData = new FormData()
            formData.append('user', this.$store.getters.info.user_id)
            formData.append('review', this.review.id)
            const data = await this.$store.dispatch('POST_REVIEW_LIKE', formData)
            console.log(data)
            this.likecount = data['like_count']
            this.ifliked = data['is_liked']
            // this.ifliked = !this.ifliked
            // if (this.ifliked){
            //     this.likecount += 1
            // } else {
            //     this.likecount -= 1
            // }
        },
        toggleEditMode() {
            this.$emit('toggleEditMode', this.review)
        }
    },
    watch: {
        review() {
            setTimeout(() => {
                this.ifliked = this.review.like_user.includes(this.$store.getters.info.user_id)
                this.likecount = this.review.like_user.length
            }, 0)
        }
    }
}
</script>

<style scoped>
i:hover {
    cursor: pointer;
}
.review-score{
    display:inline;
    font-weight:bold;
    font-size:0.9em;
    color: orangered;
}
.review-username{
    font-size: .875rem;
    line-height: 1.375rem;
    letter-spacing: .0071428571em;
    font-weight: bolder;
}
.review-info-right > i.fa-heart {
    font-size: .875rem;
    color: crimson;
    padding-right: 3px;
}
.review-info-right > .review-cnt {
    font-weight: 600;
    font-size: .875rem;
    color: rgba(0, 0, 0, 0.8);
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

.spoiler-contents {
    color: crimson;
    padding-bottom: 10px;
}

.spoiler-contents span {
    font-weight: 600;
}

.spoiler-contents small {
    border: 1px solid silver;
    border-radius: 5px;
    padding: 4px;
    background-color: rgb(250, 237, 231);
    box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.15);
}

.spoiler-contents small:hover {
    cursor: pointer;
    box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.2);
}

.review-date {
    text-align: right;
    color: gray;
    font-size: 14px;
    padding-bottom: 5px;
}
</style>