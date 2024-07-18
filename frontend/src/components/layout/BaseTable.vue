<template>
    <table class="table" :class="tableStriped">
                <thead :class="tableDark">
                    <table-header :theader="theader" :metricsHeader="metricsHeader" :calltype="calltype"> 
                        <th scope="col">
                              <button type="button" class="btn btn-primary btn-small search_btn" data-bs-toggle="modal" data-bs-target="#myDateRange" dataset-backdrop="static" dataset-keyboard="false" id="selectdate">SELECT DATE</button>
                            
                              <button v-if="theader=='csdinbound' || theader=='csdoutbound' || theader == 'collection' || theader == 'sales' || theader=='missedcalls'" type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#searchnumber" dataset-backdrop="static" dataset-keyboard="false">SEARCH</button>
                        </th>
                    </table-header>
                    
                </thead>
                <tbody>
                    <slot></slot>
                </tbody>
  </table>

  <select-date-range-modal-form :tags="tags" :calltype="calltype" @emittedData="searchResult"></select-date-range-modal-form> 
  <search-number-modal-form  :calltype="calltype" @emittedDataSearchNumber="searchNumberResult"></search-number-modal-form>


</template>

<script>
 import { defineAsyncComponent } from 'vue'
// import SelectDateRangeModalForm from '../agentcdr/modal/SelectDateRangeModalForm.vue'
// import SearchNumberModalForm from '../agentcdr/modal/SearchNumberModalForm.vue'
 import TableHeader from './tablelayout/TableHeader.vue'

//async-lazy loading for production
const SelectDateRangeModalForm = defineAsyncComponent(() => import('../agentcdr/modal/SelectDateRangeModalForm.vue'))
const SearchNumberModalForm = defineAsyncComponent(() => import('../agentcdr/modal/SearchNumberModalForm.vue'))


export default {
    props: ['theader','tdata','tableclass', 'metricsHeader', 'tags','calltype'],
    components: {
         TableHeader,
            SelectDateRangeModalForm,
            SearchNumberModalForm
         
    },
    methods:{
      searchResult(from,to,tag,duration,direction){
        
         
         this.$emit('emittedData',from,to,tag,duration, direction)
     },
     searchNumberResult(data){
        
         this.$emit('emittedDataSearchNumber',data)
     },
    },
    computed: {
        tableDark(){
           return this.tableclass == 'cdr'  || this.tableclass == "metrics" ? 'table-dark': ''
        },
        tableStriped(){
            return this.tableclass == 'agent' || this.tableclass == 'tags' || this.tableclass == 'customerinfo'?  'table table-striped': ''
        }
    },

}
</script>

<style scoped>
    .search_btn {
        border-radius: 10px;
    }
    
</style>