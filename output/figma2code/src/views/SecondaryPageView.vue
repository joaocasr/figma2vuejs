<template>
<div class="grid-container">
    <p class="grid-item text205314">THIS IS THE SECONDARY PAGE</p>
    <div class="grid-item container205315" v-on:click="gotoPrincipalPage()">
        <p class="grid-item text205316">Go Back</p>
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
		gotoPrincipalPage(){
            this.$router.push({path:"/principalpage"});
        }
	}
}
</script>
<style lang="css" scoped>
@import '../assets/secondarypage.css';
</style>