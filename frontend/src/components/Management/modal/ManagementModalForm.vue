<template>
    
    <div class="modal fade" :id="modalId" role="dialog">
    <div class="modal-dialog">

      <!-- Modal content-->
      <div class="modal-content">
        <div class="modal-header">

          <h4 class="modal-title">{{modalTitle}}</h4>
        </div>
        <div class="modal-body">
              <form :method="formMethod" :id="formId" @submit.prevent="submitFromData">
                  <template v-if="formId== 'addTag' && modalId == 'modalTag'"> 
                    <div :class="errorDiv">
                        <p class="errorP"  v-if="!mdlIsValid">Please Make Sure That Dont Leave Blank on the Input Fields</p>
                      <div class="mb-3">
                        <label for="Add Tag"  class="mb-3">Add Tag</label>
                        <input type="text" class="form-control" id="tag" aria-describedby="tag" v-model="mdlTag.val">
                        <div id="tagdesc" class="form-text">All tag must be unique.</div>
                      </div>
                      <div class="mb-3">
                          <label for="TagType" class="mb-2" >Select TagType:</label>
                          <select class="form-select" aria-label="Default select example" v-model="mdlTagType.val">
                              <option value="CSDINBOUND">CSD-INBOUND</option>
                              <option value="CSDOUTBOUND">CSD-OUTBOUND</option>
                              <option value="COLLECTION">COLLECTION</option>
                          </select>
                      </div>
                    </div>
                  </template>
                  <template v-if="formId=='addAgent' && modalId=='modalAgent'">
                    <div :class="errorDiv">
                      <p class="errorP"  v-if="!mdlIsValid">Please Make Sure That Dont Leave Blank on the Input Fields</p>
                      <div class="mb-3">
                        <label for="Name"  class="mb-3">Name</label>
                        <input type="text" class="form-control" id="name" aria-describedby="name" placeholder='Agent Name' v-model="mdlName.val" >
                      </div>
                      <div class="mb-3">
                        <label for="Email Address"  class="mb-3">Email Address</label>
                        <input type="email" class="form-control" id="email" aria-describedby="email" placeholder='Enter Valid Email' v-model="mdlEmail.val">
                      </div>
                      <div class="mb-3">
                        <label for="extension"  class="mb-3">Extension</label>
                        <input type="text" class="form-control" id="extension" aria-describedby="extension" placeholder='Enter Unique Ext.' v-model="mdlExt.val">
                      </div>
                      <div class="mb-3" v-if="agent =='sales'">
                          <label for="TagType" class="mb-2" >Select Team Leader:</label>
                          <select class="form-select" aria-label="Default select example" v-model="selectedTeamLeader.val">
                              <option v-for="teamlead in  salesTeamLeaders" :key="teamlead" :value="teamlead">{{teamlead}}</option>
                          </select>
                      </div>
                    </div>
                  </template>
                

                  <template v-if="formId=='updateAgent' && modalId=='updatemodalAgent' " >
                    <div :class="errorDiv">
                      <p class="errorP"  v-if="!mdlIsValid && noUpdate">No Found Changes </p>
                      <p class="errorP"  v-if="!mdlIsValid && blankFields">Please Make Sure That Dont Leave Blank on the Input Fields</p>
                      <div class="mb-3">
                        <label for="Name"  class="mb-3">Name</label>
                        <input type="text" class="form-control" id="updatename" aria-describedby="name" placeholder='Agent Name' :value="currentName" @input="setName">
                      </div>
                      <div class="mb-3">
                        <label for="Email Address"  class="mb-3">Email Address</label>
                        <input type="email" class="form-control" id="updateemail" aria-describedby="email" placeholder='Enter Valid Email' :value="currentEmail" @input="setEmail">
                      </div>
                      <div class="mb-3">
                        <label for="extension"  class="mb-3">Extension</label>
                        <input type="text" class="form-control" id="updateextension" aria-describedby="extension" placeholder='Enter Unique Ext.' :value="extension" disabled>
                      </div>

                      <div class="mb-3" v-if="agent =='sales'">
                          <label for="TagType" class="mb-2" >Select Team Leader:</label>
                          <select class="form-select" aria-label="Default select example"  :value="currentTeamLeader" @change="setTeamLeader">
                              <opttion :value="currentTeamLeader" selected>{{currentTeamLeader}}</opttion>
                              <option v-for="teamlead in  salesTeamLeaders" :key="teamlead" :value="teamlead">{{teamlead}}</option>
                          </select>
                      </div>
                   </div>
                  </template>

                  <hr>
                  <div class="row justify-content-end">
                    <div class="col-5 ">
                        <button type="button " class="btn btn-primary ml-auto m-1"   id="addbtn" >Submit</button>
                        <button type="button" class="btn btn-danger ml-auto "  data-bs-dismiss="modal" @click="resetInputs">Close</button>
                    </div>
  
                </div>
                 

          </form>
        </div>


      </div>

    </div>
  </div>


</template>

