<template>
<div class="grid-item-222319 component222319" v-on:click="gotoPrincipalPage()">
    <p class="grid-item-222319 textI222319222316">Go Back</p>
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
@import '../assets/secondarybtn.css';
</style>