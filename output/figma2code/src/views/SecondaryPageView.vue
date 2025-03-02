<template>
<div class="grid-container">
    <p class="grid-item text433701">THIS IS THE SECONDARY PAGE</p>
    <div class="grid-item container4338808" v-on:click="gotoPrincipalPage()">
        <p class="grid-item text4338809">Go Back</p>
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
		gotoPrincipalPage(){
            this.$router.push({path:"/principalpage"});
        }
	}
}
</script>
<style lang="css" scoped>
@import '../assets/secondarypage.css';
</style>