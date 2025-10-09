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
    <p class="progresstxt">{{progressMsg}}...{{ progress }}%</p>
    <ProgressBar class="progressbar" v-model="progress" :value="progress" ></ProgressBar>
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
    <InputText  fluid  name="input2316457" placeholder="Figma Prototype URL" type="text">
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
 <img src="/burger-menu.svg" @click="isExpanded=!isExpanded"  width="40px" class="menuburger"/>
    <aside v-show="isExpanded">
 
 <div class="gridformoption">
    
    <p class="gridformoptiona">Grid System Dimensions</p>
    
        <div class="gridform">
  <Form :initialValues="initialGridValues"  :resolver="resolverGridValues" :validateOnBlur="true" v-slot="$gridform">
   <br/>
   <div class="inputGridValuesColumns">
    <InputText v-model="nr_columns" fluid  name="inputColumns" placeholder="Number of Columns" min=1 type="number">
    </InputText>
    <Message severity="error" size="small" v-if="$gridform.inputColumns?.invalid" variant="simple">
     {{$gridform.inputColumns?.error.message}}
    </Message>
   </div>
   <br/>
   <div class="inputGridValuesRows">
    <InputText  v-model="nr_rows" fluid  name="inputRows" placeholder="Number of Rows"  min=1 type="number">
    </InputText>
    <Message severity="error" size="small" v-if="$gridform.inputRows?.invalid" variant="simple">
     {{$gridform.inputRows?.error.message}}
    </Message>
   </div>
   <br>
  </Form>
  
 </div>
</div>       
    </aside> 



 <Navigationbar class="grid-item-316718 component316718"></Navigationbar>
</div>

</template>

<script>
import axios from 'axios';
import Navigationbar from '@/components/Navigationbar.vue';
import { useToastStore } from "@/stores/toast";;
import { ref, onMounted  } from "vue";

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
            progressMsg:'Generating Vue project...',
            progress:0,
            nr_rows:'',
            nr_columns:'',
            progress:0,
            isExpanded:false
        }
    },
    setup(){

        const initialValues316457 = ref({
           input1316457: '',
           input2316457: '',
        });

        const initialGridValues = ref({
            inputColumns: '',
            inputRows: '',
        });
    
        const resolver316457 = ({ values }) => {
            const errors = {};
            if (!values.input1316457){
                errors.input1316457 = [{ message: 'Token account is required.'}];
            }
            let match = false
            var re = new RegExp("https:\/\/www.figma.com\/([a-zA-Z]+)\/.+");

            if (!values.input2316457){
                errors.input2316457 = [{ message: 'Prototype url is required.'}];
            }else{
                match=values.input2316457.match(re);
            }
            if(match===false){
                errors.input2316457 = [{ message: 'The url is not in the right format.'}];
            }
            return {
                errors
            };
        };
    
        const resolverGridValues = ({ values }) => {
            const errors = {};
           
            if(values.inputColumns!="" && values.inputRows==""){
                errors.inputColumns = [{ message: 'Your missing some grid values.'}];
            }
         
            if(values.inputRows!="" && values.inputColumns=="") {
                errors.inputRows = [{ message: 'Your missing some grid values.'}];
            }
            return {
                errors
            };
        };

        return {
            initialValues316457,
            initialGridValues,
            resolver316457,
            resolverGridValues
          }
	},methods:{
    async onFormSubmit316457(data) {
        this.showprogressbar= true
        const toastStore = useToastStore();
        let message = ""
        if(data.valid==true){
            let filekey = data.states.input2316457.value.split("/")
            if(filekey.length<5){
                return
            }else{
                filekey = filekey[4]
            }


            try{
                
                const result = await axios.post('http://localhost:8000/',
            {
                'apikey':data.states.input1316457.value,
                'filekey':filekey,
                'nrRows':this.nr_rows,
                'nrColumns':this.nr_columns,
            },
            {
                    responseType: 'blob',
                    onDownloadProgress: function(progressEvent){
                        let percentageComplete = Math.floor((progressEvent.loaded/progressEvent.total)*100)
                        //console.log(percentageComplete+"%")
                        self.progress = percentageComplete
                    }
                }
                )
                const filename = result.data
                const self = this
                this.progressMsg = "Getting Vue zip file from project..."
                this.progress = 0
                const resp = await axios.get(`http://localhost:8000/download?path=${filename}`, {
                    responseType: 'blob',
                    onDownloadProgress: function(progressEvent){
                        let percentageComplete = Math.floor((progressEvent.loaded/progressEvent.total)*100)
                        //console.log(percentageComplete+"%")
                        self.progress = percentageComplete
                    }
                });
                const blob = new Blob([resp.data], { type: 'application/zip' });
                fileUrl.value = URL.createObjectURL(blob);
                fileName.value = filename + ".zip";

                const link = this.$refs.downloadLink;
                link.href = fileUrl.value
                link.download = fileName.value
                link.click();
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
                message = "Error while downloading the Vue project generated!"            
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