<template>
<div class="grid-item-2362319 component2362319">
 <img class="grid-item container2362514" src="/image10.png" v-on:click="gotoMoviePage()"/>
 <div class="grid-item-2362319 container2362515">
  <p class="grid-item-2362319 text2362516" v-on:click="gotoMoviePage()">
   Avatar
  </p>
  <p class="grid-item-2362319 text2362517">
   1h,34min
  </p>
  <p class="grid-item-2362319 text2362518">
   10 Oct 2021
  </p>
 </div>
 <div class="grid-item-2362319 rectangle2362526">
  <p class="grid-item-2362319 text2379197">
   3.0
  </p>
 </div>
 <v-rating :length="5" :model-value="starsSeletec2465436" :size="25" class="srating2465436"  half-increments hover readonly >
 </v-rating>
</div>

</template>

<script>
export default {
    data(){
        return {
        starsSeletec2465436:"3"   
        }
    },
    methods:{
		gotoMoviePage(){
            this.$router.push({path:"/moviepage"});
        },
		gotoMoviePage(){
            this.$router.push({path:"/moviepage"});
        }
	}
}
</script>
<style lang="css" scoped>
@import '../assets/movie1.css';
</style>