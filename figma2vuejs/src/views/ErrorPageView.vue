<template>
    <div class="grid-container">
        <div class="grid-item carderror">
            <h1 class="grid-item txt1">Page Not Found</h1>
            <h2 class="grid-item txt2">404</h2>
        <p class="grid-item txt3">The page you are looking for doesn't exist. Return to Home Page</p>
        <button @click="returntopage" class="grid-item btn1">Home Page</button>
        </div>
    </div>
  </template>
<script>
export default{
    methods:{
        returntopage(){
            this.$router.push({path:'/'})
        }
    }
}
</script>
<style lang="css" scoped>
@import '../assets/errorpage.css';
</style>