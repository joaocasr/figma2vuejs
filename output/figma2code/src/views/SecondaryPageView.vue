<template>
<div class="grid-container">
 <p class="grid-item text222314">
  THIS IS THE SECONDARY PAGE
 </p>
 <Secondarybtn v-on:click="gotoPrincipalPage()"></Secondarybtn>
</div>

</template>

<script>
import Secondarybtn from '@/components/Secondarybtn.vue';

export default {
    components:{
        Secondarybtn
    },
    data(){
        return {
                
        }
    },
    methods:{
		gotoPrincipalPage(){
            this.$router.push({path:"/principalpage"});
        }
	}
}
</script>
<style lang="css" scoped>
@import '../assets/secondarypage.css';
</style>