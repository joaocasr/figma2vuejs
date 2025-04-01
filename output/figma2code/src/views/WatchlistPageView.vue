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
   <v-rating :length="5" :model-value="starsSeletec2465466" :size="25" class="srating2465466"  half-increments hover readonly >
   </v-rating>
   <p class="grid-item text2362492">
    Fantastic Beasts: The Secrets of Dumbledore
    <br/>
    (2022)
   </p>
   <img class="grid-item container2362491" src="/poster31.png"/>
  </div>
 </div>
 <Footer class="grid-item-2362509 component2362509"></Footer>
 <Navbar class="grid-item-2362512 component2362512 posnavbar"></Navbar>
 <Deletionwatchlistmodal @close-from2362636-to2362634="show2362634=false" @close-from2362638-to2362634="show2362634=false" class="grid-item-2362634 component2362634" v-if="show2362634==true"></Deletionwatchlistmodal>
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
            show2362634:false,
            starsSeletec2465466:"3",
            menuoptions2575928:[{'option': 'Login', 'destination': '2548:560'}, {'option': 'Sign Up'}]    
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
        selectedItem2575928(){
               this.$router.push({path:"/loginpage"});

            }
	}
}
</script>
<style lang="css" scoped>
@import '../assets/watchlistpage.css';
</style>