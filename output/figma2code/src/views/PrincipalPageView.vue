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
 <VueSelect :is-multi="False" :options="allOptions22801349" class="grid-item vueselect22801349" placeholder="My Dropdown Filter" v-model="selectedOption22801349"/>
 <Popup @close-from222310-to22238="show22238=false" v-if="show22238==true"></Popup>
</div>

</template>

<script>
import Iconi from '@/components/Iconi.vue';
import Popup from '@/components/Popup.vue';
import VueSelect from "vue3-select-component";

export default {
    components:{
        Iconi,
        Popup,
        VueSelect
    },
    data(){
        return {
            show22238:false,
            selectedOption22801349:"",
            allOptions22801349:[{'label': 'Option 1', 'value': 'Label1'}, {'label': 'Option 2', 'value': 'Label2'}, {'label': 'Option 3', 'value': 'Label3'}, {'label': 'Option 4', 'value': 'Label4'}, {'label': 'Option 5', 'value': 'Label5'}]    
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