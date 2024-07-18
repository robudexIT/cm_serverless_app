<template>
  <base-dialog :show="!!error" @close="handleError">
     <p>{{error}}</p>
   </base-dialog>
    <base-container>
          <div v-if="isLoading">
              <base-dialog :show="isLoading">
                  <base-spinner>
                     <p>Fetching Data From the Database Please Wait....</p>
                  </base-spinner>
              </base-dialog>
          </div>
          <div v-else>
              <base-table theader="tags" tableclass='tags'>
                  <tags-data-list :tdata="allTags" @click="deleteTag"></tags-data-list>
              </base-table>
              <management-modal-form 
                  modalId="modalTag"
                  modalTitle="Add Tag"
                  formId="addTag"
                  formMethod="POST"
                  @emittedData="addTag"   
              >
              </management-modal-form>

              <button type="button" class="btn btn-dark" data-bs-toggle="modal" :data-bs-target="dataBsTarget" dataset-backdrop="static" dataset-keyboard="false" id="add_tag">
              ADD TAG
              </button>
          </div>

    </base-container>
</template>

<script>
import TagsDataList from './data/TagsDataList.vue'
import ManagementModalForm from './modal/ManagementModalForm.vue'

export default {
    data(){
        return { 
            dataBsTarget: '#modalTag',
            isLoading: false,
            error: null,
            appName: this.$store.getters.getAppName
        }
    },
    components: {
        TagsDataList,
        ManagementModalForm
    },
    methods:{
       async fetchtAllTags(){
            try{
              this.isLoading = true
              await  this.$store.dispatch('tags/fetchAllTags')
              this.isLoading = false
            }catch(e){
                this.error = e.message
            }
        },
       async addTag(data){
         
           console.log('test')
            try {
               this.isLoading = true    
               await this.$store.dispatch('tags/createTag',data)
               this.isLoading = false   
                
            }catch(e){
                alert(e.message)
                this.error = e.message
            }
            
        },
        deleteTag(tagId){
            try{
                if(confirm(`Are you sure you want delete ${tagId} Tag? `)){
                    if(this.$store.dispatch('tags/deleteTag',{tagId})){
                      alert('Tag was successfully deleted')
                     }
                }
                
            }catch(e){
                this.error = e.message
            }
        },
        handleError(){
            this.error = null
        }
    },
    computed:{
        allTags(){
            return this.$store.getters['tags/getAllTags']
        
        },
         getAutoLogoutStatus(){
        return this.$store.getters['getAutoLogoutStatus']
        }
    },
    created(){
        this.$store.dispatch('checkIfCurrentLogin')
        this.fetchtAllTags()
        
    },
    watch:{
      getAutoLogoutStatus(currentstatus , oldstatus){
            if(currentstatus && currentstatus !== oldstatus){
             this.$router.replace('/'+this.appName+'/login')
        }
      }
    }


}
</script>