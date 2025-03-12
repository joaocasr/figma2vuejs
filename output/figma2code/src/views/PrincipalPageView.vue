<template>
<div class="grid-container">
 <p class="grid-item text22233">
  THIS IS THE PRINCIPAL PAGE
 </p>
 <div class="grid-item container22234" v-on:click="gotoSecondaryPage()">
  <p class="grid-item text22235">
   Click Me
  </p>
 </div>
 <div class="grid-item container22236" v-on:click="changeVisibility22238()">
  <p class="grid-item text22237">
   i
  </p>
 </div>
 <Popup @closefrom222310to22238="show22238=false" v-if="show22238==true"></Popup>
</div>

</template>

<script>
import Popup from '@/components/Popup.vue';

export default {
    components:{
        Popup
    },
    data(){
        return {
            show22238:false    
        }
    },
    methods:{
		gotoSecondaryPage(){
            this.$router.push({path:"/secondarypage"});
        },
		changeVisibility22238(){
            this.show22238 = true;
        },
		close22238(){
            this.$emit('closeFrom222310To22238');
        }
	}
}
</script>
<style lang="css" scoped>
@import '../assets/principalpage.css';
</style>