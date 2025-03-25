<template>
<div class="grid-container">
 <Footer class="grid-item-2362643 component2362643"></Footer>
 <img class="grid-item container2362645" src="/image12.png"/>
 <div class="grid-item container2362674">
  <p class="grid-item text2362675">
   PUBLISH
  </p>
 </div>
 <p class="grid-item text2362676">
  AVATAR (2022)
 </p>
 <div class="grid-item container2442230">
  <div class="grid-item rectangle2442231">
   <p class="grid-item text2442232">
    Write down your review...
   </p>
  </div>
 </div>
 <div class="grid-item container2480491">
  <div class="grid-item container2480492">
   <p class="grid-item text2480493">
    Rate
   </p>
   <v-rating :length="5" :model-value="starsSeletec2480504" :size="25" class="srating2480504" half-increments="" hover="">
   </v-rating>
  </div>
 </div>
 <Navbar class="grid-item-2362644 component2362644 posnavbar"></Navbar>
</div>

</template>

<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';

export default {
    components:{
        Navbar,
        Footer
    },
    data(){
        return {
            starsSeletec2480504:"5"    
        }
    },
    methods:{
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
@import '../assets/reviewpage.css';
</style>