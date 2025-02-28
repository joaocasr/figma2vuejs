<template>
<div class="grid-container">
    <p class="grid-item text433697">THIS IS THE PRINCIPAL PAGE</p>
    <div class="grid-item container433698" v-on:click="gotoSecondaryPage()">
        <p class="grid-item text433699">Click Me</p>
    </div>
    <div class="grid-item container4338820">
        <p class="grid-item text4338822">i</p>
    </div>
</div>

</template>

<script>
export default {
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