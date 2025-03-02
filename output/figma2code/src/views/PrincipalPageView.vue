<template>
<div class="grid-container">
    <p class="grid-item text20533">THIS IS THE PRINCIPAL PAGE</p>
    <div class="grid-item container20534" v-on:click="gotoSecondaryPage()">
        <p class="grid-item text20535">Click Me</p>
    </div>
    <div class="grid-item container20536">
        <p class="grid-item text20537">i</p>
    </div>
</div>

</template>

<script>

export default {
    components:{
        
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