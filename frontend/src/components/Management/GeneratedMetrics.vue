<template>
   <base-dialog :show="!!error" @close="handleError">
     <p>{{error}}</p>
   </base-dialog>
  <base-container v-if="isLoading">
      <base-dialog :show="isLoading">
        <base-spinner> <p>Fetching Data From the Database Please Wait....</p></base-spinner>
      </base-dialog>
  </base-container>  
  <base-container v-else>
     <button class="btn btn-primary h-25 p-1 w-100 " @click="exportMetrics">Export <font-awesome-icon icon="spinner" />
     </button>
     <font-awesome-icon icon="coffee"></font-awesome-icon>
     <base-table theader="metricsHeader" tableclass='metrics' :metricsHeader="metricsGenerated.tableHeader">
          <generated-tag-metrics-data-list v-if="option_metrics=='tag'"  :tdata="metricsGenerated.tableTagRecords"></generated-tag-metrics-data-list>
          <generated-cdr-metrics-data-list v-else  :tdata="metricsGenerated.tableCdrRecords" :optiondata="metricsGenerated.outSideTableData"></generated-cdr-metrics-data-list>
     </base-table>
     <div v-if="option_metrics != 'tag'">
         <p>Date Range: {{dateTimeRange}}</p>
          <p>Grand Total Counts: {{grandTotalCounts}}</p>
         <p>Grand Total Call Duration(HH:MM:SS): {{grandTotalDurations}}</p>
     </div> 
     
  </base-container>
     
</template>


<script>

import BaseContainer from '../layout/BaseContainer.vue'
import GeneratedTagMetricsDataList from './data/GeneratedTagMetricsDataList.vue'
import GeneratedCdrMetricsDataList  from './data/GeneratedCdrMetricsDataList.vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
export default {
  
    components: {
        GeneratedTagMetricsDataList,
        GeneratedCdrMetricsDataList,
        BaseContainer,
        FontAwesomeIcon
    },
    props: ['sort_order','option_metrics'],
    data(){
        return {
            error: null,
            isLoading: false,
            appName: this.$store.getters.getAppName
        }
    },
    methods: {
       async generateMetrics(){
            //get option_metrics from the querystring and add metrics word to it 
            //and assign it to this.metricsHeader to get the assign table header

            let querystring = window.location.search.substring(1)
          
            // this.metricsHeader = 'metrics_'+ this.option_metrics
            try {
              this.isLoading = true
               await this.$store.dispatch('metrics/generateMetrics',{querystring,sort_order:this.sort_order, option_metrics:this.option_metrics})
               this.isLoading = false
            }catch(e){
                this.error = e.message
            }
        },
        exportMetrics(){
            let dataToBeExported
            if(this.option_metrics == 'tag'){
                dataToBeExported = this.$store.getters['metrics/getTagExportData']
            }else{
                dataToBeExported = this.$store.getters['metrics/getCdrExportData']
                 
            }
        //    console.log(dataToBeExported)  
         window.Jhxlsx.export(dataToBeExported.tableData, dataToBeExported.options);
            
          
        
        },
        handleError(){
            this.error = null
        }
    },
    computed:{
            metricsGenerated(){
                let  metricsGenerated
                if(this.option_metrics == 'tag'){
                     metricsGenerated = this.$store.getters['metrics/getTagMetricsGeneratedData']
                }else if(this.option_metrics == 'callduration' || 
                         this.option_metrics =='callcounts'   ||
                         this.option_metrics == 'blended'       
                       ){
                          metricsGenerated = this.$store.getters['metrics/getCdrMetricsGeneratedData']
                          
                }else{
                    metricsGenerated = 'This Metrics is not available'
                }
              
                return metricsGenerated
            },
            dateTimeRange(){
                return this.$store.getters['metrics/getDateTimeRange']
            }, 
            grandTotalCounts(){
                return this.$store.getters['metrics/getGrandTotalCounts']
            },
            grandTotalDurations(){
                return this.$store.getters['metrics/getGrandTotalDurations']
            },
             getAutoLogoutStatus(){
                 return this.$store.getters['getAutoLogoutStatus']
             }
    },
    created(){
        this.$store.dispatch('checkIfCurrentLogin')
        this.generateMetrics()

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
