<template>
<div class="grid-item-2362620 component2362620">
    <div class="grid-item-2362620 container2362622" v-on:click="close2362620()">
        <p class="grid-item-2362620 text2362623">No, Cancel</p>
    </div>
    <div class="grid-item-2362620 container2362624" v-on:click="close2362620()">
        <p class="grid-item-2362620 text2362625">Yes, Insert</p>
    </div>
    <p class="grid-item-2362620 text2362626">Are you sure you want to add this movie to watchlist?</p>
    <p class="grid-item-2362620 text2362627">Insert to Watchlist</p>
</div>

</template>

<script>
export default {
    data(){
        return {
        }
    },
    methods:{
		close2362620(){
            this.$emit('close-from2362622-to2362620');
        },
		close2362620(){
            this.$emit('close-from2362624-to2362620');
        }
	}
}
</script>
<style lang="css" scoped>
@import '../assets/confirmationwatchlistmodal.css';
</style>