<template>
<div class="grid-item-2362634 component2362634">
    <div class="grid-item-2362634 container2362636" v-on:click="close2362634()">
        <p class="grid-item-2362634 text2362637">No, Cancel</p>
    </div>
    <div class="grid-item-2362634 container2362638" v-on:click="close2362634()">
        <p class="grid-item-2362634 text2362639">Yes, Delete</p>
    </div>
    <p class="grid-item-2362634 text2362640">Are you sure you want to delete all the movies from your watchlist?</p>
    <p class="grid-item-2362634 text2362641">Clear Watchlist</p>
</div>

</template>

<script>
export default {
    data(){
        return {
        }
    },
    methods:{
		close2362634(){
            this.$emit('close-from2362636-to2362634');
        },
		close2362634(){
            this.$emit('close-from2362638-to2362634');
        }
	}
}
</script>
<style lang="css" scoped>
@import '../assets/deletionwatchlistmodal.css';
</style>