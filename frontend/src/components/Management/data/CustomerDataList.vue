<template>
     <tr v-for="(item, index) in tdata" :key="index">
       <td class="lead text-justify">{{item.customer_number}}</td>
       <td class="lead text-justify">{{item.customer_id}}</td>
       <td class="lead text-justify">{{item.customer_name}}</td>
       <td class="text-primary fw-bold lead text-justify" >{{item.updated_by}}</td>
        <td>
           <!-- <button type="button" class="btn btn-primary btn-sm font-weight-normal lead" data-bs-toggle="modal" :data-bs-target="dataBsTarget" dataset-backdrop="static" dataset-keyboard="false" @click="getAgentInfo(item)" >UPDATE </button> -->
            <button class="btn btn-danger btn-sm font-weight-normal lead" @click="deleteCustomer(item)"  >DELETE</button>
        </td>
     </tr>
     

</template>

<script>
   
    export default {
        
        props:['tdata','agent'],
        data(){
            return{ 
                item: null,

            }
        },
   
        methods:{
            deleteCustomer(item){
                this.$emit('click', item)
            },
          
            
        },
        
     
    }
    
</script>