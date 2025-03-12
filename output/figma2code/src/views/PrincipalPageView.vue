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
 <Iconi v-on:click="changeVisibility22238()"></Iconi>
 <Popup @close-from222310-to22238="show22238=false" v-if="show22238==true"></Popup>
</div>

</template>

<script>
import Iconi from '@/components/Iconi.vue';
import Popup from '@/components/Popup.vue';

export default {
    components:{
        Iconi,
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
        }
	}
}
</script>
<style lang="css" scoped>
@import '../assets/principalpage.css';
</style>