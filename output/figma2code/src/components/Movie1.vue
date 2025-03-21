<template>
<div class="grid-item-2362319 component2362319">
    <img class="grid-item containerI23623192362514" src="/image10.png" v-on:click="gotoMoviePage()"/>
    <div class="grid-item-2362319 containerI23623192362515">
        <p class="grid-item-2362319 textI23623192362516" v-on:click="gotoMoviePage()">Avatar</p>
        <p class="grid-item-2362319 textI23623192362517">1h,34min</p>
        <p class="grid-item-2362319 textI23623192362518">10 Oct 2021</p>
    </div>
    <div class="grid-item-2362319 rectangleI23623192362526">
        <p class="grid-item-2362319 textI23623192379197">4.5</p>
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
		gotoMoviePage(){
            this.$router.push({path:"/moviepage"});
        },
		gotoMoviePage(){
            this.$router.push({path:"/moviepage"});
        }
	}
}
</script>
<style lang="css" scoped>
@import '../assets/movie1.css';
</style>