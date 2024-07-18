<template>
     <tr v-for="(item, index) in tdata" :key="index">
       <template v-if="activeRoutePath=='calldetails'">
       <td>{{index+trimStart+1}}</td>
       <td v-if="calltype=='csdinbounddetails'">{{item.extension}}</td>
       <td v-if="calltype=='csdinbounddetails'" >{{item.CalledNumber}}</td>
       <td v-else>
         <button v-if="item.isregistered == true" class="btn btn-info btn-sm text-justify text-white" type="button" data-bs-toggle="modal" data-bs-target="#customerModalFormId" dataset-backdrop="static" dataset-keyboard="false" @click="getCallsDetails(item)" >{{item.CalledNumber}}</button>
        <button v-else class="btn btn-outline-info btn-sm text-justify " type="button" data-bs-toggle="modal" data-bs-target="#customerModalFormId" dataset-backdrop="static" dataset-keyboard="false" @click="getCallsDetails(item)"> {{item.CalledNumber}}</button>
       </td>
       <!-- <td>{{item.caller}}</td> -->
       <td v-if="calltype=='csdinbounddetails'">
        <button v-if="item.isregistered == true" class="btn btn-info btn-sm text-justify text-white" type="button" data-bs-toggle="modal" data-bs-target="#customerModalFormId" dataset-backdrop="static" dataset-keyboard="false" @click="getCallsDetails(item)" >{{item.Caller}}</button>
        <button v-else class="btn btn-outline-info btn-sm text-justify " type="button" data-bs-toggle="modal" data-bs-target="#customerModalFormId" dataset-backdrop="static" dataset-keyboard="false" @click="getCallsDetails(item)"> {{item.Caller}}</button>
       </td>
       <td v-else>{{item.Caller}}</td>
       <td>{{item.CallStatus}}</td>
       <td>{{item.starttime}}</td>
       <td>{{item.endtime}}</td>
       <td>{{item.callDuration}} </td>
       <td>
			<audio :src="item.callrecording" controls="controls" style="width: 130px;"></audio>
		</td>
		<td>{{item.getDate}}</td>
		<td v-if="calltype=='salesdetails'">
			<button v-if="item.comment != '' " class="btn btn-info btn-sm text-justify text-white" type="button" data-bs-toggle="modal" :data-bs-target="dataBsTarget"   dataset-backdrop="static" dataset-keyboard="false" @click="getCallsDetails(item)">View Comment</button>
            <button v-else class="btn btn-outline-info btn-sm text-justify " type="button" data-bs-toggle="modal"  :data-bs-target="dataBsTarget"  dataset-backdrop="static" dataset-keyboard="false" @click="getCallsDetails(item)"> Add Comment</button>
		</td>
        <td v-else>
			<button v-if="item.tag != '' " class="btn btn-info btn-sm text-justify text-white" type="button" data-bs-toggle="modal" :data-bs-target="dataBsTarget" dataset-backdrop="static" dataset-keyboard="false" @click="getCallsDetails(item)">{{item.tag}}</button>
            <button v-else class="btn btn-outline-info btn-sm text-justify " type="button" data-bs-toggle="modal" :data-bs-target="dataBsTarget" dataset-backdrop="static" dataset-keyboard="false" @click="getCallsDetails(item)"> NO TAG</button>
		</td>
        </template>
        <template v-else-if="activeRoutePath=='searchnumberIn'">
            <td>{{index+trimStart+1}}</td>
            <td>{{item.name}}</td>
            <td>{{item.extension}}</td>
            <!-- <td>{{item.calledNumber}}</td> -->
            <td>
                
            </td>
            <td v-if="calltype=='csdinbounddetails'">
               <button v-if="item.isregistered == true" class="btn btn-info btn-sm text-justify text-white" type="button" data-bs-toggle="modal" data-bs-target="#customerModalFormId" dataset-backdrop="static" dataset-keyboard="false" @click="getCallsDetails(item)" >{{item.Caller}}</button>
               <button v-else class="btn btn-outline-info btn-sm text-justify " type="button" data-bs-toggle="modal" data-bs-target="#customerModalFormId" dataset-backdrop="static" dataset-keyboard="false" @click="getCallsDetails(item)"> {{item.Caller}}</button>
            </td>
            <td v-else>{{item.Caller}}</td>
            <td>{{item.CallStatus}}</td>
            <td>{{item.starttime}}</td>
            <td>{{item.endtime}}</td>
            <td>{{item.callDuration}}</td>
            <td>
                <audio :src="item.callrecording" controls="controls" style="width: 130px;"></audio>
            </td>
            <td>{{item.getDate}}</td>
            <td v-if="calltype=='salesdetails'">
                <button v-if="item.comment != '' " class="btn btn-info btn-sm text-justify text-white" type="button" data-bs-toggle="modal"  dataset-backdrop="static" dataset-keyboard="false" @click="NotAllowed">View Comment</button>
                <button v-else class="btn btn-outline-info btn-sm text-justify " type="button" data-bs-toggle="modal"  dataset-backdrop="static" dataset-keyboard="false" @click="NotAllowed"> Add Comment</button>
            </td>
             <td v-else>
                <button v-if="item.tag != '' " class="btn btn-info btn-sm text-justify text-white" type="button" data-bs-toggle="modal"  dataset-backdrop="static" dataset-keyboard="false" @click="NotAllowed">{{item.tag}}</button>
                <button v-else class="btn btn-outline-info btn-sm text-justify " type="button" data-bs-toggle="modal"  dataset-backdrop="static" dataset-keyboard="false" @click="NotAllowed"> NO TAG</button>
            </td>

        </template>

        <template v-else-if="activeRoutePath=='searchnumberOut'">
            <td>{{index+trimStart+1}}</td>
            <td>{{item.Caller}}</td>
            <td>{{item.extension}}</td>
            <td>
               <button v-if="item.isregistered == true" class="btn btn-info btn-sm text-justify text-white" type="button" data-bs-toggle="modal" data-bs-target="#customerModalFormId" dataset-backdrop="static" dataset-keyboard="false" @click="getCallsDetails(item)" >{{item.CalledNumber}}</button>
               <button v-else class="btn btn-outline-info btn-sm text-justify " type="button" data-bs-toggle="modal" data-bs-target="#customerModalFormId" dataset-backdrop="static" dataset-keyboard="false" @click="getCallsDetails(item)"> {{item.CalledNumber}}</button>
            </td>
            <td>{{item.CallStatus}}</td>
            <td>{{item.starttime}}</td>
            <td>{{item.endtime}}</td>
            <td>{{item.callDuration}}</td>
            <td>
                <audio :src="item.callrecording" controls="controls" style="width: 130px;"></audio>
                
            </td>
            <td>{{item.getDate}}</td>
            <td v-if="calltype=='salesdetails'">
                <button v-if="item.comment != '' " class="btn btn-info btn-sm text-justify text-white" type="button" data-bs-toggle="modal"  dataset-backdrop="static" dataset-keyboard="false" @click="NotAllowed">View Comment</button>
                <button v-else class="btn btn-outline-info btn-sm text-justify " type="button" data-bs-toggle="modal" dataset-backdrop="static" dataset-keyboard="false" @click="NotAllowed"> Add Comment</button>
            </td>
             <td v-else>
                <button v-if="item.tag != '' " class="btn btn-info btn-sm text-justify text-white" type="button" data-bs-toggle="modal" dataset-backdrop="static" dataset-keyboard="false" @click="NotAllowed">{{item.tag}}</button>
                <button v-else class="btn btn-outline-info btn-sm text-justify " type="button" data-bs-toggle="modal"  dataset-backdrop="static" dataset-keyboard="false" @click="NotAllowed"> NO TAG</button>
               
            </td>
        

        </template>
     </tr>
     <cdr-modal-form
         modalId="modalCommentTag"
         modalTitle="Add Comment"
         formId="commentTag"
         formMethod="POST"
         mode="tagandcomment"
         :tags="tags"
         :calltype="calltype"
         :callDetails="callDetails"
         :currentComment="comment"
         :currentTag="tag"
         @emittedData="putCommentTag"
     ></cdr-modal-form>

     <customer-modal-form 
       :customer_id="customer_id"
       :customer_number="customer_number"
       :customer_name="customer_name"
       :updated_by="updated_by"
       :calltype="calltype"
       @emittedCustomerData="setCustomerinfo"
     ></customer-modal-form>
   
</template>

<script>
    import CdrModalForm from '../modal/CdrModalForm.vue'
    import CustomerModalForm from '../modal/CustomerModalForm.vue'

    
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
           },
           activeRoutePath: {
               type: String,
               required: false
           }
          
       },
        data(){
            return {
                 dataBsTarget: '#modalCommentTag',
                 comment: null,
                 tag: null,
                 customer_id: null,
                 customer_name: null,
                 customer_number: null,
                 updated_by: null,
                 callDetails: null,
                 numberPerPage: 5,
                 currentPage: 1
            }
        },
       


        components: {
            CdrModalForm,
            CustomerModalForm,
          
        },

        methods: {
            getCallsDetails(item){
                this.comment = item.comment
                this.tag = item.tag
                this.callDetails = item
                this.customer_id = item.customer_id
                this.customer_number = item.customer_number
                this.customer_name = item.customer_name
                this.updated_by = item.updated_by
            },
            putCommentTag(data){
                this.$emit('emittedData', data)
            },
            NotAllowed(){
                alert('Editing Form Search Result is not allowed.')
                return
            },
            setCustomerinfo(data){

                this.$emit('emittedCustomerData', data)
            }
           

        },
      
    }
    
</script>



