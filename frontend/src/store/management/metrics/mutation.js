export default {
    mutGeneratedMetrics(state, payload){
       if(payload.option_metrics == 'tag'){
           state.tagMetricsGeneratedData = payload.tagMetricsData
           state.tagExportData = payload.tagMetricsData.metricsExportObject 
          
       }else{
           state.cdrMetricsGeneratedData = payload.cdrMetricsData
           state.grandTotalCounts = payload.cdrMetricsData.outSideTableData.grand_total_counts
           state.grandTotalDurations = payload.cdrMetricsData.outSideTableData.grand_total_duration
           state.dateTimeRange =  payload.cdrMetricsData.outSideTableData.datetimeRange

           state.cdrExportData =  payload.cdrMetricsData.metricsExportObject 
          
       }
    }
}