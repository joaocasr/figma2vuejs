<template>
<div class="grid-container">
 <img class="grid-item container2362397" src="/image11.png"/>
 <p class="grid-item text2362398">
  Avatar (2022)
 </p>
 <p class="grid-item text2362399">
  Jake Sully lives with his newfound family formed on the extrasolar moon  Pandora. Once a familiar threat returns to finish what was previously  started, Jake must work with Neytiri and the army of the Na'vi race to  protect their home.
 </p>
 <div class="grid-item rectangle2433228">
  <p class="grid-item text2362402">
   Score
  </p>
  <p class="grid-item text2362403">
   3.0
  </p>
 </div>
 <div class="grid-item container2362404" v-on:click="changeVisibility2362620()">
  <p class="grid-item text2362405">
   Add to Watchlist
  </p>
 </div>
 <div class="grid-item container2362406" v-on:click="scrollTo2362406()">
  <p class="grid-item text2362407">
   Watch Trailer
  </p>
  <div class="grid-item regular_polygon2362408">
  </div>
 </div>
 <div class="grid-item container2362409">
  <p class="grid-item text2362410">
   Watch Online Now
  </p>
  <div class="grid-item regular_polygon2362411">
  </div>
 </div>
 <p class="grid-item text2362419">
  1h,34min
 </p>
 <p class="grid-item text2362420">
  10 Oct 2022
 </p>
 <div class="grid-item container2362421" v-on:click="gotoReviewPage()">
  <p class="grid-item text2362424">
   Insert My Review
  </p>
 </div>
 <p class="grid-item text2362425">
  REVIEWS
 </p>
 <p class="grid-item text2362426">
  Related Movies
 </p>
 <div class="grid-item line2362427">
 </div>
 <div class="grid-item line2362428">
 </div>
 <Footer class="grid-item-2362433 component2362433"></Footer>
 <div class="grid-item container2362434">
  <Related1 class="grid-item-2362435 component2362435"></Related1>
  <Related2 class="grid-item-2362436 component2362436"></Related2>
  <Related3 class="grid-item-2362437 component2362437"></Related3>
 </div>
 <Review class="grid-item-23641380 component23641380"></Review>
 <Review class="grid-item-2488518 component2488518"></Review>
 <v-rating :length="5" :model-value="starsSeletec2465472" :size="25" class="srating2465472"  half-increments hover readonly >
 </v-rating>
 <v-pagination :length="68" :total-visible="3" class="spaginator2488497" v-model="currentPage2488497">
 </v-pagination>
 <div class="svideo2560721" ref="ref2560721">
  <iframe controls="1" height="500.0px" src="https://www.youtube.com/embed/9ZIgQFKaK4Y" width="934.0px">
  </iframe>
 </div>
 <Navbar @show-from2621776-to26211200="show26211200=true" class="grid-item-2362441 component2362441 posnavbar"></Navbar>
 <Confirmationwatchlistmodal @close-from2362622-to2362620="show2362620=false" @close-from2362624-to2362620="show2362620=false" class="grid-item-2362620 component2362620" v-if="show2362620==true"></Confirmationwatchlistmodal>
</div>

</template>

<script>
import Navbar from '@/components/Navbar.vue';
import Related3 from '@/components/Related3.vue';
import Related2 from '@/components/Related2.vue';
import Review from '@/components/Review.vue';
import Confirmationwatchlistmodal from '@/components/Confirmationwatchlistmodal.vue';
import Related1 from '@/components/Related1.vue';
import Footer from '@/components/Footer.vue';

export default {
    components:{
        Navbar,
        Related3,
        Related2,
        Review,
        Confirmationwatchlistmodal,
        Related1,
        Footer
    },
    data(){
        return {
            show2362620:false,
            starsSeletec2480470:"5",
            starsSeletec2480470:"5",
            starsSeletec2465472:"3",
            currentPage2488497:1,
            menuoptions2575928:[{'option': 'Login', 'destination': '2548:560'}, {'option': 'Sign Up'}]    
        }
    },
    methods:{
		changeVisibility2362620(){
            this.show2362620 = true;
        },
        scrollTo2362406(){
            this.$refs.ref2560721?.scrollIntoView({ behavior: 'smooth' });
        },
		gotoReviewPage(){
            this.$router.push({path:"/reviewpage"});
        },
		gotoHomePage(){
            this.$router.push({path:"/homepage"});
        },
		gotoWatchlistPage(){
            this.$router.push({path:"/watchlistpage"});
        },
        selectedItem2575928(){
               this.$router.push({path:"/loginpage"});

            },
		changeVisibility26211200(){
            this.$emit('show-from2621776-to26211200');
        }
	}
}
</script>
<style lang="css" scoped>
@import '../assets/moviepage.css';
</style>