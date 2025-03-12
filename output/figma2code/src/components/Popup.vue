<template>
<div class="grid-item-22238 component22238">
    <p class="grid-item-22238 text22239">This page was created by João Castro.</p>
    <div class="grid-item-22238 container222310" v-on:click="close22238()">
        <div class="grid-item-22238 line222311"/>
        <div class="grid-item-22238 line222312"/>
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
		close22238(){
            this.$emit('closeFrom222310To22238');
        }
	}
}
</script>
<style lang="css" scoped>
@import '../assets/popup.css';
</style>