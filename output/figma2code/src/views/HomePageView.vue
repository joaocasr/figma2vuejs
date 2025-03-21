<template>
<div class="grid-container">
 <div class="grid-item container2362312">
  <div class="grid-item rectangle2362313">
  </div>
  <p class="grid-item text2362314">
   1
  </p>
 </div>
 <Homebanner></Homebanner>
 <Footer></Footer>
 <div class="grid-item container2362318">
  <Movie1></Movie1>
  <Movie2></Movie2>
  <Movie3></Movie3>
  <Movie4></Movie4>
  <Movie5></Movie5>
  <Movie6></Movie6>
  <Movie7></Movie7>
  <Movie8></Movie8>
 </div>
 <IconField class="ssearchinputfilter2377217">
  <InputIcon class="pi pi-search">
  </InputIcon>
  <InputText placeholder="Search . . ." v-model="inputsearch2377217">
  </InputText>
 </IconField>
 <Navbar></Navbar>
 <div class="grid-item container2442234">
  <p class="grid-item text2442235">
   Upcoming Movies
  </p>
  <div class="grid-item container2442236">
   <img class="grid-item container2442237" src="/joker.png"/>
   <div class="grid-item container2442238">
    <p class="grid-item text2442239">
     Joker: Folie à Deux
    </p>
   </div>
   <div class="grid-item container2442240">
    <p class="grid-item text2442241">
     Oct 02, 2024
    </p>
   </div>
  </div>
  <div class="grid-item container2442242">
   <img class="grid-item container2442243" src="/wolverine.png"/>
   <div class="grid-item container2442244">
    <p class="grid-item text2442245">
     Deadpool &amp; Wolverine
    </p>
   </div>
   <div class="grid-item container2442246">
    <p class="grid-item text2442247">
     Jul 24, 2024
    </p>
   </div>
  </div>
 </div>
 <div class="grid-item container2442248">
  <div class="grid-item rectangle2454254">
   <img class="grid-item container2442252" src="/tapevector.svg"/>
   <p class="grid-item text2442251">
    BROWSE ALL MOVIES
   </p>
   <img class="grid-item container2442250" src="/govector.svg"/>
  </div>
 </div>
</div>

</template>

<script>
import Homebanner from '@/components/Homebanner.vue';
import Footer from '@/components/Footer.vue';
import Movie1 from '@/components/Movie1.vue';
import Movie2 from '@/components/Movie2.vue';
import Movie3 from '@/components/Movie3.vue';
import Movie4 from '@/components/Movie4.vue';
import Movie5 from '@/components/Movie5.vue';
import Movie6 from '@/components/Movie6.vue';
import Movie7 from '@/components/Movie7.vue';
import Movie8 from '@/components/Movie8.vue';
import Navbar from '@/components/Navbar.vue';

export default {
    components:{
        Homebanner,
        Footer,
        Movie1,
        Movie2,
        Movie3,
        Movie4,
        Movie5,
        Movie6,
        Movie7,
        Movie8,
        Navbar
    },
    data(){
        return {
            inputsearch2377217:""    
        }
    },
    methods:{
		gotoMoviePage(){
            this.$router.push({path:"/moviepage"});
        },
		gotoMoviePage(){
            this.$router.push({path:"/moviepage"});
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
@import '../assets/homepage.css';
</style>