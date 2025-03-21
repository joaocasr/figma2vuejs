<template>
<div class="grid-container">
 <Footer></Footer>
 <Navbar></Navbar>
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
                
        }
    },
    methods:{
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