<script>
    export default {
        emits:['emittedData'],
        props: ['modalId','modalTitle', 'formId', 'formMethod','agent','currentName', 'currentEmail', 'extension','currentTeamLeader'],
        
        data(){
          return {
            mdlIsValid: true,
            mdlName: {
              val: null,
              isValid: true
            },
            mdlEmail: {
              val: null,
              isValid: true
            },
            mdlExt: {
              val: null,
              isValid: true
            } ,
            mdlTag: {
              val: null,
              isValid:true
            },
            mdlTagType: {
              val: null,
              isValid: true
            },
            selectedTeamLeader: {
              val: null,
              isValid: true 
            },
            updateName: null,
            updateEmail:null,
            updateTeamLeader:null
         
          }
        },
        computed:{
          salesTeamLeaders(){
            //available on sales only
            return this.$store.getters['agentinfo/getSalesTeamLeaders']
          },
          errorDiv(){
           return !this.mdlIsValid ? 'errorDiv' : ''
          },
          noUpdate(){
            return this.updateName == null && this.updateEmail == null  ?  true: false
          },
          blankFields(){
            return this.updateName == '' || this.updateEmail == '' ? true : false
          }
         
        },
        methods: {
            setName(e){
              this.updateName = e.target.value
              this.mdlIsValid = true
            },
            setEmail(e){
              this.updateEmail = e.target.value
              this.mdlIsValid = true
            },
            setTeamLeader(e){
              this.updateTeamLeader = e.target.value
              this.mdlIsValid = true
            },
            formValidation(){             
              this.mdlIsValid = true
              if(this.modalId == 'modalTag' && this.formId == 'addTag'){
                if((this.mdlTag.val == null || this.mdlTag.val == '') || 
                (this.mdlTagType.val == null || this.mdlTagType.val == '')){
                   alert('Blank Fields are not allowed.Please dont leave any blank fields before submitting the form')
                  this.mdlIsValid = false
                }
              }else if(this.modalId == 'modalAgent' && this.formId == 'addAgent'){
                if(this.agent == 'sales'){
                  if((this.mdlName.val == null || this.mdlName.val == '')  ||
                    (this.mdlEmail.val == null || this.mdlEmail.val == '') ||
                    (this.mdlExt.val == null || this.mdlExt.val == '')  ||
                     (this.selectedTeamLeader.val == null || this.selectedTeamLeader.val == '')){
                        alert('Blank Fields are not allowed.Please dont leave any blank fields before submitting the form')
                      this.mdlIsValid = false
                  }
                }
                else {
                    if((this.mdlName.val == null || this.mdlName.val == '') ||
                    (this.mdlEmail.val == null || this.mdlEmail.val == '') ||
                    (this.mdlExt.val == null || this.mdlExt.val == '')){    
                      alert('Blank Fields are not allowed.Please dont leave any blank fields before submitting the form')  
                    this.mdlIsValid = false
                  }
                }          
             
              }else if(this.formId=='updateAgent' && this.modalId=='updatemodalAgent'){
                 if(this.agent == 'sales'){
                   if(this.updateTeamLeader == null && this.updateName == null && this.updateEmail == null){
                       alert('No Found Changes')
                     this.mdlIsValid = false
                   }else if(this.updateTeamLeader == '' || this.updateName == '' || this.updateEmail == ''){
                       alert('Blank Fields are not allowed.Please dont leave any blank fields before submitting the form')
                     this.mdlIsValid = false
                   }
                 }else {
                   if(this.updateName == null && this.updateEmail == null){
                      alert('No Found Changes')
                     this.mdlIsValid = false
                   }else if(this.updateName == '' || this.updateEmail == ''){
                      alert('Blank Fields are not allowed.Please dont leave any blank fields before submitting the form')
                     this.mdlIsValid = false
                   }
                 }
              }
              return this.mdlIsValid
            },  
            resetInputs(){
                  this.mdlExt.val = null
                  this.mdlName.val = null
                  this.mdlEmail.val = null
                  this.selectedTeamLeader.val = null
                  this.updateName = null
                  this.updateEmail = null
                  this.updateTeamLeader = null
                  this.mdlIsValid = true
                
            },
           
            submitFromData(){
              if(!this.formValidation()){
               
                return
              }
            
              let data;
              if(this.modalId == 'modalTag' && this.formId == 'addTag'){
                  let d = new Date()
                  let month = d.getMonth()+1
                  let year = d.getFullYear()
                  let  day = d.getDate()
                  let createddate = `${year}-${month}-${day}`
                 data = {
                  createdby:  this.$store.getters['getLoggedinUserData'].name,//this.$store.getters.getUserName,
                  createddate: createddate,
                  tagname: this.mdlTag.val,
                  tagtype: this.mdlTagType.val
                }
                console.log(data)
              }else if(this.modalId == 'modalAgent' && this.formId == 'addAgent'){
                  data = {
                  name: this.mdlName.val,
                  email: this.mdlEmail.val,
                  extension: this.mdlExt.val
                }
                if(this.agent == 'sales'){
                  data.teamlead = this.selectedTeamLeader.val
                }
              }else if(this.formId=='updateAgent' && this.modalId=='updatemodalAgent'){
                  let name
                  let email
                  if(this.updateName !== null){
                    name = this.updateName
                  }else{
                    name = this.currentName
                  }

                  if(this.updateEmail !== null){
                    email = this.updateEmail
                  }else{
                    email = this.currentEmail

                  }
                  data = {
                  name: name,
                  email: email,
                  extension: this.extension
                }
                if(this.agent == 'sales'){
                  if(this.updateTeamLeader !== null){
                     data.teamlead = this.updateTeamLeader
                     this.updateTeamLeader = null
                    
                  }else{
                    data.teamlead = this.currentTeamLeader
                    this.updateTeamLeader = null
                  }
                 
                }
               
              }
              
              this.$emit('emittedData', data)
              this.resetInputs()
            }
        },
       
        
    }

</script>

<style scoped>
  .errorDiv {
    border: 5px solid red;
    padding: 10px;
   
  }
  .errorP{
    color:red;
  }
</style>