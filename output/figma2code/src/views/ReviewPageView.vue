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
import Footer from '@/components/Footer.vue';
import Navbar from '@/components/Navbar.vue';

export default {
    components:{
        Footer,
        Navbar
    },
    data(){
        return {
            starsSeletec2480504:"5",
            menuoptions2575928:[{'option': 'Login', 'destination': '2548:560'}, {'option': 'Sign Up'}]    
        }
    },
    methods:{
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
@import '../assets/reviewpage.css';
</style>