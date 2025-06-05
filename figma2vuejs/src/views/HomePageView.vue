<template>
<div class="grid-container">
 <p class="grid-item text31635">
  Turn your Figma prototypes
  <br/>
  into fully functional Vue.js projects
 </p>
 <p class="grid-item text31637">
  Figma2Vuejs
 </p>
 <div class="form316457">
  <Form  :initialValues="initialValues316457" :resolver="resolver316457"  :validateOnBlur="true" @submit="onFormSubmit316457" v-slot="$form316457">
   <br/>
   <div class="inputform316457">
    <InputText  fluid  name="input1316457" placeholder="Figma Token Account" type="text">
    </InputText>
    <Message severity="error" size="small" v-if="$form316457.input1316457?.invalid" variant="simple">
     {{$form316457.input1316457?.error.message}}
    </Message>
   </div>
   <br/>
   <div class="inputform316457">
    <InputText  fluid  name="input2316457" placeholder="Figma URL prototype" type="text">
    </InputText>
    <Message severity="error" size="small" v-if="$form316457.input2316457?.invalid" variant="simple">
     {{$form316457.input2316457?.error.message}}
    </Message>
   </div>
   <button class="submitbtnform316457" label="Submit" type="submit">
    Generate
   </button>
  </Form>
 </div>
 <Navigationbar class="grid-item-316718 component316718"></Navigationbar>
</div>

</template>

<script>
import Navigationbar from '@/components/Navigationbar.vue';
import { useToastStore } from "@/stores/toast";;
import { ref } from 'vue';
export default {
    components:{
        Navigationbar
    },
    data(){
        return {
                
                
        }
    },
            setup(){

        const initialValues316457 = ref({
           input1316457: '',
           input2316457: '',
        });
    
        const resolver316457 = ({ values }) => {
            const errors = {};
            if (!values.input1316457){
                errors.input1316457 = [{ message: 'Token is required.'}];
            }
        
            if (!values.input2316457){
                errors.input2316457 = [{ message: 'URL is required.'}];
            }
        
       
            return {
                errors
            };
        };
    

        return {
            initialValues316457,
            resolver316457,
          }
	},methods:{
    onFormSubmit316457(data) {
        const toastStore = useToastStore();
        let message = ""
        if(data.valid==true){
            message = "The form was successfully submited!"            
            toastStore.showSuccess(message);
        }
        if(data.valid==false){
            message = "Error in form submission!"            
            toastStore.showError(message);
        }
    }
    
	}
}
</script>
<style lang="css" scoped>
@import '../assets/homepage.css';
</style>