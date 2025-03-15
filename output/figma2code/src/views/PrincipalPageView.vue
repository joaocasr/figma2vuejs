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
 <IconField class="ssearchinputfilter23041263">
  <InputIcon class="pi pi-search">
  </InputIcon>
  <InputText placeholder="Search . . ." v-model="inputsearch23041263">
  </InputText>
 </IconField>
 <DatePicker :showonfocus="false" class="sdatepicker23201811"  showIcon fluid  v-model="datepicker23201811">
 </DatePicker>
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
            show22238:false,
            inputsearch23041263:"",
            datepicker23201811:""    
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