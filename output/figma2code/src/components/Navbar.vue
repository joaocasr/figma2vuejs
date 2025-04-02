<template>
<div>
 <img class="grid-item-2548575 container2362353" src="/48311921.png"/>
 <p class="grid-item-2548575 text2362354" v-on:click="gotoHomePage()">
  MOVIESTV
 </p>
 <div class="grid-item-2548575 container2362355">
  <div class="grid-item-2548575 container2402193">
   <div class="grid-item-2548575 container2402194" v-on:click="gotoWatchlistPage()">
    <img class="grid-item-2548575 container2402195" src="/listVector.svg"/>
   </div>
   <div class="grid-item-2548575 container2402196">
    <img class="grid-item-2548575 container2402197" src="/heartVector.svg"/>
   </div>
   <div class="grid-item-2548575 smenu2575928">
    <v-menu>
     <template v-slot:activator="{ props }">
      <div v-bind="props">
       <img src="/iconMenu.png"/>
      </div>
     </template>
     <v-list>
      <v-list-item :key="index" :value="index" v-for="(item, index) in menuoptions2575928">
       <v-list-item-title @click="selectedItem2575928(item)">
        {{ item.option }}
       </v-list-item-title>
      </v-list-item>
     </v-list>
    </v-menu>
   </div>
  </div>
  <div class="grid-item-2548575 container2621776">
   <p class="grid-item-2548575 text2621777">
    HOME
   </p>
  </div>
  <div class="grid-item-2548575 container26211200">
   <p class="grid-item-2548575 text26211201">
    HOME
   </p>
  </div>
 </div>
</div>

</template>

<script>
export default {
    data(){
        return {
        menuoptions2575928:[{'option': 'Login', 'destination': '2548:560'}, {'option': 'Sign Up'}],
            show26211200:false   
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
@import '../assets/navbar.css';
</style>