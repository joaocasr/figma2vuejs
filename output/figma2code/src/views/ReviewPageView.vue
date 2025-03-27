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
 <div class="form2545550">
  <Form  :initialValues="initialValues2545550" :resolver="resolver2545550"  :validateOnBlur="true" @submit="onFormSubmit2545550" v-slot="$form2545550">
   <div class="inputform2545550">
    <InputText  fluid  name="firstnamebox" placeholder="First Name" type="text">
    </InputText>
    <Message severity="error" size="small" v-if="$form2545550.firstnamebox?.invalid" variant="simple">
     {{$form2545550.firstnamebox?.error.message}}
    </Message>
   </div>
   <div class="inputform2545550">
    <InputText  fluid  name="lastnamebox" placeholder="Last Name" type="text">
    </InputText>
    <Message severity="error" size="small" v-if="$form2545550.lastnamebox?.invalid" variant="simple">
     {{$form2545550.lastnamebox?.error.message}}
    </Message>
   </div>
   <div class="inputform2545550">
    <InputText  fluid  name="usernamebox" placeholder="Username" type="text">
    </InputText>
    <Message severity="error" size="small" v-if="$form2545550.usernamebox?.invalid" variant="simple">
     {{$form2545550.usernamebox?.error.message}}
    </Message>
   </div>
   <button class="submitbtnform2545550" label="Submit" type="submit">
    Submit
   </button>
  </Form>
 </div>
 <div class="scheckbox2546595">
  <div :key="box.key" v-for="box of boxes2546595">
   <Checkbox :inputid="box.key" :value="box.name" name="box" v-model="selectedCategories">
   </Checkbox>
   <label :for="box.key" class="labelscheckbox2546595">
    {{ box.name }}
   </label>
  </div>
 </div>
 <Navbar class="grid-item-2362644 component2362644 posnavbar"></Navbar>
</div>

</template>

<script>
import Footer from '@/components/Footer.vue';
import Navbar from '@/components/Navbar.vue';
import { ref } from 'vue';

export default {
    components:{
        Footer,
        Navbar
    },
    data(){
        return {
            starsSeletec2480504:"5",
            boxes2546595:[],
            boxesValues2546595:[{'name': 'Romance', 'key': 'Checkbox'}, {'name': 'Sci-fi', 'key': 'Checkbox'}, {'name': 'Horror', 'key': 'Checkbox'}, {'name': 'Comedy', 'key': 'Checkbox'}],
            selectedBoxes2546595:[]    
        }
    },
    setup(){

        const initialValues2545550 = ref({
           firstnamebox: '',
           lastnamebox: '',
           usernamebox: '',
        });
    
        const resolver2545550 = ({ values }) => {
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
            initialValues2545550,
            resolver2545550,
          }
	},methods:{
        getCheckboxOptions2546595(){
            /*Here you can adapt to fetch the data from an API*/
            this.boxes2546595 = this.boxesValues2546595;
        },
		gotoHomePage(){
            this.$router.push({path:"/homepage"});
        },
		gotoHomePage(){
            this.$router.push({path:"/homepage"});
        },
		gotoWatchlistPage(){
            this.$router.push({path:"/watchlistpage"});
        }
	},mounted(){
        this.getCheckboxOptions2546595();
	}
}
</script>
<style lang="css" scoped>
@import '../assets/reviewpage.css';
</style>