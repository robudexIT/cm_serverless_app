export default {
    getTagMetricsGeneratedData(state){
        return state.tagMetricsGeneratedData
    },
    getCdrMetricsGeneratedData(state){
        return state.cdrMetricsGeneratedData
    },
    getTagExportData(state){
        return state.tagExportData
    },
    getCdrExportData(state){
        return state.cdrExportData
    },
    getGrandTotalCounts(state){
        return state.grandTotalCounts
    },
    getGrandTotalDurations(state){
        return state.grandTotalDurations
    }, 
    getDateTimeRange(state){
        return state.dateTimeRange
    }
}