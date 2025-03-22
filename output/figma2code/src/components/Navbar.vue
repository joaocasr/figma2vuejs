<template>
<div class="grid-item-2362644 component2362644">
 <img class="grid-item container2362353" src="/48311921.png"/>
 <p class="grid-item-2362644 text2362354" v-on:click="gotoHomePage()">
  MOVIESTV
 </p>
 <div class="grid-item-2362644 container2362355">
  <p class="grid-item-2362644 text2362356" v-on:click="gotoHomePage()">
   Home
  </p>
  <p class="grid-item-2362644 text2362357">
   Movies
  </p>
  <p class="grid-item-2362644 text2362358">
   Series
  </p>
  <div class="grid-item-2362644 container2402193">
   <div class="grid-item-2362644 container2402194" v-on:click="gotoWatchlistPage()">
    <img class="grid-item container2402195" src="/listVector.svg"/>
   </div>
   <div class="grid-item-2362644 container2402201">
    <div class="grid-item-2362644 container2402202">
     <img class="grid-item container2402203" src="/bodyVector.svg"/>
     <img class="grid-item container2402204" src="/headVector.svg"/>
    </div>
   </div>
   <div class="grid-item-2362644 container2402196">
    <img class="grid-item container2402197" src="/heartVector.svg"/>
   </div>
  </div>
 </div>
</div>

</template>

<script>
export default {
    data(){
        return {
           
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
@import '../assets/navbar.css';
</style>