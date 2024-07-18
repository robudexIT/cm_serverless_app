<template>
     <tr v-for="(item, index) in tdata" :key="index">
        <td>{{index+1}}</td>
       <td>{{item.starttime}}</td>
       <td>{{item.endtime}}</td>
       <!-- <td>{{item.caller}}</td> -->
        <td>
        <button v-if="item.isRegistered == true" class="btn btn-info btn-sm text-justify text-white" type="button" data-bs-toggle="modal" data-bs-target="#customerModalFormId" dataset-backdrop="static" dataset-keyboard="false" @click="getCallsDetails(item)" >{{item.Caller}}</button>
        <button v-else class="btn btn-outline-info btn-sm text-justify " type="button" data-bs-toggle="modal" data-bs-target="#customerModalFormId" dataset-backdrop="static" dataset-keyboard="false" @click="getCallsDetails(item)"> {{item.Caller}}</button>
        </td>
       <td>{{item.CallStatus}}</td>
       <td>
            <button v-if="item.comment != ''" type="button" class="btn btn-info btn-sm text-justify text-white" data-bs-toggle="modal" :data-bs-target="dataBsTarget" dataset-backdrop="static" dataset-keyboard="false" @click="getCallsDetails(item)">{{limitCommentTitle(item.comment)}}</button>
            
            <button v-else class="btn btn-outline-info btn-sm text-justify " type="button" data-bs-toggle="modal" :data-bs-target="dataBsTarget" dataset-backdrop="static" dataset-keyboard="false" id="comment_tag" @click="getCallsDetails(item)" >No Comment</button>
       </td>
       <td>{{item.commentby}}</td>
       <td>{{item.getdate}}</td>
     </tr>
     <teleport to='body'>
        <cdr-modal-form
            modalId="modalCommentTag"
            modalTitle="Add Comment"
            formId="commentTag"
            formMethod="POST"
            mode="commentonly"
            :callDetails="callDetails"
            :currentComment="comment"
            :tag="tag"
            @emittedData="putCommentTag"
        ></cdr-modal-form>
    </teleport>


     <customer-modal-form 
       :customer_id="customer_id"
       :customer_number="customer_number"
       :customer_name="customer_name"
       :updated_by="updated_by"
       calltype="missedcallsdetails"
       @emittedCustomerData="setCustomerinfo"
     ></customer-modal-form>
</template>

<script>
   import CdrModalForm from '../modal/CdrModalForm.vue'
   import CustomerModalForm from '../modal/CustomerModalForm.vue'
    export default {
        props:['tdata'],
        components: {
            CdrModalForm,
            CustomerModalForm
        },
        data(){
            return {
                dataBsTarget: '#modalCommentTag',
                comment: null,
                callDetails: null,
                customer_id: null,
                 customer_name: null,
                 customer_number: null,
                 updated_by: null,
            }
        },
        methods: {
            limitCommentTitle(comment, limit = 30)  {
                var newComment = [];
                if (comment.length > limit) {
                    comment.split(' ').reduce((acc, cur) => {
                        if (acc + cur.length <= limit) {
                            newComment.push(cur);
                        }
                        return acc + cur.length;
                    }, 0);

                    // return the result
                    return `${newComment.join(' ')} ...`;
                }
                return comment;
            }, 
            getCallsDetails(item){
                this.comment = item.comment
                this.callDetails = item
                this.customer_id = item.customer_id
                this.customer_number = item.customer_number
                this.customer_name = item.customer_name
                this.updated_by = item.updated_by
            },
            putCommentTag(data){
                this.$emit('emittedData',data)
            },
            setCustomerinfo(data){

                this.$emit('emittedCustomerData', data)
            }
        },
        computed:{
            buttonText(item){
                return item.comment == '' ? 'No Comment' : item.comment
            }
        },
        created(){
            console.log(this.tdata)
        }
     
    }
    
</script>



