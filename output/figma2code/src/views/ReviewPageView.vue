<template>
<div class="grid-container">
 <Footer class="grid-item-2362643 component2362643"></Footer>
 <img class="grid-item container2362645" src="/image12.png"/>
 <div class="grid-item container2362674">
  <p class="grid-item text2362675">
   PUBLISH
  </p>
 </div>
 <p class="grid-item text2362676">
  AVATAR (2022)
 </p>
 <div class="grid-item container2442230">
  <div class="grid-item rectangle2442231">
   <p class="grid-item text2442232">
    Write down your review...
   </p>
  </div>
 </div>
 <div class="grid-item container2480491">
  <div class="grid-item container2480492">
   <p class="grid-item text2480493">
    Rate
   </p>
   <v-rating :length="5" :model-value="starsSeletec2480504" :size="25" class="srating2480504" half-increments="" hover="">
   </v-rating>
  </div>
 </div>
 <div class="form2538550">
  <Form  :initialValues="initialValues2538550" :resolver="resolver2538550"  :validateOnBlur="true" @submit="onFormSubmit2538550" v-slot="$form2538550">
   <div class="inputform2538550">
    <InputText  fluid  name="firstnamebox" placeholder="First Name" type="text">
    </InputText>
    <Message severity="error" size="small" v-if="$form2538550.firstnamebox?.invalid" variant="simple">
     {{$form2538550.firstnamebox?.error.message}}
    </Message>
   </div>
   <div class="inputform2538550">
    <InputText  fluid  name="lastnamebox" placeholder="Last Name" type="text">
    </InputText>
    <Message severity="error" size="small" v-if="$form2538550.lastnamebox?.invalid" variant="simple">
     {{$form2538550.lastnamebox?.error.message}}
    </Message>
   </div>
   <div class="inputform2538550">
    <InputText  fluid  name="usernamebox" placeholder="Username" type="text">
    </InputText>
    <Message severity="error" size="small" v-if="$form2538550.usernamebox?.invalid" variant="simple">
     {{$form2538550.usernamebox?.error.message}}
    </Message>
   </div>
   <button class="submitbtnform2538550" label="Submit" type="submit">
    Submit
   </button>
  </Form>
 </div>
 <Navbar class="grid-item-2362644 component2362644 posnavbar"></Navbar>
</div>

</template>

<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import { ref } from 'vue';

export default {
    components:{
        Navbar,
        Footer
    },
    data(){
        return {
            starsSeletec2480504:"5"    
        }
    },
    setup(){

        const initialValues2538550 = ref({
           firstnamebox: '',
           lastnamebox: '',
           usernamebox: '',
        });
    
        const resolver2538550 = ({ values }) => {
            const errors = {};
            if (!values.firstnamebox){
                errors.firstnamebox = [{ message: 'First Name is required.'}];
            }
        
            if (!values.lastnamebox){
                errors.lastnamebox = [{ message: 'Last Name is required.'}];
            }
        
            if (!values.usernamebox){
                errors.usernamebox = [{ message: 'Username is required.'}];
            }
        
       
            return {
                errors
            };
        };
    

        return {
            initialValues2538550,
            resolver2538550,
          }
	},methods:{
		gotoHomePage(){
            this.$router.push({path:"/homepage"});
        },
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
@import '../assets/reviewpage.css';
</style>