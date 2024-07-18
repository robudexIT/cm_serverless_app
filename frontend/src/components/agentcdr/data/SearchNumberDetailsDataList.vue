<template>
     <tr v-for="(item, index) in tdata" :key="index">
       
       <td>{{index+trimStart+1}}</td>
       <td v-if="calltype=='csdinbounddetails'">{{item.extension}}</td>
       <td>{{item.calledNumber}}</td>
       <td>{{item.caller}}</td>
       <td>{{item.callStatus}}</td>
       <td>{{item.startime}}</td>
       <td>{{item.endtime}}</td>
       <td>{{item.callDuration}}</td>
       <td>
			<audio :src="item.callrecording" controls="controls" style="width: 130px;"></audio>
		</td>
		<td>{{item.getDate}}</td>
		<td v-if="calltype=='salesdetails'">
			<button v-if="item.comment != '' " class="btn btn-info btn-sm text-justify text-white" type="button" data-bs-toggle="modal" :data-bs-target="dataBsTarget" dataset-backdrop="static" dataset-keyboard="false" @click="getCallsDetails(item)">View Comment</button>
            <button v-else class="btn btn-outline-info btn-sm text-justify " type="button" data-bs-toggle="modal" :data-bs-target="dataBsTarget" dataset-backdrop="static" dataset-keyboard="false" @click="getCallsDetails(item)"> Add Comment</button>
		</td>
        <td v-else>
			<button v-if="item.tag != '' " class="btn btn-info btn-sm text-justify text-white" type="button" data-bs-toggle="modal" :data-bs-target="dataBsTarget" dataset-backdrop="static" dataset-keyboard="false" @click="getCallsDetails(item)">{{item.tag}}</button>
            <button v-else class="btn btn-outline-info btn-sm text-justify " type="button" data-bs-toggle="modal" :data-bs-target="dataBsTarget" dataset-backdrop="static" dataset-keyboard="false" @click="getCallsDetails(item)"> NO TAG</button>
		</td>
     </tr>
     <cdr-modal-form
         modalId="modalCommentTag"
         modalTitle="Add Comment"
         formId="commentTag"
         formMethod="POST"
         mode="tag"
         :tags="tags"
         :calltype="calltype"
         :callDetails="callDetails"
         :currentComment="comment"
         :currentTag="tag"
         @emittedData="putCommentTag"
     ></cdr-modal-form>
   
</template>

<script>
    import CdrModalForm from '../modal/CdrModalForm.vue'
    
    export default {
       // props:['tdata','tags','calltype','trimStart',],
       props:{
           tdata: {
               type:Array,
               required: false
           },
           tags: {
               type: Array,
               required:false
           },
           calltype: {
               type: String,
               required: false,
           },
           trimStart: {
               type: Number,
               required: false
           }
          
       },
        data(){
            return {
                 dataBsTarget: '#modalCommentTag',
                 comment: null,
                 tag: null,
                 callDetails: null,
                 numberPerPage: 5,
                 currentPage: 1
            }
        },
       


        components: {
            CdrModalForm,
          
        },

        methods: {
            getCallsDetails(item){
                this.comment = item.comment
                this.tag = item.tag
                this.callDetails = item
            },
            putCommentTag(data){
                this.$emit('emittedData', data)
            },
           

        },
        created(){
           
        }
    }
    
</script>



