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
 <div class="grid-item container2362406">
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
 <div class="grid-item container2362429">
  <div class="grid-item rectangle2362430">
  </div>
  <p class="grid-item text2362431">
   1
  </p>
 </div>
 <Footer></Footer>
 <div class="grid-item container2362434">
  <Related1></Related1>
  <Related2></Related2>
  <Related3></Related3>
 </div>
 <Review></Review>
 <v-rating :length="5" :model-value="starsSeletec2465472" :size="25" class="srating2465472"  half-increments hover readonly >
 </v-rating>
 <Navbar class="posnavbar"></Navbar>
 <Confirmationwatchlistmodal @close-from2362622-to2362620="show2362620=false" @close-from2362624-to2362620="show2362620=false" v-if="show2362620==true"></Confirmationwatchlistmodal>
</div>

</template>

<script>
import Footer from '@/components/Footer.vue';
import Related1 from '@/components/Related1.vue';
import Related2 from '@/components/Related2.vue';
import Related3 from '@/components/Related3.vue';
import Review from '@/components/Review.vue';
import Navbar from '@/components/Navbar.vue';
import Confirmationwatchlistmodal from '@/components/Confirmationwatchlistmodal.vue';

export default {
    components:{
        Footer,
        Related1,
        Related2,
        Related3,
        Review,
        Navbar,
        Confirmationwatchlistmodal
    },
    data(){
        return {
            show2362620:false,
            starsSeletec2465472:"3"    
        }
    },
    methods:{
		changeVisibility2362620(){
            this.show2362620 = true;
        },
		gotoReviewPage(){
            this.$router.push({path:"/reviewpage"});
        },
		gotoHomePage(){
            this.$router.push({path:"/homepage"});
        },
		gotoHomePage(){
            this.$router.push({path:"/homepage"});
        },
		gotoWatchlistPage(){
            this.$router.push({path:"/watchlistpage"});
        }
	}
}
</script>
<style lang="css" scoped>
@import '../assets/moviepage.css';
</style>