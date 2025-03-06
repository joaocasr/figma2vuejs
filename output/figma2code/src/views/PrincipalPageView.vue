<template>
<div class="grid-container">
    <p class="grid-item text20533">THIS IS THE PRINCIPAL PAGE</p>
    <div class="grid-item container20534" v-on:click="gotoSecondaryPage()">
        <p class="grid-item text20535">Click Me</p>
    </div>
    <div class="grid-item container20536">
        <p class="grid-item text20537">i</p>
    </div>
    <Popup></Popup>
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
        }
    },
    methods:{
		gotoSecondaryPage(){
            this.$router.push({path:"/secondarypage"});
        }
	}
}
</script>
<style lang="css" scoped>
@import '../assets/principalpage.css';
</style>