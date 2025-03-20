<template>
<div class="grid-container">
 <div class="grid-item container2362475">
  <div class="grid-item rectangle2362476">
   <p class="grid-item text2362511">
    4.5
   </p>
   <p class="grid-item text2362477">
    AVERAGE SCORE
   </p>
  </div>
 </div>
 <div class="grid-item container2362478" v-on:click="changeVisibility2362634()">
  <p class="grid-item text2362479">
   Clear Watchlist
  </p>
  <div class="grid-item container2362480">
   <img class="grid-item container2362481" src="/trashVector.svg"/>
  </div>
 </div>
 <div class="grid-item container2362482">
  <div class="grid-item rectangle2362483">
   <p class="grid-item text2362486">
    1
   </p>
   <p class="grid-item text2362484">
    ITEMS ON LIST
   </p>
  </div>
 </div>
 <p class="grid-item text2362488">
  WATCHLIST
 </p>
 <div class="grid-item container2362489">
  <div class="grid-item rectangle2362490">
   <p class="grid-item text2362492">
    Fantastic Beasts: The Secrets of Dumbledore
    <br/>
    (2022)
   </p>
   <img class="grid-item container2362491" src="/poster31.png"/>
  </div>
 </div>
 <Footer></Footer>
 <Navbar class="posnavbar"></Navbar>
 <Deletionwatchlistmodal @close-from2362636-to2362634="show2362634=false" @close-from2362638-to2362634="show2362634=false" v-if="show2362634==true"></Deletionwatchlistmodal>
</div>

</template>

<script>
import Footer from '@/components/Footer.vue';
import Navbar from '@/components/Navbar.vue';
import Deletionwatchlistmodal from '@/components/Deletionwatchlistmodal.vue';

export default {
    components:{
        Footer,
        Navbar,
        Deletionwatchlistmodal
    },
    data(){
        return {
            show2362634:false    
        }
    },
    methods:{
		changeVisibility2362634(){
            this.show2362634 = true;
        },
		gotoHomePage(){
            this.$router.push({path:"/homepage"});
        },
		gotoWatchlistPage(){
            this.$router.push({path:"/watchlistpage"});
        },
		goto(){
            this.$router.push({path:"/"});
        }
	}
}
</script>
<style lang="css" scoped>
@import '../assets/watchlistpage.css';
</style>