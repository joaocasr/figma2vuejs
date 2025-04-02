<template>
<div>
 <img class="grid-item-2362316 container2362370" src="/maxresdefault1.png"/>
 <div class="grid-item-2362316 container2362371">
 </div>
 <p class="grid-item-2362316 text2362372">
  Movie from 2017
 </p>
 <p class="grid-item-2362316 text2362373">
  Online Movie- Duration: 1h, 46min
 </p>
 <p class="grid-item-2362316 text2362374">
  7.8/10
 </p>
 <div @mouseenter="changeVisibility26211200" @mouseleave="changeVisibility26211200" class="grid-item-2362316 container2362375">
  <p class="grid-item-2362316 text2362376">
   Watch Trailer
  </p>
  <div class="grid-item-2362316 regular_polygon2362377">
  </div>
 </div>
 <div class="grid-item-2362316 container2362378">
  <p class="grid-item-2362316 text2362379">
   Watch Online Now
  </p>
  <div class="grid-item-2362316 regular_polygon2362380">
  </div>
 </div>
 <p class="grid-item-2362316 text2362381">
  Allied soldiers from Belgium, the British Commonwealth and Empire, and France  are surrounded by the German Army and evacuated during a fierce battle  in World War II.
 </p>
 <p class="grid-item-2362316 text2362382">
  Dunkirk
 </p>
 <div class="grid-item-2362316 container26211200" v-show="show26211200==true">
  <p class="grid-item-2362316 text26211201">
   HOME
  </p>
 </div>
</div>

</template>

<script>
export default {
    data(){
        return {
        show26211200:false   
        }
    },
    methods:{
		changeVisibility26211200(){
            this.show26211200 = !this.show26211200;
        }
	}
}
</script>
<style lang="css" scoped>
@import '../assets/homebanner.css';
</style>