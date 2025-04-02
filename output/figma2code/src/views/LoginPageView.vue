<template>
<div class="grid-container">
 <Footer class="grid-item-2548561 component2548561"></Footer>
 <img class="grid-item container2549596" src="/photo14895998499272ee91cede3ba1.png"/>
 <img class="grid-item container2549626" src="/48311921.png"/>
 <div class="grid-item container2548653">
  <div class="form2549619">
   <Form  :initialValues="initialValues2549619" :resolver="resolver2549619"  :validateOnBlur="true" @submit="onFormSubmit2549619" v-slot="$form2549619">
    <div class="inputform2549619">
     <InputText  fluid  name="firstnamebox" placeholder="Password" type="text">
     </InputText>
     <Message severity="error" size="small" v-if="$form2549619.firstnamebox?.invalid" variant="simple">
      {{$form2549619.firstnamebox?.error.message}}
     </Message>
    </div>
    <div class="inputform2549619">
     <InputText  fluid  name="usernamebox" placeholder="Username" type="text">
     </InputText>
     <Message severity="error" size="small" v-if="$form2549619.usernamebox?.invalid" variant="simple">
      {{$form2549619.usernamebox?.error.message}}
     </Message>
    </div>
    <button class="submitbtnform2549619" label="Submit" type="submit">
     Login
    </button>
   </Form>
  </div>
  <div class="scheckbox2549638">
   <div :key="box.key" v-for="box of boxes2549638">
    <Checkbox :inputid="box.key" :value="box.name" name="box" v-model="selectedCategories">
    </Checkbox>
    <label :for="box.key" class="labelscheckbox2549638">
     {{ box.name }}
    </label>
   </div>
  </div>
  <p class="grid-item text2549628">
   Forgot your password?
  </p>
 </div>
 <Navbar class="grid-item-2548575 component2548575 posnavbar"></Navbar>
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
            boxes2549638:[],
            boxesValues2549638:[{'name': 'Remember Me', 'key': 'Checkbox'}],
            selectedBoxes2549638:[],
            menuoptions2575928:[{'option': 'Login', 'destination': '2548:560'}, {'option': 'Sign Up'}]    
        }
    },
    setup(){

        const initialValues2549619 = ref({
           firstnamebox: '',
           usernamebox: '',
        });
    
        const resolver2549619 = ({ values }) => {
            const errors = {};
            if (!values.firstnamebox){
                errors.firstnamebox = [{ message: 'Password is required.'}];
            }
        
            if (!values.usernamebox){
                errors.usernamebox = [{ message: 'Username is required.'}];
            }
        
       
            return {
                errors
            };
        };
    

        return {
            initialValues2549619,
            resolver2549619,
          }
	},methods:{
        getCheckboxOptions2549638(){
            /*Here you can adapt to fetch the data from an API*/
            this.boxes2549638 = this.boxesValues2549638;
        },
		gotoHomePage(){
            this.$router.push({path:"/homepage"});
        },
		gotoWatchlistPage(){
            this.$router.push({path:"/watchlistpage"});
        },
        selectedItem2575928(){
               this.$router.push({path:"/loginpage"});

            }
	},mounted(){
        this.getCheckboxOptions2549638();
	}
}
</script>
<style lang="css" scoped>
@import '../assets/loginpage.css';
</style>