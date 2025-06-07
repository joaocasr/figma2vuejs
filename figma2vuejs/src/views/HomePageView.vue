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
 <div v-if="showprogressbar" class="progressbarcard">
    <p class="progresstxt">{{progressMsg}}</p>
    <ProgressBar class="progressbar" :value="progress" />
 </div>

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
    <InputText  fluid  name="input2316457" placeholder="Figma Prototype File Key " type="text">
    </InputText>
    <Message severity="error" size="small" v-if="$form316457.input2316457?.invalid" variant="simple">
     {{$form316457.input2316457?.error.message}}
    </Message>
   </div>
   <button class="submitbtnform316457" label="Submit" type="submit">
    Generate
   </button>
   <br>
  <a v-show="showlink" ref="downloadLink" :href="fileUrl" :download="fileName">Download File</a>
  </Form>
 </div>
 <Navigationbar class="grid-item-316718 component316718"></Navigationbar>
</div>

</template>

<script>
import axios from 'axios';
import Navigationbar from '@/components/Navigationbar.vue';
import { useToastStore } from "@/stores/toast";;
import { ref } from "vue";

const fileUrl = ref(null)
const fileName = ref('')
export default {
    components:{
        Navigationbar
    },
    data(){
        return {
            showlink:false,
            showprogressbar:false,
            progress:10,
            progressMsg:'Generating Vue project...'
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
                errors.input1316457 = [{ message: 'Token account is required.'}];
            }
        
            if (!values.input2316457){
                errors.input2316457 = [{ message: 'Prototype file key is required.'}];
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
    async onFormSubmit316457(data) {
        this.showprogressbar= true
        const toastStore = useToastStore();
        let message = ""
        if(data.valid==true){
            try{
                
                const result = await axios.post('http://localhost:8000/',
            {
                'apikey':data.states.input1316457.value,
                'filekey':data.states.input2316457.value
            }
                )
                this.progress = 60
                this.progressMsg = "Vue project generated. Compressing and sending..."
                const filename = result.data
                const resp = await axios.get(`http://localhost:8000/download?path=${filename}`, {
                    responseType: 'blob'
                });
                this.progress = 80
                const blob = new Blob([resp.data], { type: 'application/zip' });
                fileUrl.value = URL.createObjectURL(blob);
                fileName.value = filename + ".zip";

                const link = this.$refs.downloadLink;
                link.href = fileUrl.value
                link.download = fileName.value
                link.click();
                this.progress = 100
                setTimeout(() => {
                    URL.revokeObjectURL(fileUrl.value);
                }, 1000);
                message = "Prototype converted successfully!"
                toastStore.showSuccess(message);
                this.showprogressbar = false
            }catch(err){
                console.log(err)
            }        
            if(data.valid==false){
                message = "Error in form submission!"            
                toastStore.showError(message);
            }
        }
    }
    
	}
}
</script>
<style lang="css" scoped>
@import '../assets/homepage.css';
</style>