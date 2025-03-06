<template>
<div class="grid-item component20983" v-on:click="gotoPrincipalPage()">
    <p class="grid-item textI20983205316">Go Back</p>
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
@import '../assets/backbutton.css';
</style>