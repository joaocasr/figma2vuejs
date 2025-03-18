<template>
<div class="grid-item-2362644 component2362644">
    <img class="grid-item containerI23626442362353" src="/48311921.png"/>
    <p class="grid-item-2362644 textI23626442362354">MOVIESTV</p>
    <div class="grid-item-2362644 containerI23626442362355">
        <p class="grid-item-2362644 textI23626442362356">Home</p>
        <p class="grid-item-2362644 textI23626442362357">Movies</p>
        <p class="grid-item-2362644 textI23626442362358">Series</p>
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
		gotoHomePage(){
            this.$router.push({path:"/homepage"});
        }
	}
}
</script>
<style lang="css" scoped>
@import '../assets/navbar.css';
</style>