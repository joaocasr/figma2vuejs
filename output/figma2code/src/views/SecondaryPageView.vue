<template>
<div class="grid-container">
    <p class="grid-item text205314">THIS IS THE SECONDARY PAGE</p>
    <Backbutton></Backbutton>
</div>

</template>

<script>
import Backbutton from '@/components/Backbutton.vue';

export default {
    components:{
        Backbutton
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