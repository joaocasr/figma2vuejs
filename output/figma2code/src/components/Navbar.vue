<template>
<div class="grid-item-2362644 component2362644">
    <img class="grid-item containerI23626442362353" src="/48311921.png"/>
    <p class="grid-item-2362644 textI23626442362354" v-on:click="gotoHomePage()">MOVIESTV</p>
    <div class="grid-item-2362644 containerI23626442362355">
        <p class="grid-item-2362644 textI23626442362356">Home</p>
        <p class="grid-item-2362644 textI23626442362357">Movies</p>
        <p class="grid-item-2362644 textI23626442362358">Series</p>
        <div class="grid-item-2362644 containerI23626442402193">
            <div class="grid-item-2362644 containerI23626442402194" v-on:click="gotoWatchlistPage()">
                <img class="grid-item containerI23626442402195" src="/listVector.svg"/>
            </div>
            <div class="grid-item-2362644 containerI23626442402201">
                <div class="grid-item-2362644 containerI23626442402202">
                    <img class="grid-item containerI23626442402203" src="/bodyVector.svg"/>
                    <img class="grid-item containerI23626442402204" src="/headVector.svg"/>
                </div>
            </div>
            <div class="grid-item-2362644 containerI23626442402196">
                <img class="grid-item containerI23626442402197" src="/heartVector.svg"/>
            </div>
        </div>
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
        },
		gotoWatchlistPage(){
            this.$router.push({path:"/watchlistpage"});
        }
	}
}
</script>
<style lang="css" scoped>
@import '../assets/navbar.css';
</style>