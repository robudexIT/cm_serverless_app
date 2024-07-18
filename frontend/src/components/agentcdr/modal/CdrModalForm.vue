<template>
    <!-- <div>{{details}}</div> -->
    <div class="modal fade" :id="modalId" role="dialog">
    <div class="modal-dialog">

      <!-- Modal content-->
      <div class="modal-content">
        <div class="modal-header">

          <h4 class="modal-title">{{modalTitle}}</h4>
        </div>
        <div class="modal-body">
              <form :method="formMethod" :id="formId" @submit.prevent="submitFromData">
                  <template v-if="formId== 'commentTag' && modalId == 'modalCommentTag'"> 
                     <div class="mb-3">
                      <label for="Add Tag"  class="mb-3">Add Comment</label>
                     <textarea  class="form-control" cols="62" placeholder="Put Your Comment Here." :value="currentComment" @input="setNewComment"></textarea>
                   </div>
                    <div class="mb-3" v-if="mode=='tagandcomment'">
                        <label for="TagType" class="mb-2" >Select Tag:</label>
                        <select class="form-select"  :value="currentTag" @change="setNewTag">
                            <option v-for="tag in tags" :key="tag" :value="tag">{{tag}}</option>
                      </select>
                    </div>
                  </template>
                  
                  <hr>
                  <div class="row justify-content-end">
                    <div class="col-5 ">
                        <button type="button " class="btn btn-primary ml-auto m-1" data-bs-dismiss="modal" id="addbtn" >Submit</button>
                        <button type="button" class="btn btn-danger ml-auto "  data-bs-dismiss="modal" >Close</button>
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
    props:['modalId','modalTitle', 'formId', 'formMethod', 'mode','tags','currentComment','currentTag', 'callDetails'],
    data(){
        return{
            newTag: null,
            newComment: null,
            formIsValid: true,
        }
    },
    
    methods:{
        setNewTag(e){
            this.newTag = e.target.value
        },
        setNewComment(e){
            this.newComment = e.target.value
        },
        formValidation(){
            return this.formIsValid
        },
        submitFromData(){
            console.log('test')
            if(!this.formValidation()){
                return
            }
            const loggedInUserName = this.$store.getters['getLoggedinUserData'].name
      
            const data = {}
                data.starttimestamp = this.callDetails.starttimestamp;
                data.getdate = this.callDetails.getDate
                data.whoansweredcall = this.callDetails.extension
                data.caller = this.callDetails.Caller
                data.commentby = loggedInUserName

                if(this.newComment != null){
                    data.comment = this.newComment
                    this.newComment = null
                }    
               else {
                    data.comment = this.currentComment
                    this.newComment = null
                }
                if(this.mode == 'tagandcomment'){
                    if(this.newTag !=  null){
                        data.tag = this.newTag
                        this.newTag = null
                    }else{
                        data.tag = this.currentTag
                    }
                }
                
               this.$emit('emittedData', data)
        }

    },
    created(){
       
    }
}
</script>