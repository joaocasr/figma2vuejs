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
        }
	}
}
</script>
<style lang="css" scoped>
@import '../assets/homepage.css';
</style>