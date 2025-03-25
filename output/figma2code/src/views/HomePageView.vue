<template>
<div class="grid-container">
 <Homebanner class="grid-item-2362316 component2362316"></Homebanner>
 <Footer class="grid-item-2362317 component2362317"></Footer>
 <div class="grid-item container2362318">
  <Movie1 class="grid-item-2362319 component2362319"></Movie1>
  <Movie2 class="grid-item-2362320 component2362320"></Movie2>
  <Movie3 class="grid-item-2362321 component2362321"></Movie3>
  <Movie4 class="grid-item-2362322 component2362322"></Movie4>
  <Movie5 class="grid-item-2362323 component2362323"></Movie5>
  <Movie6 class="grid-item-2362324 component2362324"></Movie6>
  <Movie7 class="grid-item-2362325 component2362325"></Movie7>
  <Movie8 class="grid-item-2362326 component2362326"></Movie8>
 </div>
 <IconField class="ssearchinputfilter2377217">
  <InputIcon class="pi pi-search">
  </InputIcon>
  <InputText placeholder="Search . . ." v-model="inputsearch2377217">
  </InputText>
 </IconField>
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
 <v-pagination :length="68" :total-visible="3" class="spaginator2487476" v-model="currentPage2487476">
 </v-pagination>
 <Navbar class="grid-item-2362346 component2362346 posnavbar"></Navbar>
</div>

</template>

<script>
import Movie1 from '@/components/Movie1.vue';
import Movie4 from '@/components/Movie4.vue';
import Homebanner from '@/components/Homebanner.vue';
import Footer from '@/components/Footer.vue';
import Movie7 from '@/components/Movie7.vue';
import Movie2 from '@/components/Movie2.vue';
import Movie3 from '@/components/Movie3.vue';
import Navbar from '@/components/Navbar.vue';
import Movie6 from '@/components/Movie6.vue';
import Movie8 from '@/components/Movie8.vue';
import Movie5 from '@/components/Movie5.vue';

export default {
    components:{
        Movie1,
        Movie4,
        Homebanner,
        Footer,
        Movie7,
        Movie2,
        Movie3,
        Navbar,
        Movie6,
        Movie8,
        Movie5
    },
    data(){
        return {
            starsSeletec2465436:"3",
            starsSeletec2465418:"3",
            starsSeletec2473415:"3",
            starsSeletec2473395:"3",
            starsSeletec2473435:"3",
            starsSeletec2473303:"3",
            starsSeletec2473375:"3",
            starsSeletec2473355:"3",
            inputsearch2377217:"",
            currentPage2487476:1    
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